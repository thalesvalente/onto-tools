#!/usr/bin/env python
"""
run_rc.py — Single entry-point for the full canonical RC pipeline.

Modes:
    python scripts/run_rc.py                    # autodiscover next RC_vNN_CANON
    python scripts/run_rc.py --rc-root <path>   # use explicit bundle path
    python scripts/run_rc.py --no-fill           # skip derived-doc fill step

Phases executed:
    FASES 1-6  — primary artifacts   (always)
    Fill       — derived docs via fill_rc_bundle.py (unless --no-fill)
    Verify     — consistency checks + final report

The rc_root must be a NEW directory (must not yet exist).
Expected pattern: outputs/logs/RC_v{NN}_CANON/{execution_id}/
"""
import argparse
import json
import hashlib
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root and defaults
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "examples" / "energy-domain-ontology.ttl"
COVERAGE_THRESHOLD = 95.0
LOGS_DIR = PROJECT_ROOT / "outputs" / "logs"

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.adapters.logging.audit_logger import create_audit_logger
from onto_tools.application.facade import OntoToolsFacade
from onto_tools.application.verification.hasher import sha256_file
from onto_tools.application.verification.isomorphism import compare_isomorphism
from onto_tools.application.verification.idempotency import check_idempotency


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Execute canonical RC pipeline (phases 1-6 + fill + verify)."
    )
    parser.add_argument(
        "--rc-root",
        type=Path,
        default=None,
        help="Path to the new RC bundle root. If omitted, auto-discovers next RC_vNN_CANON.",
    )
    parser.add_argument(
        "--no-fill",
        action="store_true",
        help="Skip the derived-doc fill step (debug use).",
    )
    args = parser.parse_args()

    if args.rc_root is not None:
        rc_root = args.rc_root if args.rc_root.is_absolute() else PROJECT_ROOT / args.rc_root
    else:
        rc_root = None

    return rc_root, args.no_fill


# ---------------------------------------------------------------------------
# Version discovery helpers
# ---------------------------------------------------------------------------
def _discover_next_version() -> tuple[int, str]:
    """Scan outputs/logs/ for RC_vNN_CANON dirs and return (next_nn, version_str)."""
    pattern = re.compile(r"^RC_v(\d+)_CANON$", re.IGNORECASE)
    existing_nns: list[int] = []
    if LOGS_DIR.exists():
        for d in LOGS_DIR.iterdir():
            m = pattern.match(d.name)
            if m and d.is_dir():
                existing_nns.append(int(m.group(1)))
    next_nn = (max(existing_nns) + 1) if existing_nns else 1
    return next_nn, f"RC_v{next_nn}_CANON"


def _create_execution_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    uid = uuid.uuid4().hex[:8]
    return f"{ts}_{uid}"


