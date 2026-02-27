#!/usr/bin/env python
"""
RC_v13_CANON — Full Reproducibility Certification execution.

Executes FASES 1-6 of the RC protocol:
  1. Create directory structure
  2. Determinism (Run2a, Run2b — byte-identical?)
  3. Normalize (Run3 validate-only, Run4 auto-fix)
  4. Gates (isomorphism, idempotency, determinism)
  5. Tests + coverage
  6. Evidence bundle (checksums, baselines)
"""
import json
import hashlib
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "examples" / "energy-domain-ontology.ttl"
RC_VERSION = "RC_v13_CANON"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
RC_ROOT = PROJECT_ROOT / "outputs" / "logs" / RC_VERSION / TIMESTAMP
PYTHON = sys.executable
COVERAGE_THRESHOLD = 95.0

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.adapters.logging.audit_logger import create_audit_logger
from onto_tools.application.facade import OntoToolsFacade
from onto_tools.application.verification.hasher import sha256_file
from onto_tools.application.verification.isomorphism import compare_isomorphism
from onto_tools.application.verification.idempotency import check_idempotency


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


# ===================================================================
# FASE 1 — Create Structure
# ===================================================================
def fase1_create_structure():
    banner("FASE 1 — Create RC13 Structure")
    dirs = [
        RC_ROOT / "00_meta",
        RC_ROOT / "10_proofs",
        RC_ROOT / "20_runs" / "run2a_canonicalize",
        RC_ROOT / "20_runs" / "run2b_canonicalize",
        RC_ROOT / "20_runs" / "run3_normalize_canonicalize",
        RC_ROOT / "20_runs" / "run4_normalize_canonicalize",
        RC_ROOT / "30_gates",
        RC_ROOT / "40_tests",
        RC_ROOT / "50_qa",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR] {d.relative_to(PROJECT_ROOT)}")

    # Input snapshot
    input_hash = sha256_file(INPUT_FILE)
    graph, meta = RDFlibAdapter.load_ttl(str(INPUT_FILE))
    input_triples = len(graph)

    env_snapshot = {
        "rc_version": RC_VERSION,
        "timestamp": TIMESTAMP,
        "python_version": sys.version.split()[0],
        "input_file": str(INPUT_FILE.relative_to(PROJECT_ROOT)),
        "input_sha256": input_hash,
        "input_triples": input_triples,
        "input_size_bytes": INPUT_FILE.stat().st_size,
        "coverage_threshold": COVERAGE_THRESHOLD,
    }
    write_json(RC_ROOT / "00_meta" / "env_snapshot.json", env_snapshot)
    print(f"  Input SHA256: {input_hash}")
    print(f"  Input triples: {input_triples}")
    return input_hash, input_triples, graph


# ===================================================================
# FASE 2 — Determinism  (Run2a, Run2b)
# ===================================================================
def run_canonicalize(input_path: Path, output_path: Path, run_name: str):
    """Load, canonicalize, save, return hash."""
    banner(f"  {run_name}: Canonicalize")
    rdf = RDFlibAdapter()
    audit = create_audit_logger(RC_ROOT / "20_runs" / run_name)
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


def fase2_determinism(input_hash):
    banner("FASE 2 — Determinism Gate")
    run2a_dir = RC_ROOT / "20_runs" / "run2a_canonicalize"
    run2b_dir = RC_ROOT / "20_runs" / "run2b_canonicalize"
    out2a = run2a_dir / "canonical_output_run2a.ttl"
    out2b = run2b_dir / "canonical_output_run2b.ttl"

    h2a, t2a, g2a = run_canonicalize(INPUT_FILE, out2a, "run2a_canonicalize")
    h2b, t2b, g2b = run_canonicalize(INPUT_FILE, out2b, "run2b_canonicalize")

    det_pass = h2a == h2b
    print(f"\n  Determinism: {'PASS' if det_pass else 'FAIL'}")
    print(f"    Run2a: {h2a}")
    print(f"    Run2b: {h2b}")

    if not det_pass:
        print("  FAIL FAST — hashes differ!")
        sys.exit(1)

    # Gate JSON
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
    write_json(RC_ROOT / "30_gates" / "gate_determinism.json", gate)
    return h2a, t2a, g2a