def _read_json_safe(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def banner(msg):
    print(f"\n{'='*72}")
    print(f"  {msg}")
    print(f"{'='*72}")


def _extract_nn(rc_version: str) -> int:
    """Extract NN integer from 'RC_vNN_CANON'."""
    m = re.search(r"RC_v(\d+)_CANON", rc_version, re.IGNORECASE)
    if not m:
        raise ValueError(f"Cannot extract NN from rc_version={rc_version!r}")
    return int(m.group(1))


# ===================================================================
# FASE 1 — Create Structure
# ===================================================================
def fase1_create_structure(rc_root: Path, rc_version: str, execution_id: str):
    banner(f"FASE 1 — Create RC Structure ({rc_version})")
    dirs = [
        rc_root / "00_meta",
        rc_root / "10_proofs",
        rc_root / "20_runs" / "run2a_canonicalize",
        rc_root / "20_runs" / "run2b_canonicalize",
        rc_root / "20_runs" / "run3_normalize_canonicalize",
        rc_root / "20_runs" / "run4_normalize_canonicalize",
        rc_root / "30_gates",
        rc_root / "40_tests",
        rc_root / "50_qa",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR] {d.relative_to(PROJECT_ROOT)}")

    input_hash = sha256_file(INPUT_FILE)
    graph, meta = RDFlibAdapter.load_ttl(str(INPUT_FILE))
    input_triples = len(graph)

    env_snapshot = {
        "rc_version": rc_version,
        "execution_id": execution_id,
        "python_version": sys.version.split()[0],
        "input_file": str(INPUT_FILE.relative_to(PROJECT_ROOT)),
        "input_sha256": input_hash,
        "input_triples": input_triples,
        "input_size_bytes": INPUT_FILE.stat().st_size,
        "coverage_threshold": COVERAGE_THRESHOLD,
    }
    write_json(rc_root / "00_meta" / "env_snapshot.json", env_snapshot)
    print(f"  Input SHA256: {input_hash}")
    print(f"  Input triples: {input_triples}")
    return input_hash, input_triples, graph


# ===================================================================
# FASE 2 — Determinism (Run2a, Run2b)
# ===================================================================
def _run_canonicalize(input_path: Path, output_path: Path, run_name: str, rc_root: Path):
    """Load, canonicalize, save, return hash."""
    banner(f"  {run_name}: Canonicalize")
    rdf = RDFlibAdapter()
    audit = create_audit_logger(rc_root / "20_runs" / run_name)
    facade = OntoToolsFacade(
        rdf_adapter=rdf,
        audit_logger=audit,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade.load_ontology(str(input_path))
    facade.canonicalize_ontology()
    facade.generate_review_output(str(output_path))

    out_hash = sha256_file(output_path)
    out_graph, _ = RDFlibAdapter.load_ttl(str(output_path))
    print(f"    Output SHA256: {out_hash}")
    print(f"    Output triples: {len(out_graph)}")
    return out_hash, len(out_graph), out_graph


def fase2_determinism(rc_root: Path):
    banner("FASE 2 — Determinism Gate")
    run2a_dir = rc_root / "20_runs" / "run2a_canonicalize"
    run2b_dir = rc_root / "20_runs" / "run2b_canonicalize"
    out2a = run2a_dir / "canonical_output_run2a.ttl"
    out2b = run2b_dir / "canonical_output_run2b.ttl"

    h2a, t2a, g2a = _run_canonicalize(INPUT_FILE, out2a, "run2a_canonicalize", rc_root)
    h2b, t2b, g2b = _run_canonicalize(INPUT_FILE, out2b, "run2b_canonicalize", rc_root)

    det_pass = h2a == h2b
    print(f"\n  Determinism: {'PASS' if det_pass else 'FAIL'}")
    print(f"    Run2a: {h2a}")
    print(f"    Run2b: {h2b}")

    if not det_pass:
        print("  FAIL FAST — hashes differ!")
        sys.exit(1)

    gate = {
        "gate_id": "determinism",
        "gate_name": "Byte-level Determinism (Article Claim iii)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if det_pass else "FAIL",
        "evidence": {
            "run2a_output_hash": h2a,
            "run2b_output_hash": h2b,
            "hashes_match": det_pass,
        },
        "article_claim": "(iii) Determinism",
    }
    write_json(rc_root / "30_gates" / "gate_determinism.json", gate)
    return h2a, t2a, g2a


# ===================================================================
# FASE 3 — Normalize (Run3 validate, Run4 auto-fix)
# ===================================================================
def fase3_normalize(rc_root: Path):
    banner("FASE 3 — Normalize")

    # Run3: validate-only
    print("\n  Run3: normalize (validate-only)...")
    rdf3 = RDFlibAdapter()
    audit3 = create_audit_logger(rc_root / "20_runs" / "run3_normalize_canonicalize")
    facade3 = OntoToolsFacade(
        rdf_adapter=rdf3, audit_logger=audit3,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade3.load_ontology(str(INPUT_FILE))
    norm3 = facade3.normalize_ontology(auto_fix=False)
    facade3.canonicalize_ontology()
    out3 = rc_root / "20_runs" / "run3_normalize_canonicalize" / "canonical_output_run3.ttl"
    facade3.generate_review_output(str(out3))
    h3 = sha256_file(out3)
    g3, _ = RDFlibAdapter.load_ttl(str(out3))
    print(f"    Run3 output SHA256: {h3}")
    print(f"    Run3 output triples: {len(g3)}")
    write_json(
        rc_root / "20_runs" / "run3_normalize_canonicalize" / "normalize_log_run3.json",
        norm3 if isinstance(norm3, dict) else {"result": str(norm3)},
    )

    # Run4: auto-fix
    print("\n  Run4: normalize (auto-fix)...")
    rdf4 = RDFlibAdapter()
    audit4 = create_audit_logger(rc_root / "20_runs" / "run4_normalize_canonicalize")
    facade4 = OntoToolsFacade(
        rdf_adapter=rdf4, audit_logger=audit4,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade4.load_ontology(str(INPUT_FILE))
    norm4 = facade4.normalize_ontology(auto_fix=True)
    facade4.canonicalize_ontology()
    out4 = rc_root / "20_runs" / "run4_normalize_canonicalize" / "canonical_output_run4.ttl"
    facade4.generate_review_output(str(out4))
    h4 = sha256_file(out4)
    g4, _ = RDFlibAdapter.load_ttl(str(out4))
    print(f"    Run4 output SHA256: {h4}")
    print(f"    Run4 output triples: {len(g4)}")
    write_json(
        rc_root / "20_runs" / "run4_normalize_canonicalize" / "normalize_log_run4.json",
        norm4 if isinstance(norm4, dict) else {"result": str(norm4)},
    )

    return h3, len(g3), g3, h4, len(g4), g4, norm3, norm4


# ===================================================================
# FASE 4 — Gates (Isomorphism + Idempotency)
# ===================================================================
def _canonicalize_transform(input_path: Path, output_path: Path, rc_root: Path):
    """Transform function for idempotency check."""
    rdf = RDFlibAdapter()
    # Use the run2a bundle dir so audit logs land inside 20_runs/, not in the
    # temporary directory that check_idempotency passes as output_path.parent.
    audit = create_audit_logger(rc_root / "20_runs" / "run2a_canonicalize")
    facade = OntoToolsFacade(
        rdf_adapter=rdf, audit_logger=audit,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade.load_ontology(str(input_path))
    facade.canonicalize_ontology()
    facade.generate_review_output(str(output_path))


def fase4_gates(rc_root: Path):
    banner("FASE 4 — Verification Gates")

    out2a = rc_root / "20_runs" / "run2a_canonicalize" / "canonical_output_run2a.ttl"
    out3 = rc_root / "20_runs" / "run3_normalize_canonicalize" / "canonical_output_run3.ttl"

    print("  Isomorphism check (input vs run2a)...")
    iso_2a = compare_isomorphism(str(INPUT_FILE), str(out2a))
    print(f"    Run2a isomorphic: {iso_2a.are_isomorphic}")
    write_json(rc_root / "20_runs" / "run2a_canonicalize" / "isomorphism_run2a.json",
               iso_2a.to_dict())

    print("  Isomorphism check (input vs run3)...")
    iso_3 = compare_isomorphism(str(INPUT_FILE), str(out3))
    print(f"    Run3 isomorphic: {iso_3.are_isomorphic}")
    write_json(rc_root / "20_runs" / "run3_normalize_canonicalize" / "isomorphism_run3.json",
               iso_3.to_dict())

    gate_iso = {
        "gate_id": "isomorphism",
        "gate_name": "Semantic Preservation / RDF Isomorphism (Article Claim ii)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if iso_2a.are_isomorphic and iso_3.are_isomorphic else "FAIL",
        "evidence": {
            "run2a_isomorphism": {
                "are_isomorphic": iso_2a.are_isomorphic,
                "input_triples": iso_2a.graph_a_triple_count,
                "output_triples": iso_2a.graph_b_triple_count,
            },
            "run3_isomorphism": {
                "are_isomorphic": iso_3.are_isomorphic,
                "input_triples": iso_3.graph_a_triple_count,
                "output_triples": iso_3.graph_b_triple_count,
            },
        },
        "article_claim": "(ii) Semantic Preservation",
    }
    write_json(rc_root / "30_gates" / "gate_isomorphism.json", gate_iso)

    print("  Idempotency check...")
    # Wrap transform to pass rc_root via closure
    def _transform(inp: Path, out: Path):
        _canonicalize_transform(inp, out, rc_root)

    idemp = check_idempotency(str(out2a), _transform)
    print(f"    Idempotent: {idemp.is_idempotent}")
    write_json(rc_root / "20_runs" / "run2a_canonicalize" / "idempotency_run2a.json",
               idemp.to_dict())

    gate_idemp = {
        "gate_id": "idempotency",
        "gate_name": "Idempotency (Article Claim i)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if idemp.is_idempotent else "FAIL",
        "evidence": {
            "is_idempotent": idemp.is_idempotent,
            "hashes_match": idemp.hashes_match,
            "first_result_hash": idemp.first_result_hash,
            "second_result_hash": idemp.second_result_hash,
        },
        "article_claim": "(i) Idempotency",
    }
    write_json(rc_root / "30_gates" / "gate_idempotency.json", gate_idemp)

    all_pass = (iso_2a.are_isomorphic and iso_3.are_isomorphic and idemp.is_idempotent)
    print(f"\n  All gates: {'PASS' if all_pass else 'FAIL'}")
    return all_pass


# ===================================================================
# FASE 5 — Tests + Coverage
# ===================================================================
def fase5_tests(rc_root: Path):
    banner("FASE 5 — Tests + Coverage")
    import re as _re
    import os

    TEST_SCOPE = "tests/1-uc-ontology"
    cwd_str = str(PROJECT_ROOT)

    junit_xml_path = rc_root / "40_tests" / "junit.xml"
    cov_xml_path   = rc_root / "40_tests" / "coverage.xml"
    cov_json_path  = rc_root / "40_tests" / "coverage.json"
    cov_html_dir   = rc_root / "40_tests" / "coverage_html"

    cmd = [
        sys.executable, "-m", "pytest", TEST_SCOPE,
        "-v", "--no-header", "--tb=short",
        "--durations=10",
        f"--junitxml={junit_xml_path}",
        "--cov=src/onto_tools",
        "--cov-report=term",
        f"--cov-report=xml:{cov_xml_path}",
        f"--cov-report=json:{cov_json_path}",
        f"--cov-report=html:{cov_html_dir}",
    ]
    env = os.environ.copy()
    src_path = str(PROJECT_ROOT / "src")
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")

    cmd_str = f"PYTHONPATH={src_path} " + " ".join(cmd)
    print(f"  Running: {cmd_str}")

    (rc_root / "40_tests" / "pytest_cmd.txt").write_text(cmd_str + "\n", encoding="utf-8")

    t0 = time.time()
    result = subprocess.run(cmd, cwd=cwd_str, env=env,
                            capture_output=True, text=True, timeout=600)
    duration = time.time() - t0

    full_output = result.stdout + "\n" + result.stderr
    (rc_root / "40_tests" / "pytest_full.txt").write_text(full_output, encoding="utf-8")

    # pytest_output.txt — real stdout from the main run (no stderr)
    (rc_root / "40_tests" / "pytest_output.txt").write_text(result.stdout, encoding="utf-8")

    # pytest_durations.txt — extract slow tests from the already-completed run output
    # Parses the "slowest durations" section emitted by --tb=short output, or
    # produces a durations summary from the real full output without a second pytest run.
    try:
        dur_lines: list[str] = []
        in_slow = False
        import re as _re
        _ansi = _re.compile(r'\x1b\[[0-9;]*m')
        for line in (result.stdout + "\n" + result.stderr).splitlines():
            clean = _ansi.sub("", line)
            if "slowest" in clean.lower() and "duration" in clean.lower():
                in_slow = True
            if in_slow:
                dur_lines.append(line)
                # section ends at blank line or next separator (after the header line)
                if len(dur_lines) > 2 and (clean.strip() == "" or clean.strip().startswith("=")):
                    break
        if not dur_lines:
            # No slowest section emitted — emit a brief note derived from pytest_summary
            durations_text = (
                f"# Durations — {TEST_SCOPE}\n"
                f"# source: extracted from 40_tests/pytest_full.txt\n"
                f"# note: pytest did not emit a slowest-durations section in this run.\n"
                f"# To obtain durations, add --durations=10 --durations-min=0.5 to the cmd.\n"
            )
        else:
            clean_dur_lines = [_ansi.sub("", ln) for ln in dur_lines]
            durations_text = (
                f"# Durations — {TEST_SCOPE}\n"
                f"# source: extracted from 40_tests/pytest_full.txt\n\n"
                + "\n".join(clean_dur_lines) + "\n"
            )
        (rc_root / "40_tests" / "pytest_durations.txt").write_text(durations_text, encoding="utf-8")
        print(f"  Durations saved ({len(dur_lines)} lines extracted from full output)")
    except Exception as exc:
        (rc_root / "40_tests" / "pytest_durations.txt").write_text(
            f"# durations extraction failed: {exc}\n", encoding="utf-8"
        )
        print(f"  [WARN] durations extraction failed: {exc}")

    # pytest_collection.txt — real collection via --collect-only
    collect_cmd = [sys.executable, "-m", "pytest", TEST_SCOPE, "--collect-only", "-q"]
    collect_cmd_str = "PYTHONPATH=" + src_path + " " + " ".join(collect_cmd)
    print(f"  Collecting: {collect_cmd_str}")
    try:
        collect_result = subprocess.run(
            collect_cmd, cwd=cwd_str, env=env,
            capture_output=True, text=True, timeout=120,
        )
        collection_text = (
            f"# pytest --collect-only -q {TEST_SCOPE}\n"
            f"# command: {collect_cmd_str}\n"
            f"# exit_code: {collect_result.returncode}\n\n"
            + collect_result.stdout
            + ("\n" + collect_result.stderr if collect_result.stderr.strip() else "")
        )
        (rc_root / "40_tests" / "pytest_collection.txt").write_text(collection_text, encoding="utf-8")
        print(f"  Collection saved ({len(collect_result.stdout.splitlines())} lines)")
    except Exception as exc:
        (rc_root / "40_tests" / "pytest_collection.txt").write_text(
            f"# collection failed: {exc}\n", encoding="utf-8"
        )
        print(f"  [WARN] --collect-only failed: {exc}")

    lines = result.stdout.strip().splitlines()
    summary_line = [l for l in lines if "passed" in l]
    summary_text = summary_line[-1] if summary_line else ""
    print(f"  {summary_text}")

    m = _re.search(r"(\d+)\s+passed", summary_text)
    passed = int(m.group(1)) if m else 0
    m = _re.search(r"(\d+)\s+failed", summary_text)
    failed = int(m.group(1)) if m else 0
    m = _re.search(r"(\d+)\s+error", summary_text)
    errors = int(m.group(1)) if m else 0
    m = _re.search(r"(\d+)\s+skipped", summary_text)
    skipped = int(m.group(1)) if m else 0
    collected = passed + failed + errors + skipped

    cov_line = [l for l in lines if "TOTAL" in l]
    total_cov = 0.0
    if cov_line:
        m = _re.search(r"(\d+\.\d+)%", cov_line[-1])
        if m:
            total_cov = float(m.group(1))
        else:
            m = _re.search(r"\s(\d+)%", cov_line[-1])
            if m:
                total_cov = float(m.group(1))

    pytest_version = "unknown"
    try:
        ver_result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        m_ver = _re.search(r"pytest\s+(\S+)", ver_result.stdout + ver_result.stderr)
        if m_ver:
            pytest_version = m_ver.group(1)
    except Exception:
        pass

    cov_passed = total_cov >= COVERAGE_THRESHOLD
    tests_passed = failed == 0 and errors == 0 and passed > 0

    print(f"  Passed: {passed}, Failed: {failed}, Errors: {errors}, Skipped: {skipped}")
    print(f"  Coverage: {total_cov:.2f}% (threshold: {COVERAGE_THRESHOLD}%)")
    print(f"  Return code: {result.returncode}")

    summary = {
        "test_suite": TEST_SCOPE,
        "command": cmd_str,
        "cwd": cwd_str,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pytest_version": pytest_version,
        "python_version": sys.version.split()[0],
        "results": {
            "collected": collected,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "duration_seconds": round(duration, 2),
        },
        "coverage": {
            "total_percent": total_cov,
            "threshold_required": COVERAGE_THRESHOLD,
            "passed": cov_passed,
        },
        "returncode": result.returncode,
        "sources": [
            str((rc_root / "40_tests" / "pytest_full.txt").relative_to(PROJECT_ROOT)),
            str((rc_root / "40_tests" / "pytest_cmd.txt").relative_to(PROJECT_ROOT)),
        ],
        "coverage_reports": {
            "xml":  str(cov_xml_path.relative_to(PROJECT_ROOT)),
            "json": str(cov_json_path.relative_to(PROJECT_ROOT)),
            "html": str(cov_html_dir.relative_to(PROJECT_ROOT)),
        },
        "junit_xml": str(junit_xml_path.relative_to(PROJECT_ROOT)),
    }
    write_json(rc_root / "40_tests" / "pytest_summary.json", summary)
    return tests_passed, cov_passed, passed, failed, total_cov, duration


# ===================================================================
# FASE 6 — Evidence Bundle
# ===================================================================
def fase6_evidence(rc_root: Path, rc_version: str):
    banner("FASE 6 — Evidence Bundle (Checksums)")

    checksums = []
    for fp in sorted(rc_root.rglob("*")):
        if fp.is_file():
            rel = fp.relative_to(rc_root)
            h = sha256_file(fp)
            checksums.append((h.lower(), str(rel).replace("\\", "/")))

    ck_lines = [
        f"# SHA256 Checksums for {rc_version}",
        f"# Generated: {datetime.now(timezone.utc).isoformat()}",
        f"# Total files: {len(checksums)}",
        "#",
    ]
    for h, rel in checksums:
        ck_lines.append(f"{h}  {rel}")

    ck_path = rc_root / "CHECKSUMS_SHA256.txt"
    ck_path.write_text("\n".join(ck_lines) + "\n", encoding="utf-8")
    print(f"  Written {len(checksums)} checksums")

    baseline = {
        "baseline_type": "post",
        "rc_version": rc_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": {rel: h for h, rel in checksums},
    }
    write_json(rc_root / "10_proofs" / "BASELINE_POST_SHA256.json", baseline)
    print("  BASELINE_POST_SHA256.json written")

    return len(checksums)


# ===================================================================
# Primary Execution (phases 1-6)
# ===================================================================
def run_primary_phases(rc_root: Path) -> tuple[bool, dict]:
    """Execute FASES 1-6 and write rc_result.json. Returns (success, summary_dict)."""
    rc_version = rc_root.parent.name
    execution_id = rc_root.name
    nn = _extract_nn(rc_version)
    result_filename = f"rc{nn}_result.json"

    banner(f"{rc_version} — Primary Execution (FASES 1-6)")
    print(f"  Execution ID: {execution_id}")
    print(f"  Output: {rc_root.relative_to(PROJECT_ROOT)}")
    t_start = time.time()

    # FASE 1
    input_hash, input_triples, input_graph = fase1_create_structure(
        rc_root, rc_version, execution_id
    )

    # FASE 2
    canon_hash, canon_triples, canon_graph = fase2_determinism(rc_root)

    # FASE 3
    h3, t3, g3, h4, t4, g4, norm3, norm4 = fase3_normalize(rc_root)

    # FASE 4
    gates_pass = fase4_gates(rc_root)

    # FASE 5
    tests_pass, cov_pass, n_passed, n_failed, coverage, test_duration = fase5_tests(rc_root)

    # FASE 6
    n_checksums = fase6_evidence(rc_root, rc_version)

    total_time = time.time() - t_start
    success = gates_pass and tests_pass and cov_pass

    banner("PRIMARY RESULT")
    print(f"  Status: {'SUCCESS' if success else 'FAIL'}")
    print(f"  Gates: {'PASS' if gates_pass else 'FAIL'}")
    print(f"  Tests: {n_passed} passed, {n_failed} failed")
    print(f"  Coverage: {coverage:.2f}%")
    print(f"  Evidence files: {n_checksums}")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Bundle: {rc_root}")

    def _read_gate_status(gate_file: Path) -> str:
        try:
            with open(gate_file, encoding="utf-8") as f:
                return json.load(f).get("status", "UNKNOWN")
        except Exception:
            return "MISSING"

    gate_det = _read_gate_status(rc_root / "30_gates" / "gate_determinism.json")
    gate_iso = _read_gate_status(rc_root / "30_gates" / "gate_isomorphism.json")
    gate_idemp = _read_gate_status(rc_root / "30_gates" / "gate_idempotency.json")

    result_summary = {
        "rc_version": rc_version,
        "execution_id": execution_id,
        "bundle_path": str(rc_root.relative_to(PROJECT_ROOT)),
        "status": "SUCCESS" if success else "FAIL",
        "input_sha256": input_hash,
        "input_triples": input_triples,
        "canon_sha256": canon_hash,
        "canon_triples": canon_triples,
        "run3_sha256": h3,
        "run4_sha256": h4,
        "gates": {
            "determinism": gate_det,
            "isomorphism": gate_iso,
            "idempotency": gate_idemp,
        },
        "tests": {
            "passed": n_passed,
            "failed": n_failed,
            "coverage": coverage,
        },
        "total_duration_seconds": round(total_time, 2),
        "sources": {
            "gates": "30_gates/*.json",
            "tests": "40_tests/pytest_summary.json",
            "baseline_post": "10_proofs/BASELINE_POST_SHA256.json",
        },
    }
    write_json(rc_root / result_filename, result_summary)
    write_json(rc_root / "rc_result.json", result_summary)

    return success, result_summary


# ===================================================================
# Fill (derived docs)
# ===================================================================
def run_fill(rc_root: Path) -> bool:
    """Run fill_rc_bundle.py --rc-root <rc_root>. Returns True on success."""
    import os

    banner("FILL — Derived Documentation (fill_rc_bundle.py)")
    fill_script = PROJECT_ROOT / "scripts" / "fill_rc_bundle.py"
    if not fill_script.exists():
        print(f"[ERROR] fill script not found: {fill_script}", file=sys.stderr)
        return False

    required_primaries = [
        "00_meta/env_snapshot.json",
        "10_proofs/BASELINE_POST_SHA256.json",
        "30_gates/gate_determinism.json",
        "30_gates/gate_isomorphism.json",
        "30_gates/gate_idempotency.json",
        "40_tests/pytest_summary.json",
        "40_tests/pytest_full.txt",
        "rc_result.json",
    ]
    missing = [f for f in required_primaries if not (rc_root / f).exists()]
    if missing:
        print("[BLOCKED] Fill cannot run — missing primary artifacts:")
        for m in missing:
            print(f"  - {m}")
        return False

    env = os.environ.copy()
    src_path = str(PROJECT_ROOT / "src")
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, str(fill_script), "--rc-root", str(rc_root)],
        cwd=str(PROJECT_ROOT),
        env=env,
    )
    return result.returncode == 0


# ===================================================================
# Verification + Final Report
# ===================================================================
def run_verification(rc_root: Path, primary_failed: bool, fill_blocked: bool) -> bool:
    """Consistency checks and final report. Returns True if all OK."""
    banner("VERIFICATION")

    rc_version = rc_root.parent.name
    execution_id = rc_root.name

    rc_result = _read_json_safe(rc_root / "rc_result.json")
    pytest_summary = _read_json_safe(rc_root / "40_tests" / "pytest_summary.json")
    gate_det = _read_json_safe(rc_root / "30_gates" / "gate_determinism.json")
    gate_iso = _read_json_safe(rc_root / "30_gates" / "gate_isomorphism.json")
    gate_idemp = _read_json_safe(rc_root / "30_gates" / "gate_idempotency.json")

    # Consistency checks
    inconsistencies: list[str] = []

    ps_cmd = pytest_summary.get("command", "")
    ps_suite = pytest_summary.get("test_suite", "")
    if ps_suite and ps_cmd and ps_suite not in ps_cmd:
        inconsistencies.append(
            f"pytest_summary.json: test_suite={ps_suite!r} not found in command={ps_cmd!r}"
        )

    rc_gates = rc_result.get("gates", {})
    for gate_name, gate_data in [
        ("determinism", gate_det),
        ("isomorphism", gate_iso),
        ("idempotency", gate_idemp),
    ]:
        actual_status = gate_data.get("status", "MISSING")
        declared_status = rc_gates.get(gate_name, "MISSING")
        if actual_status != declared_status:
            inconsistencies.append(
                f"Gate {gate_name}: gate JSON says {actual_status!r} but "
                f"rc_result.json says {declared_status!r}"
            )

    rc_tests = rc_result.get("tests", {})
    ps_results = pytest_summary.get("results", {})
    if ps_results.get("passed") is not None and rc_tests.get("passed") is not None:
        if ps_results["passed"] != rc_tests["passed"]:
            inconsistencies.append(
                f"Tests passed: pytest_summary says {ps_results['passed']}, "
                f"rc_result.json says {rc_tests['passed']}"
            )

    # Final report
    banner("FINAL REPORT")

    overall_status = rc_result.get("status", "UNKNOWN")
    p = pytest_summary.get("results", {})
    c = pytest_summary.get("coverage", {})
    gates = rc_result.get("gates", {})

    pytest_cmd_path = rc_root / "40_tests" / "pytest_cmd.txt"
    pytest_cmd_str = (
        pytest_cmd_path.read_text(encoding="utf-8").strip()
        if pytest_cmd_path.exists()
        else "N/A"
    )

    print(f"\n  RC Version   : {rc_version}")
    print(f"  Execution ID : {execution_id}")
    print(f"  RC Root      : {rc_root.relative_to(PROJECT_ROOT)}")
    print(f"  Status       : {overall_status}")
    print(f"\n  Gates:")
    print(f"    Determinism : {gates.get('determinism', 'N/A')}")
    print(f"    Isomorphism : {gates.get('isomorphism', 'N/A')}")
    print(f"    Idempotency : {gates.get('idempotency', 'N/A')}")
    print(f"\n  Tests:")
    print(f"    Scope       : {pytest_summary.get('test_suite', 'N/A')}")
    print(f"    Collected   : {p.get('collected', 'N/A')}")
    print(f"    Passed      : {p.get('passed', 'N/A')}")
    print(f"    Failed      : {p.get('failed', 'N/A')}")
    print(f"    Errors      : {p.get('errors', 'N/A')}")
    print(f"    Duration    : {p.get('duration_seconds', 'N/A')} s")
    print(f"\n  Coverage:")
    print(f"    Total       : {c.get('total_percent', 'N/A')}%")
    print(f"    Threshold   : {c.get('threshold_required', 'N/A')}%")
    print(f"    Passed      : {c.get('passed', 'N/A')}")
    print(f"\n  Pytest command (exact):")
    print(f"    {pytest_cmd_str}")
    print(f"\n  Fill status  : {'PARTIAL (BLOCKED)' if fill_blocked else 'COMPLETE'}")

    if inconsistencies:
        print(f"\n  INCONSISTENCIES FOUND ({len(inconsistencies)}):")
        for inc in inconsistencies:
            print(f"    - {inc}")
    else:
        print("\n  Consistency check: OK (no inconsistencies found)")

    print(f"\n{'='*72}")
    print(f"  Command to reproduce: python scripts/run_rc.py")
    print(f"{'='*72}\n")

    return not (overall_status != "SUCCESS" or fill_blocked or inconsistencies or primary_failed)


# ===================================================================
# Main
# ===================================================================
def main():
    rc_root, no_fill = parse_args()

    # ── Autodiscovery if --rc-root not given ────────────────────
    if rc_root is None:
        banner("run_rc.py — Canonical RC Execution")
        next_nn, rc_version = _discover_next_version()
        execution_id = _create_execution_id()
        rc_root = LOGS_DIR / rc_version / execution_id

        print(f"\n  RC Version  : {rc_version}")
        print(f"  Execution ID: {execution_id}")
        print(f"  RC Root     : {rc_root.relative_to(PROJECT_ROOT)}")

    if rc_root.exists():
        print(f"[ERROR] rc_root already exists: {rc_root}", file=sys.stderr)
        sys.exit(1)

    # ── BLOCO A — Primary execution (phases 1-6) ───────────────
    primary_ok, summary = run_primary_phases(rc_root)
    if not primary_ok:
        print(f"\n[WARNING] Primary phases finished with FAIL status — "
              "will attempt fill if primary artifacts exist.")

    # ── BLOCO B — Fill derived docs ─────────────────────────────
    fill_blocked = False
    if no_fill:
        print("\n  --no-fill: skipping fill step.")
        fill_blocked = True
    else:
        fill_ok = run_fill(rc_root)
        fill_blocked = not fill_ok

    # ── BLOCO C — Verification + Report ─────────────────────────
    all_ok = run_verification(rc_root, primary_failed=not primary_ok, fill_blocked=fill_blocked)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