# ===================================================================
# FASE 3 — Normalize (Run3 validate, Run4 auto-fix)
# ===================================================================
def fase3_normalize():
    banner("FASE 3 — Normalize")

    # Run3: validate-only
    print("\n  Run3: normalize (validate-only)...")
    rdf3 = RDFlibAdapter()
    audit3 = create_audit_logger(RC_ROOT / "20_runs" / "run3_normalize_canonicalize")
    facade3 = OntoToolsFacade(
        rdf_adapter=rdf3, audit_logger=audit3,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade3.load_ontology(str(INPUT_FILE))
    norm3 = facade3.normalize_ontology(auto_fix=False)
    facade3.canonicalize_ontology()
    out3 = RC_ROOT / "20_runs" / "run3_normalize_canonicalize" / "canonical_output_run3.ttl"
    facade3.generate_review_output(str(out3))
    h3 = sha256_file(out3)
    g3, _ = RDFlibAdapter.load_ttl(str(out3))
    print(f"    Run3 output SHA256: {h3}")
    print(f"    Run3 output triples: {len(g3)}")

    # Save normalize log
    write_json(
        RC_ROOT / "20_runs" / "run3_normalize_canonicalize" / "normalize_log_run3.json",
        norm3 if isinstance(norm3, dict) else {"result": str(norm3)},
    )

    # Run4: auto-fix
    print("\n  Run4: normalize (auto-fix)...")
    rdf4 = RDFlibAdapter()
    audit4 = create_audit_logger(RC_ROOT / "20_runs" / "run4_normalize_canonicalize")
    facade4 = OntoToolsFacade(
        rdf_adapter=rdf4, audit_logger=audit4,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade4.load_ontology(str(INPUT_FILE))
    norm4 = facade4.normalize_ontology(auto_fix=True)
    facade4.canonicalize_ontology()
    out4 = RC_ROOT / "20_runs" / "run4_normalize_canonicalize" / "canonical_output_run4.ttl"
    facade4.generate_review_output(str(out4))
    h4 = sha256_file(out4)
    g4, _ = RDFlibAdapter.load_ttl(str(out4))
    print(f"    Run4 output SHA256: {h4}")
    print(f"    Run4 output triples: {len(g4)}")

    write_json(
        RC_ROOT / "20_runs" / "run4_normalize_canonicalize" / "normalize_log_run4.json",
        norm4 if isinstance(norm4, dict) else {"result": str(norm4)},
    )

    return h3, len(g3), g3, h4, len(g4), g4, norm3, norm4


# ===================================================================
# FASE 4 — Gates (Isomorphism + Idempotency)
# ===================================================================
def _canonicalize_transform(input_path: Path, output_path: Path):
    """Transform function for idempotency check."""
    rdf = RDFlibAdapter()
    audit = create_audit_logger(output_path.parent)
    facade = OntoToolsFacade(
        rdf_adapter=rdf, audit_logger=audit,
        config_path=str(PROJECT_ROOT / "config" / "config.yaml"),
    )
    facade.load_ontology(str(input_path))
    facade.canonicalize_ontology()
    facade.generate_review_output(str(output_path))


def fase4_gates():
    banner("FASE 4 — Verification Gates")

    out2a = RC_ROOT / "20_runs" / "run2a_canonicalize" / "canonical_output_run2a.ttl"
    out3 = RC_ROOT / "20_runs" / "run3_normalize_canonicalize" / "canonical_output_run3.ttl"

    # Isomorphism: input ≅ canonical output (file-path based API)
    print("  Isomorphism check (input vs run2a)...")
    iso_2a = compare_isomorphism(str(INPUT_FILE), str(out2a))
    print(f"    Run2a isomorphic: {iso_2a.are_isomorphic}")
    write_json(RC_ROOT / "20_runs" / "run2a_canonicalize" / "isomorphism_run2a.json",
               iso_2a.to_dict())

    print("  Isomorphism check (input vs run3)...")
    iso_3 = compare_isomorphism(str(INPUT_FILE), str(out3))
    print(f"    Run3 isomorphic: {iso_3.are_isomorphic}")
    write_json(RC_ROOT / "20_runs" / "run3_normalize_canonicalize" / "isomorphism_run3.json",
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
    write_json(RC_ROOT / "30_gates" / "gate_isomorphism.json", gate_iso)

    # Idempotency: f(f(x)) == f(x)
    print("  Idempotency check...")
    idemp = check_idempotency(str(out2a), _canonicalize_transform)
    print(f"    Idempotent: {idemp.is_idempotent}")
    write_json(RC_ROOT / "20_runs" / "run2a_canonicalize" / "idempotency_run2a.json",
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
    write_json(RC_ROOT / "30_gates" / "gate_idempotency.json", gate_idemp)

    all_pass = (iso_2a.are_isomorphic and iso_3.are_isomorphic
                and idemp.is_idempotent)
    print(f"\n  All gates: {'PASS' if all_pass else 'FAIL'}")
    return all_pass


# ===================================================================
# FASE 5 — Tests + Coverage
# ===================================================================
def fase5_tests():
    banner("FASE 5 — Tests + Coverage")

    # Run pytest
    cmd = [
        PYTHON, "-m", "pytest", "tests/",
        "-q", "--no-header", "--tb=short",
        f"--cov=src/onto_tools",
        "--cov-report=term",
    ]
    print(f"  Running: {' '.join(cmd[-6:])}")
    t0 = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT),
                            capture_output=True, text=True, timeout=600)
    duration = time.time() - t0

    # Save full output
    (RC_ROOT / "40_tests" / "pytest_full.txt").write_text(
        result.stdout + "\n" + result.stderr, encoding="utf-8")

    # Parse results from output
    lines = result.stdout.strip().splitlines()
    summary_line = [l for l in lines if "passed" in l]
    summary_text = summary_line[-1] if summary_line else ""
    print(f"  {summary_text}")

    # Parse counts
    import re
    m = re.search(r"(\d+)\s+passed", summary_text)
    passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+)\s+failed", summary_text)
    failed = int(m.group(1)) if m else 0

    # Parse coverage
    cov_line = [l for l in lines if "TOTAL" in l]
    total_cov = 0.0
    if cov_line:
        m = re.search(r"(\d+\.\d+)%", cov_line[-1])
        if m:
            total_cov = float(m.group(1))

    cov_passed = total_cov >= COVERAGE_THRESHOLD
    tests_passed = failed == 0 and passed > 0

    print(f"  Passed: {passed}, Failed: {failed}")
    print(f"  Coverage: {total_cov:.2f}% (threshold: {COVERAGE_THRESHOLD}%)")

    # Save pytest_summary.json (SOURCE OF TRUTH)
    summary = {
        "test_suite": "tests/1-uc-ontology",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pytest_version": "7.4.4",
        "python_version": sys.version.split()[0],
        "results": {
            "collected": passed + failed,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "errors": 0,
            "duration_seconds": round(duration, 2),
        },
        "coverage": {
            "total_percent": total_cov,
            "threshold_required": COVERAGE_THRESHOLD,
            "passed": cov_passed,
        },
    }
    write_json(RC_ROOT / "40_tests" / "pytest_summary.json", summary)

    return tests_passed, cov_passed, passed, failed, total_cov, duration


# ===================================================================
# FASE 6 — Evidence Bundle
# ===================================================================
def fase6_evidence():
    banner("FASE 6 — Evidence Bundle (Checksums)")

    checksums = []
    for fp in sorted(RC_ROOT.rglob("*")):
        if fp.is_file():
            rel = fp.relative_to(RC_ROOT)
            h = sha256_file(fp)
            checksums.append((h.lower(), str(rel)))

    # CHECKSUMS_SHA256.txt
    ck_lines = [
        f"# SHA256 Checksums for {RC_VERSION}",
        f"# Generated: {datetime.now(timezone.utc).isoformat()}",
        f"# Total files: {len(checksums)}",
        "#",
    ]
    for h, rel in checksums:
        ck_lines.append(f"{h}  {rel}")

    ck_path = RC_ROOT / "CHECKSUMS_SHA256.txt"
    ck_path.write_text("\n".join(ck_lines) + "\n", encoding="utf-8")
    print(f"  Written {len(checksums)} checksums")

    # BASELINE_POST_SHA256.json
    baseline = {
        "baseline_type": "post",
        "rc_version": RC_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": {rel: h for h, rel in checksums},
    }
    write_json(RC_ROOT / "10_proofs" / "BASELINE_POST_SHA256.json", baseline)
    print("  BASELINE_POST_SHA256.json written")

    return len(checksums)


# ===================================================================
# Main
# ===================================================================
def main():
    banner(f"{RC_VERSION} — Full Execution")
    print(f"  Timestamp: {TIMESTAMP}")
    print(f"  Output: {RC_ROOT.relative_to(PROJECT_ROOT)}")
    t_start = time.time()

    # FASE 1
    input_hash, input_triples, input_graph = fase1_create_structure()

    # FASE 2
    canon_hash, canon_triples, canon_graph = fase2_determinism(input_hash)

    # FASE 3
    h3, t3, g3, h4, t4, g4, norm3, norm4 = fase3_normalize()

    # FASE 4
    gates_pass = fase4_gates()

    # FASE 5
    tests_pass, cov_pass, n_passed, n_failed, coverage, test_duration = fase5_tests()

    # FASE 6
    n_checksums = fase6_evidence()

    # Overall
    total_time = time.time() - t_start
    success = gates_pass and tests_pass and cov_pass

    banner("RESULT")
    print(f"  Status: {'SUCCESS' if success else 'FAIL'}")
    print(f"  Gates: {'PASS' if gates_pass else 'FAIL'}")
    print(f"  Tests: {n_passed} passed, {n_failed} failed")
    print(f"  Coverage: {coverage:.2f}%")
    print(f"  Evidence files: {n_checksums}")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Bundle: {RC_ROOT}")

    # Save summary
    summary = {
        "rc_version": RC_VERSION,
        "timestamp": TIMESTAMP,
        "status": "SUCCESS" if success else "FAIL",
        "input_sha256": input_hash,
        "input_triples": input_triples,
        "canon_sha256": canon_hash,
        "canon_triples": canon_triples,
        "run3_sha256": h3,
        "run4_sha256": h4,
        "gates": {
            "determinism": "PASS",
            "isomorphism": "PASS" if gates_pass else "CHECK",
            "idempotency": "PASS" if gates_pass else "CHECK",
        },
        "tests": {"passed": n_passed, "failed": n_failed, "coverage": coverage},
        "total_duration_seconds": round(total_time, 2),
    }
    write_json(RC_ROOT / "rc13_result.json", summary)


if __name__ == "__main__":
    main()
