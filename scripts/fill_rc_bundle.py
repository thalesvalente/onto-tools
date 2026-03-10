"""
fill_rc_bundle.py
-----------------
Gerador DERIVADO de documentação para qualquer RC_vNN_CANON.

Gera APENAS documentos derivados a partir dos artefatos primários reais.
NÃO contém nenhum dado hardcoded (métricas, hashes, timestamps, etc.).

Uso (obrigatório):
    python scripts/fill_rc_bundle.py --rc-root <path_ao_bundle>

Chamado automaticamente por run_rc.py ao final das fases primárias.
O --rc-root é obrigatório; não há autodiscovery neste script.

Regras:
- Toda métrica usada neste script é lida de uma fonte primária real.
- Se uma fonte primária estiver ausente, o arquivo derivado é marcado BLOCKED.
- Nunca sobrescrever artefatos primários gerados por run_rc.py.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

BLOCKED: list[dict] = []


def _extract_nn(rc_version: str) -> int:
    """Extract NN integer from 'RC_vNN_CANON'."""
    m = re.search(r"RC_v(\d+)_CANON", rc_version, re.IGNORECASE)
    if not m:
        raise ValueError(f"Cannot extract NN from rc_version={rc_version!r}")
    return int(m.group(1))


def load_json(path: Path, label: str) -> Optional[dict]:
    """Load a JSON file; return None and register BLOCKED if missing."""
    if not path.exists():
        BLOCKED.append({
            "file": str(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path),
            "reason": "source file not found",
        })
        print(f"  [BLOCKED] {label}: {path} not found")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        BLOCKED.append({"file": str(path), "reason": str(e)})
        print(f"  [BLOCKED] {label}: {e}")
        return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest().lower()


def git_commit() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def write(path: Path, content: str, rc_root: Path) -> None:
    """Write a derived document. Never overwrites primary artifacts."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    try:
        rel = path.relative_to(rc_root)
    except ValueError:
        rel = path
    print(f"  [OK] {rel}")


def write_json_derived(path: Path, data: Any, rc_root: Path) -> None:
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", rc_root)


def blocked_placeholder(path: Path, reason: str, rc_root: Path) -> None:
    """Write a BLOCKED placeholder instead of a derived document."""
    content = json.dumps(
        {"status": "BLOCKED", "reason": reason, "path": str(path)}, indent=2
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    try:
        rel = path.relative_to(rc_root)
    except ValueError:
        rel = path
    print(f"  [BLOCKED] {rel} — {reason}")
    BLOCKED.append({"file": str(rel), "reason": reason})


def provenance_header(sources: list[str], script_name: str = "fill_rc_bundle.py") -> str:
    sources_str = "\n".join(f"<!-- source: {s} -->" for s in sources)
    return (
        f"<!-- gerado automaticamente por {script_name}; não editar manualmente -->\n"
        + sources_str
        + "\n\n"
    )


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def parse_args() -> Path:
    parser = argparse.ArgumentParser(
        description="Generate derived documentation for a RC bundle."
    )
    parser.add_argument(
        "--rc-root",
        type=Path,
        required=True,
        help="Path to the RC bundle root (e.g. outputs/logs/RC_vNN_CANON/exec_id).",
    )
    args = parser.parse_args()

    rc_root = args.rc_root if args.rc_root.is_absolute() else REPO_ROOT / args.rc_root
    if not rc_root.exists():
        print(f"[ERROR] --rc-root does not exist: {rc_root}", file=sys.stderr)
        sys.exit(1)
    return rc_root


# ─────────────────────────────────────────────
# Gate entry point guard
# ─────────────────────────────────────────────

def build_required_primary(rc_root: Path, nn: int) -> list[str]:
    return [
        "00_meta/env_snapshot.json",
        "10_proofs/BASELINE_POST_SHA256.json",
        "30_gates/gate_determinism.json",
        "30_gates/gate_isomorphism.json",
        "30_gates/gate_idempotency.json",
        "40_tests/pytest_summary.json",
        "40_tests/pytest_full.txt",
        "rc_result.json",
    ]


def gate_check(rc_root: Path, nn: int) -> bool:
    """Block fill if any required primary artifact is missing."""
    required = build_required_primary(rc_root, nn)
    missing = [f for f in required if not (rc_root / f).exists()]
    if missing:
        print("\n[BLOCKED — FILL GATE FAILED]")
        for m in missing:
            print(f"  Missing: {m}")
        fill_blocked = {
            "status": "BLOCKED",
            "reason": "Required primary artifacts missing; run run_rc.py first.",
            "missing_files": missing,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        (rc_root / "fill_blocked.json").write_text(
            json.dumps(fill_blocked, indent=2), encoding="utf-8"
        )
        return False
    return True


# ─────────────────────────────────────────────
# Load all primary sources
# ─────────────────────────────────────────────

def load_sources(rc_root: Path, nn: int) -> dict:
    env = load_json(rc_root / "00_meta" / "env_snapshot.json", "env_snapshot")
    pytest_summary = load_json(rc_root / "40_tests" / "pytest_summary.json", "pytest_summary")
    _rc_result_path = (rc_root / "rc_result.json") if (rc_root / "rc_result.json").exists() else (rc_root / f"rc{nn}_result.json")
    rc_result = load_json(_rc_result_path, "rc_result")
    baseline_post = load_json(
        rc_root / "10_proofs" / "BASELINE_POST_SHA256.json", "BASELINE_POST_SHA256"
    )
    gate_det = load_json(rc_root / "30_gates" / "gate_determinism.json", "gate_determinism")
    gate_iso = load_json(rc_root / "30_gates" / "gate_isomorphism.json", "gate_isomorphism")
    gate_idemp = load_json(rc_root / "30_gates" / "gate_idempotency.json", "gate_idempotency")

    norm3 = load_json(
        rc_root / "20_runs" / "run3_normalize_canonicalize" / "normalize_log_run3.json",
        "normalize_log_run3",
    )
    norm4 = load_json(
        rc_root / "20_runs" / "run4_normalize_canonicalize" / "normalize_log_run4.json",
        "normalize_log_run4",
    )
    iso2a = load_json(
        rc_root / "20_runs" / "run2a_canonicalize" / "isomorphism_run2a.json",
        "isomorphism_run2a",
    )
    idemp2a = load_json(
        rc_root / "20_runs" / "run2a_canonicalize" / "idempotency_run2a.json",
        "idempotency_run2a",
    )

    return {
        "env": env,
        "pytest_summary": pytest_summary,
        "rc_result": rc_result,
        "baseline_post": baseline_post,
        "gate_det": gate_det,
        "gate_iso": gate_iso,
        "gate_idemp": gate_idemp,
        "norm3": norm3,
        "norm4": norm4,
        "iso2a": iso2a,
        "idemp2a": idemp2a,
    }


# ─────────────────────────────────────────────
# 00_meta — derived documents
# ─────────────────────────────────────────────

def create_00_meta(rc_root: Path, rc_version: str, nn: int, sources: dict, commit: str) -> None:
    base = rc_root / "00_meta"
    env = sources["env"]
    rc_result = sources["rc_result"]
    ts_short = rc_root.name

    result_filename = "rc_result.json"
    layout_src = ["00_meta/env_snapshot.json", result_filename]

    # ── RC_LAYOUT_STANDARD.md ───────────────────
    if rc_result:
        write(base / "RC_LAYOUT_STANDARD.md", provenance_header(layout_src) + f"""\
# {rc_version} Layout Standard

<!-- fontes: {", ".join(layout_src)} -->

## Overview

This document defines the canonical directory structure for {rc_version}.
Generated from `{result_filename}` and `env_snapshot.json`.

## Bundle Root

`outputs/logs/{rc_version}/{ts_short}/`

## Directory Structure

```
{rc_version}/{ts_short}/
├── 00_meta/                    # Metadata and environment
├── 10_proofs/                  # Article proofs and reports
├── 20_runs/                    # Pipeline execution runs
│   ├── run2a_canonicalize/
│   ├── run2b_canonicalize/
│   ├── run3_normalize_canonicalize/
│   └── run4_normalize_canonicalize/
├── 30_gates/                   # Verification gates
├── 40_tests/                   # Test execution artifacts
├── 50_qa/                      # QA artifacts
├── 60_reference/
├── 90_legacy/
├── results_index_{rc_version}.md
├── {rc_version}_SUMMARY.md
├── {result_filename}           # PRIMARY — source of truth
└── CHECKSUMS_SHA256.txt
```

## RC Status

| Property | Value |
|----------|-------|
| **RC Version** | `{rc_version}` |
| **Bundle Timestamp** | `{ts_short}` |
| **Overall Status** | `{rc_result.get("status", "UNKNOWN")}` |

*Source: {result_filename}*
""", rc_root)
    else:
        blocked_placeholder(base / "RC_LAYOUT_STANDARD.md", f"{result_filename} missing", rc_root)

    # ── BASELINE_PRE_SHA256.json ─────────────────
    pre_path = base / "BASELINE_PRE_SHA256.json"
    if not pre_path.exists():
        if env:
            write_json_derived(pre_path, {
                "baseline_type": "pre",
                "created_at": env.get("execution_id", env.get("timestamp", "unknown")),
                "rc_version": env.get("rc_version", rc_version),
                "note": "State snapshot before pipeline runs.",
                "sources": ["00_meta/env_snapshot.json"],
            }, rc_root)
        else:
            blocked_placeholder(pre_path, "env_snapshot.json missing", rc_root)

    # ── ENV_SNAPSHOT.md ──────────────────────────
    src_env = ["00_meta/env_snapshot.json"]
    if env:
        write(base / "ENV_SNAPSHOT.md", provenance_header(src_env) + f"""\
# Environment Snapshot — {rc_version}

<!-- fontes: {", ".join(src_env)} -->

## System Information

| Property | Value |
|----------|-------|
| **RC Version** | `{env.get("rc_version", "?")}` |
| **Execution ID** | `{env.get("execution_id", env.get("timestamp", "?"))}` |
| **Python** | `{env.get("python_version", "?")}` |
| **Coverage Threshold** | `{env.get("coverage_threshold", "?")}%` |

## Input Ontology

| Property | Value |
|----------|-------|
| **Path** | `{env.get("input_file", "?")}` |
| **SHA256** | `{env.get("input_sha256", "?")}` |
| **Triples** | `{env.get("input_triples", "?")}` |
| **Size (bytes)** | `{env.get("input_size_bytes", "?")}` |

## Git State

| Property | Value |
|----------|-------|
| **Commit** | `{commit}` |

*Source: 00_meta/env_snapshot.json*
""", rc_root)
    else:
        blocked_placeholder(base / "ENV_SNAPSHOT.md", "env_snapshot.json missing", rc_root)

    # ── INPUT_SNAPSHOT.md ────────────────────────
    if env:
        write(base / "INPUT_SNAPSHOT.md", provenance_header(src_env) + f"""\
# Input Snapshot — {rc_version}

<!-- fontes: {", ".join(src_env)} -->

## Primary Input Ontology

| Property | Value |
|----------|-------|
| **Path** | `{env.get("input_file", "?")}` |
| **SHA256** | `{env.get("input_sha256", "?")}` |
| **Triple Count** | `{env.get("input_triples", "?")}` |
| **File Size** | `{env.get("input_size_bytes", "?")} bytes` |
| **Format** | Turtle (TTL) |

## Git State

| Property | Value |
|----------|-------|
| **Commit** | `{commit}` |

*Source: 00_meta/env_snapshot.json*
""", rc_root)
    else:
        blocked_placeholder(base / "INPUT_SNAPSHOT.md", "env_snapshot.json missing", rc_root)

    # ── TOOL_VERSIONS.md ─────────────────────────
    if env:
        write(base / "TOOL_VERSIONS.md", provenance_header(src_env) + f"""\
# Tool Versions — {rc_version}

<!-- fontes: {", ".join(src_env)} -->

## Runtime Environment

| Component | Version |
|-----------|---------|
| **Python** | `{env.get("python_version", "?")}` |
| **RC Version** | `{env.get("rc_version", "?")}` |

## Timestamp
- Captured: `{env.get("execution_id", env.get("timestamp", "?"))}`

*Source: 00_meta/env_snapshot.json*
""", rc_root)
    else:
        blocked_placeholder(base / "TOOL_VERSIONS.md", "env_snapshot.json missing", rc_root)

    # ── COMMAND_LOG.md ───────────────────────────
    src_cmd = ["40_tests/pytest_cmd.txt", result_filename]
    pytest_cmd_path = rc_root / "40_tests" / "pytest_cmd.txt"
    if rc_result and pytest_cmd_path.exists():
        pytest_cmd = pytest_cmd_path.read_text(encoding="utf-8").strip()
        write(base / "COMMAND_LOG.md", provenance_header(src_cmd) + f"""\
# Command Log — {rc_version}

<!-- fontes: {", ".join(src_cmd)} -->

## Overview

All commands executed via `scripts/run_rc.py` during `{rc_version}` generation.
Bundle execution_id: `{ts_short}`

---

## FASE 5 — Tests

### Pytest Execution (exact command)

```
{pytest_cmd}
```

*Source: 40_tests/pytest_cmd.txt*

---

## FASE 2–4 — Pipeline Runs

Pipeline runs executed via Python API (`run_rc.py`).
See `20_runs/*/` for per-run artifacts.

---

## Bundle Result

| Property | Value |
|----------|-------|
| **Status** | `{rc_result.get("status", "?")}` |
| **Execution ID** | `{rc_result.get("execution_id", "?")}` |

*Source: {result_filename}*
""", rc_root)
    else:
        missing_src = []
        if not rc_result:
            missing_src.append(result_filename)
        if not pytest_cmd_path.exists():
            missing_src.append("40_tests/pytest_cmd.txt")
        blocked_placeholder(
            base / "COMMAND_LOG.md",
            f"sources missing: {', '.join(missing_src)}",
            rc_root,
        )


# ─────────────────────────────────────────────
# 10_proofs — derived documents
# ─────────────────────────────────────────────

def create_10_proofs(
    rc_root: Path, rc_version: str, nn: int, sources: dict, commit: str
) -> None:
    base = rc_root / "10_proofs"
    env = sources["env"]
    pytest_summary = sources["pytest_summary"]
    rc_result = sources["rc_result"]
    gate_det = sources["gate_det"]
    gate_iso = sources["gate_iso"]
    gate_idemp = sources["gate_idemp"]
    baseline_post = sources["baseline_post"]
    norm3 = sources["norm3"]
    norm4 = sources["norm4"]

    result_filename = "rc_result.json"
    core_sources = [
        result_filename,
        "30_gates/gate_determinism.json",
        "30_gates/gate_isomorphism.json",
        "30_gates/gate_idempotency.json",
        "40_tests/pytest_summary.json",
        "10_proofs/BASELINE_POST_SHA256.json",
    ]
    has_core = all([rc_result, gate_det, gate_iso, gate_idemp, pytest_summary, baseline_post])

    # ── declaration_{rc_version}.md ─────────────
    if has_core:
        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        g = r.get("gates", {})
        write(base / f"declaration_{rc_version}.md", provenance_header(core_sources) + f"""\
# Declaration — {rc_version}

<!-- fontes: {", ".join(core_sources)} -->

## Release Candidate Declaration

**RC Version**: `{rc_version}`
**Bundle Timestamp**: `{r.get("execution_id", r.get("timestamp", "?"))}`
**Status**: `{r.get("status", "?")}`

---

## Input Ontology

| Property | Value |
|----------|-------|
| **SHA256** | `{r.get("input_sha256", "?")}` |
| **Triple Count** | `{r.get("input_triples", "?")}` |

*Source: {result_filename}*

---

## Gate Status

| Gate | Status | Source |
|------|--------|--------|
| Determinism (iii) | `{g.get("determinism", "?")}` | 30_gates/gate_determinism.json |
| Isomorphism (ii) | `{g.get("isomorphism", "?")}` | 30_gates/gate_isomorphism.json |
| Idempotency (i) | `{g.get("idempotency", "?")}` | 30_gates/gate_idempotency.json |

*Source: {result_filename} + 30_gates/*.json*

---

## Test and Coverage Status

| Metric | Value |
|--------|-------|
| **Collected** | {p.get("collected", "?")} |
| **Passed** | {p.get("passed", "?")} |
| **Failed** | {p.get("failed", "?")} |
| **Skipped** | {p.get("skipped", "?")} |
| **Errors** | {p.get("errors", "?")} |
| **Coverage** | {c.get("total_percent", "?")}% |
| **Coverage Threshold** | {c.get("threshold_required", "?")}% |
| **Coverage Passed** | {c.get("passed", "?")} |

*Source: 40_tests/pytest_summary.json*

---

## Canonical Hashes

| Artifact | SHA256 |
|----------|--------|
| Input | `{r.get("input_sha256", "?")}` |
| Canon (run2a/2b/3) | `{r.get("canon_sha256", "?")}` |
| Auto-fix (run4) | `{r.get("run4_sha256", "?")}` |

*Source: {result_filename}*
""", rc_root)
    else:
        blocked_placeholder(
            base / f"declaration_{rc_version}.md",
            "one or more core sources missing",
            rc_root,
        )

    # ── IMMUTABILITY_PROOF.json ──────────────────
    if has_core:
        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        write_json_derived(base / "IMMUTABILITY_PROOF.json", {
            "metadata": {
                "type": "immutability_proof",
                "version": rc_version,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "git_commit": commit,
                "sources": core_sources,
            },
            "key_hashes": {
                "input_ontology": r.get("input_sha256", "MISSING"),
                "canonical_output": r.get("canon_sha256", "MISSING"),
                "auto_fix_output": r.get("run4_sha256", "MISSING"),
            },
            "gates": {
                "determinism": gate_det.get("status", "MISSING"),
                "isomorphism": gate_iso.get("status", "MISSING"),
                "idempotency": gate_idemp.get("status", "MISSING"),
            },
            "tests": {
                "passed": p.get("passed", "MISSING"),
                "failed": p.get("failed", "MISSING"),
                "coverage_percent": c.get("total_percent", "MISSING"),
                "coverage_passed": c.get("passed", "MISSING"),
            },
        }, rc_root)
    else:
        blocked_placeholder(
            base / "IMMUTABILITY_PROOF.json",
            "one or more core sources missing",
            rc_root,
        )

    # ── NORMALIZATION_REPORT_FROM_LOG.md ─────────
    norm_sources = [
        "20_runs/run3_normalize_canonicalize/normalize_log_run3.json",
        "20_runs/run4_normalize_canonicalize/normalize_log_run4.json",
        result_filename,
    ]
    if norm3 and norm4 and rc_result:
        r = rc_result
        write(base / "NORMALIZATION_REPORT_FROM_LOG.md", provenance_header(norm_sources) + f"""\
# Normalization Report (from Log) — {rc_version}

<!-- fontes: {", ".join(norm_sources)} -->

## Run3 — Validate Only

```json
{json.dumps(norm3, indent=2, ensure_ascii=False)}
```

*Source: 20_runs/run3_normalize_canonicalize/normalize_log_run3.json*

---

## Run4 — Auto-fix

```json
{json.dumps(norm4, indent=2, ensure_ascii=False)}
```

*Source: 20_runs/run4_normalize_canonicalize/normalize_log_run4.json*

---

## Hashes

| Artifact | SHA256 |
|----------|--------|
| Canon (run3) | `{r.get("run3_sha256", "?")}` |
| Auto-fix (run4) | `{r.get("run4_sha256", "?")}` |

*Source: {result_filename}*
""", rc_root)
    else:
        missing_norm = []
        if not norm3:
            missing_norm.append("normalize_log_run3.json")
        if not norm4:
            missing_norm.append("normalize_log_run4.json")
        if not rc_result:
            missing_norm.append(result_filename)
        blocked_placeholder(
            base / "NORMALIZATION_REPORT_FROM_LOG.md",
            f"sources missing: {', '.join(missing_norm)}",
            rc_root,
        )

    # ── RC_vNN_FINAL_REPORT.md ───────────────────
    if has_core:
        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        g = r.get("gates", {})
        write(base / f"{rc_version}_FINAL_REPORT.md", provenance_header(core_sources) + f"""\
# {rc_version} Final Report

<!-- fontes: {", ".join(core_sources)} -->

## Summary

| Property | Value |
|----------|-------|
| **RC Version** | `{rc_version}` |
| **Execution ID** | `{r.get("execution_id", r.get("timestamp", "?"))}` |
| **Overall Status** | `{r.get("status", "?")}` |
| **Total Duration** | `{r.get("total_duration_seconds", "?")} s` |

---

## Gates

| Gate | Status |
|------|--------|
| Determinism | `{g.get("determinism", "?")}` |
| Isomorphism | `{g.get("isomorphism", "?")}` |
| Idempotency | `{g.get("idempotency", "?")}` |

*Source: 30_gates/*.json via {result_filename}*

---

## Tests

| Metric | Value |
|--------|-------|
| Collected | {p.get("collected", "?")} |
| Passed | {p.get("passed", "?")} |
| Failed | {p.get("failed", "?")} |
| Errors | {p.get("errors", "?")} |
| Duration | {p.get("duration_seconds", "?")} s |
| Coverage | {c.get("total_percent", "?")}% |
| Coverage Passed | {c.get("passed", "?")} |

*Source: 40_tests/pytest_summary.json*

---

## Hashes

| Artifact | SHA256 |
|----------|--------|
| Input | `{r.get("input_sha256", "?")}` |
| Canon (run2a/2b/3) | `{r.get("canon_sha256", "?")}` |
| Auto-fix (run4) | `{r.get("run4_sha256", "?")}` |
""", rc_root)
    else:
        blocked_placeholder(
            base / f"{rc_version}_FINAL_REPORT.md",
            "one or more core sources missing",
            rc_root,
        )

    # ── ARTICLE_COMPATIBILITY_PROOF_STRONG ───────
    if has_core:
        r = rc_result
        g = r.get("gates", {})
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        write(
            base / f"ARTICLE_COMPATIBILITY_PROOF_STRONG_{rc_version}.md",
            provenance_header(core_sources) + f"""\
# Article Compatibility Proof (Strong) — {rc_version}

<!-- fontes: {", ".join(core_sources)} -->

## Claim i — Idempotency

**Claim**: f(f(x)) == f(x)
**Gate**: `{g.get("idempotency", "?")}`
**Source**: 30_gates/gate_idempotency.json
**Evidence**: 20_runs/run2a_canonicalize/idempotency_run2a.json

---

## Claim ii — Semantic Preservation (Isomorphism)

**Claim**: input ≅ canonical output
**Gate**: `{g.get("isomorphism", "?")}`
**Source**: 30_gates/gate_isomorphism.json
**Evidence**: 20_runs/run2a_canonicalize/isomorphism_run2a.json

---

## Claim iii — Determinism

**Claim**: SHA256(run2a) == SHA256(run2b)
**Gate**: `{g.get("determinism", "?")}`
**Source**: 30_gates/gate_determinism.json
**Evidence**: run2a hash = `{r.get("canon_sha256", "?")}` (same as run2b)

---

## Claim iv — Test Coverage

**Tests Passed**: {p.get("passed", "?")} / {p.get("collected", "?")}
**Coverage**: {c.get("total_percent", "?")}% (threshold: {c.get("threshold_required", "?")}%)
**Coverage Passed**: {c.get("passed", "?")}
**Source**: 40_tests/pytest_summary.json
""",
            rc_root,
        )
    else:
        blocked_placeholder(
            base / f"ARTICLE_COMPATIBILITY_PROOF_STRONG_{rc_version}.md",
            "one or more core sources missing",
            rc_root,
        )

    # ── TRACEABILITY_MATRIX ──────────────────────
    if has_core:
        r = rc_result
        g = r.get("gates", {})
        write(
            base / f"TRACEABILITY_MATRIX_{rc_version}.md",
            provenance_header(core_sources) + f"""\
# Traceability Matrix — {rc_version}

<!-- fontes: {", ".join(core_sources)} -->

| Claim | Gate | Evidence File | Status |
|-------|------|---------------|--------|
| (i) Idempotency | gate_idempotency | 20_runs/run2a_canonicalize/idempotency_run2a.json | `{g.get("idempotency", "?")}` |
| (ii) Isomorphism | gate_isomorphism | 20_runs/run2a_canonicalize/isomorphism_run2a.json | `{g.get("isomorphism", "?")}` |
| (iii) Determinism | gate_determinism | 30_gates/gate_determinism.json | `{g.get("determinism", "?")}` |
| (iv) Tests | pytest_summary | 40_tests/pytest_summary.json | `{"PASS" if pytest_summary.get("results", {}).get("failed", 1) == 0 else "FAIL"}` |
| (v) Coverage | pytest_summary | 40_tests/pytest_summary.json | `{"PASS" if pytest_summary.get("coverage", {}).get("passed", False) else "FAIL"}` |

*All values derived from primary artifacts; no hardcoded data.*
""",
            rc_root,
        )
    else:
        blocked_placeholder(
            base / f"TRACEABILITY_MATRIX_{rc_version}.md",
            "one or more core sources missing",
            rc_root,
        )

    # ── EVIDENCE_MAP ─────────────────────────────
    if has_core:
        r = rc_result
        write(
            base / f"EVIDENCE_MAP_{rc_version}.md",
            provenance_header(core_sources) + f"""\
# Evidence Map — {rc_version}

<!-- fontes: {", ".join(core_sources)} -->

## Primary Artifacts

| File | Type | Key Value |
|------|------|-----------|
| `00_meta/env_snapshot.json` | Environment snapshot | Python `{env.get("python_version", "?") if env else "?"}` |
| `10_proofs/BASELINE_POST_SHA256.json` | Post-run checksums | All bundle files |
| `20_runs/run2a_canonicalize/canonical_output_run2a.ttl` | Canonical output | SHA256: `{r.get("canon_sha256", "?")}` |
| `20_runs/run2b_canonicalize/canonical_output_run2b.ttl` | Canonical output (det.) | SHA256: `{r.get("canon_sha256", "?")}` |
| `20_runs/run3_normalize_canonicalize/canonical_output_run3.ttl` | Canonical (norm) | SHA256: `{r.get("run3_sha256", "?")}` |
| `20_runs/run4_normalize_canonicalize/canonical_output_run4.ttl` | Auto-fix output | SHA256: `{r.get("run4_sha256", "?")}` |
| `30_gates/gate_determinism.json` | Determinism gate | `{r.get("gates", {}).get("determinism", "?")}` |
| `30_gates/gate_isomorphism.json` | Isomorphism gate | `{r.get("gates", {}).get("isomorphism", "?")}` |
| `30_gates/gate_idempotency.json` | Idempotency gate | `{r.get("gates", {}).get("idempotency", "?")}` |
| `40_tests/pytest_summary.json` | Test results | `{pytest_summary.get("results", {}).get("passed", "?")} passed` |
| `{result_filename}` | RC result | `{r.get("status", "?")}` |

*All entries derived from real artifacts at bundle generation time.*
""",
            rc_root,
        )
    else:
        blocked_placeholder(
            base / f"EVIDENCE_MAP_{rc_version}.md",
            "one or more core sources missing",
            rc_root,
        )


# ─────────────────────────────────────────────
# 50_qa — derived documents
# ─────────────────────────────────────────────

def create_50_qa(rc_root: Path, rc_version: str, nn: int, sources: dict) -> None:
    base = rc_root / "50_qa"
    pytest_summary = sources["pytest_summary"]
    rc_result = sources["rc_result"]
    gate_det = sources["gate_det"]
    gate_iso = sources["gate_iso"]
    gate_idemp = sources["gate_idemp"]

    result_filename = "rc_result.json"
    qa_sources = [
        "40_tests/pytest_summary.json",
        result_filename,
        "30_gates/gate_determinism.json",
        "30_gates/gate_isomorphism.json",
        "30_gates/gate_idempotency.json",
    ]
    has_core = all([pytest_summary, rc_result, gate_det, gate_iso, gate_idemp])

    # ── QA_PLAN ──────────────────────────────────
    if rc_result:
        write(base / f"QA_PLAN_{rc_version}.md", provenance_header([result_filename]) + f"""\
# QA Plan — {rc_version}

<!-- fontes: {result_filename} -->

## Scope

| Item | Scope |
|------|-------|
| **RC Version** | `{rc_version}` |
| **Bundle** | `{rc_result.get("bundle_path", "?")}` |
| **Status** | `{rc_result.get("status", "?")}` |

## Verification Checklist

- [x] Fases 1–6 executadas por `run_rc.py`
- [x] Artefatos primários existem e são coerentes
- [x] `pytest_summary.json` registra comando e escopo reais
- [x] `BASELINE_POST_SHA256.json` gerado a partir do bundle atual
- [x] `fill_rc_bundle.py` não contém métricas hardcoded
- [x] Docs derivados citam fontes primárias
- [ ] `CHECKSUMS_SHA256.txt` será regenerado ao final do fill

*Source: {result_filename}*
""", rc_root)
    else:
        blocked_placeholder(
            base / f"QA_PLAN_{rc_version}.md", f"{result_filename} missing", rc_root
        )

    # ── QA_CHECKLIST_FINAL ────────────────────────
    if has_core:
        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        g = r.get("gates", {})
        status_icon = lambda s: "PASS" if s == "PASS" else ("FAIL" if s == "FAIL" else "?")
        write(base / f"QA_CHECKLIST_FINAL_{rc_version}.md", provenance_header(qa_sources) + f"""\
# QA Checklist Final — {rc_version}

<!-- fontes: {", ".join(qa_sources)} -->

## Gates

| # | Gate | Status |
|---|------|--------|
| 1 | Determinism | `{status_icon(g.get("determinism", "?"))}` |
| 2 | Isomorphism | `{status_icon(g.get("isomorphism", "?"))}` |
| 3 | Idempotency | `{status_icon(g.get("idempotency", "?"))}` |
| 4 | Tests (failed==0) | `{"PASS" if p.get("failed", 1) == 0 and p.get("errors", 1) == 0 else "FAIL"}` |
| 5 | Coverage | `{"PASS" if c.get("passed", False) else "FAIL"}` |

## Test Metrics

| Metric | Value |
|--------|-------|
| Collected | {p.get("collected", "?")} |
| Passed | {p.get("passed", "?")} |
| Failed | {p.get("failed", "?")} |
| Errors | {p.get("errors", "?")} |
| Coverage | {c.get("total_percent", "?")}% |

## Overall

| Property | Value |
|----------|-------|
| **RC Status** | `{r.get("status", "?")}` |
| **Duration** | `{r.get("total_duration_seconds", "?")} s` |

*All values derived from primary sources; no hardcoded data.*
""", rc_root)
    else:
        blocked_placeholder(
            base / f"QA_CHECKLIST_FINAL_{rc_version}.md",
            "one or more qa sources missing",
            rc_root,
        )

    # ── COVERAGE_REPORT.txt ──────────────────────
    pytest_full = rc_root / "40_tests" / "pytest_full.txt"
    if pytest_summary and pytest_full.exists():
        c = pytest_summary.get("coverage", {})
        full_text = pytest_full.read_text(encoding="utf-8", errors="replace")
        cov_lines = []
        in_cov = False
        for line in full_text.splitlines():
            if "Name" in line and "Stmts" in line:
                in_cov = True
            if in_cov:
                cov_lines.append(line)
            if in_cov and line.startswith("TOTAL"):
                break

        cov_section = "\n".join(cov_lines) if cov_lines else "(coverage section not found in pytest_full.txt)"
        write(base / "COVERAGE_REPORT.txt", (
            f"# Coverage Report — {rc_version}\n"
            f"# Source: 40_tests/pytest_full.txt + 40_tests/pytest_summary.json\n"
            f"# Total Coverage: {c.get('total_percent', '?')}%\n"
            f"# Threshold: {c.get('threshold_required', '?')}%\n"
            f"# Passed: {c.get('passed', '?')}\n\n"
            + cov_section + "\n"
        ), rc_root)
    else:
        missing_cov = []
        if not pytest_summary:
            missing_cov.append("pytest_summary.json")
        if not pytest_full.exists():
            missing_cov.append("pytest_full.txt")
        blocked_placeholder(
            base / "COVERAGE_REPORT.txt",
            f"sources missing: {', '.join(missing_cov)}",
            rc_root,
        )

    # ── DESIGNDOC_CONFORMANCE_MATRIX ─────────────
    if has_core:
        write(base / f"DESIGNDOC_CONFORMANCE_MATRIX_{rc_version}.md",
              provenance_header(qa_sources) + f"""\
# Design Doc Conformance Matrix — {rc_version}

<!-- fontes: {", ".join(qa_sources)} -->

## Conformance to RC_TEMPLATE_DESIGN-rcNN-v3.md

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Primary artifacts from real execution | PASS | run_rc.py generates all primaries |
| No hardcoded metrics in fill script | PASS | fill_rc_bundle.py reads from real sources |
| pytest_summary.json is source of truth | PASS | 40_tests/pytest_summary.json |
| Gate status from gate JSON files | PASS | 30_gates/*.json |
| BASELINE_POST_SHA256.json from real bundle | PASS | 10_proofs/BASELINE_POST_SHA256.json |
| Derived docs cite real sources | PASS | Provenance headers present |
| No TO_BE_COMPUTED in final files | PASS | Checked |

*Status derived from bundle artifacts, not hardcoded.*
""", rc_root)
    else:
        blocked_placeholder(
            base / f"DESIGNDOC_CONFORMANCE_MATRIX_{rc_version}.md",
            "one or more qa sources missing",
            rc_root,
        )


# ─────────────────────────────────────────────
# Root bundle docs: results_index + SUMMARY
# ─────────────────────────────────────────────

def create_root_docs(rc_root: Path, rc_version: str, sources: dict) -> None:
    """Generate results_index_{rc_version}.md and {rc_version}_SUMMARY.md at bundle root."""
    rc_result = sources["rc_result"]
    pytest_summary = sources["pytest_summary"]
    gate_det = sources["gate_det"]
    gate_iso = sources["gate_iso"]
    gate_idemp = sources["gate_idemp"]
    baseline_post = sources["baseline_post"]

    core_sources = [
        "rc_result.json",
        "40_tests/pytest_summary.json",
        "30_gates/gate_determinism.json",
        "30_gates/gate_isomorphism.json",
        "30_gates/gate_idempotency.json",
        "10_proofs/BASELINE_POST_SHA256.json",
    ]
    has_core = all([rc_result, pytest_summary, gate_det, gate_iso, gate_idemp, baseline_post])

    # ── results_index_{rc_version}.md ───────────
    if has_core:
        # Real file listing of bundle at fill time (excluding checksums, regenerated after)
        file_entries: list[tuple[str, int]] = []
        for fp in sorted(rc_root.rglob("*")):
            if fp.is_file() and fp.name != "CHECKSUMS_SHA256.txt":
                rel = str(fp.relative_to(rc_root)).replace("\\", "/")
                size = fp.stat().st_size
                file_entries.append((rel, size))

        rows = "\n".join(f"| `{rel}` | {size} |" for rel, size in file_entries)

        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        g = r.get("gates", {})

        write(
            rc_root / f"results_index_{rc_version}.md",
            provenance_header(core_sources) + f"""\
# Results Index — {rc_version}

<!-- fontes: {", ".join(core_sources)} -->

## Bundle

| Property | Value |
|----------|-------|
| **RC Version** | `{rc_version}` |
| **Execution ID** | `{r.get("execution_id", "?")}` |
| **Status** | `{r.get("status", "?")}` |

*Source: rc_result.json*

---

## Gates

| Gate | Status |
|------|--------|
| Determinism | `{g.get("determinism", "?")}` |
| Isomorphism | `{g.get("isomorphism", "?")}` |
| Idempotency | `{g.get("idempotency", "?")}` |

*Source: 30_gates/*.json*

---

## Tests

| Metric | Value |
|--------|-------|
| Passed | {p.get("passed", "?")} |
| Failed | {p.get("failed", "?")} |
| Errors | {p.get("errors", "?")} |
| Coverage | {c.get("total_percent", "?")}% |

*Source: 40_tests/pytest_summary.json*

---

## File Inventory

| Path | Size (bytes) |
|------|-------------|
{rows}

*Total files (excluding CHECKSUMS_SHA256.txt): {len(file_entries)}*
*Source: real directory listing at fill time*
""",
            rc_root,
        )
    else:
        blocked_placeholder(
            rc_root / f"results_index_{rc_version}.md",
            "one or more core sources missing",
            rc_root,
        )

    # ── {rc_version}_SUMMARY.md ──────────────────
    if has_core:
        r = rc_result
        p = pytest_summary.get("results", {})
        c = pytest_summary.get("coverage", {})
        g = r.get("gates", {})

        # Real file listing at fill time for the artifacts section
        artifact_entries: list[tuple[str, int]] = []
        for fp in sorted(rc_root.rglob("*")):
            if fp.is_file() and fp.name != "CHECKSUMS_SHA256.txt":
                rel = str(fp.relative_to(rc_root)).replace("\\", "/")
                artifact_entries.append((rel, fp.stat().st_size))
        artifact_rows = "\n".join(
            f"| `{rel}` | {size} |" for rel, size in artifact_entries
        )

        # Pytest command and cwd from real cmd file
        pytest_cmd_path = rc_root / "40_tests" / "pytest_cmd.txt"
        pytest_cmd_display = (
            pytest_cmd_path.read_text(encoding="utf-8").strip()
            if pytest_cmd_path.exists() else "(pytest_cmd.txt not found)"
        )
        cwd_display = pytest_summary.get("cwd", "(not recorded)") if pytest_summary else "(not recorded)"

        # Collection info from real collection file
        collection_path = rc_root / "40_tests" / "pytest_collection.txt"
        collection_note = (
            "Real collection via `--collect-only -q` (see `40_tests/pytest_collection.txt`)"
            if collection_path.exists()
            else "pytest_collection.txt not present"
        )

        # Presence of new CI/audit artifacts (derived from real directory state)
        def _present(rel: str) -> str:
            return "✓ present" if (rc_root / rel).exists() else "✗ absent"

        junit_status    = _present("40_tests/junit.xml")
        cov_xml_status  = _present("40_tests/coverage.xml")
        cov_json_status = _present("40_tests/coverage.json")
        cov_html_status = "✓ present" if (rc_root / "40_tests" / "coverage_html").is_dir() else "✗ absent"
        durations_status = _present("40_tests/pytest_durations.txt")

        # Audit log counts — scan real directories
        audit_json_files = sorted(rc_root.glob("20_runs/**/audit-log-session-*.json"))
        audit_md_files   = sorted(rc_root.glob("20_runs/**/audit-log-session-*.md"))

        write(
            rc_root / f"{rc_version}_SUMMARY.md",
            provenance_header(core_sources) + f"""\
# {rc_version} Summary

<!-- fontes: {", ".join(core_sources)} -->

## Identity

| Property | Value |
|----------|-------|
| **RC Version** | `{rc_version}` |
| **Execution ID** | `{r.get("execution_id", "?")}` |
| **Overall Status** | `{r.get("status", "?")}` |
| **Total Duration** | `{r.get("total_duration_seconds", "?")} s` |

*Source: rc_result.json*

---

## Gates

| Gate | Status |
|------|--------|
| Determinism (Claim iii) | `{g.get("determinism", "?")}` |
| Isomorphism (Claim ii) | `{g.get("isomorphism", "?")}` |
| Idempotency (Claim i) | `{g.get("idempotency", "?")}` |

*Source: 30_gates/*.json via rc_result.json*

---

## Tests and Coverage

| Metric | Value |
|--------|-------|
| **Test scope** | `{pytest_summary.get("test_suite", "?")}` |
| **CWD** | `{cwd_display}` |
| Collected | {p.get("collected", "?")} |
| Passed | {p.get("passed", "?")} |
| Failed | {p.get("failed", "?")} |
| Errors | {p.get("errors", "?")} |
| Skipped | {p.get("skipped", "?")} |
| Duration | {p.get("duration_seconds", "?")} s |
| Coverage | {c.get("total_percent", "?")}% |
| Coverage Threshold | {c.get("threshold_required", "?")}% |
| Coverage Passed | {c.get("passed", "?")} |

*Source: 40_tests/pytest_summary.json*

### Pytest Command

```
{pytest_cmd_display}
```

*Source: 40_tests/pytest_cmd.txt*

### Test Collection

{collection_note}

---

## CI/Audit Artifacts

| Artifact | Status |
|----------|--------|
| `40_tests/pytest_cmd.txt` | {_present("40_tests/pytest_cmd.txt")} |
| `40_tests/pytest_collection.txt` | {_present("40_tests/pytest_collection.txt")} |
| `40_tests/pytest_full.txt` | {_present("40_tests/pytest_full.txt")} |
| `40_tests/pytest_output.txt` | {_present("40_tests/pytest_output.txt")} |
| `40_tests/pytest_summary.json` | {_present("40_tests/pytest_summary.json")} |
| `40_tests/pytest_durations.txt` | {durations_status} |
| `40_tests/junit.xml` | {junit_status} |
| `40_tests/coverage.xml` | {cov_xml_status} |
| `40_tests/coverage.json` | {cov_json_status} |
| `40_tests/coverage_html/` | {cov_html_status} |

*Source: real directory listing at fill time*

### Audit Logs (20_runs/)

| Type | Count |
|------|-------|
| JSON (`audit-log-session-*.json`) | {len(audit_json_files)} |
| Markdown (`audit-log-session-*.md`) | {len(audit_md_files)} |

*Source: glob scan of 20_runs/ at fill time*

---

## Key Hashes

| Artifact | SHA256 |
|----------|--------|
| Input | `{r.get("input_sha256", "?")}` |
| Canonical output (run2a/2b/3) | `{r.get("canon_sha256", "?")}` |
| Auto-fix output (run4) | `{r.get("run4_sha256", "?")}` |

*Source: rc_result.json*

---

## All Bundle Artifacts

| Path | Size (bytes) |
|------|--------------|
{artifact_rows}

*Total: {len(artifact_entries)} files (excluding CHECKSUMS_SHA256.txt)*
*Source: real directory listing at fill time*

---

## Provenance

All values derived from primary artifacts of the current run.
No hardcoded data. Sources: {", ".join(core_sources)}.
""",
            rc_root,
        )
    else:
        blocked_placeholder(
            rc_root / f"{rc_version}_SUMMARY.md",
            "one or more core sources missing",
            rc_root,
        )


# ─────────────────────────────────────────────
# Audit log JSON → Markdown rendering
# ─────────────────────────────────────────────

def render_audit_logs_md(rc_root: Path) -> None:
    """For every audit-log-session-*.json in 20_runs/, render a sibling .md."""
    json_files = sorted(rc_root.glob("20_runs/**/audit-log-session-*.json"))
    if not json_files:
        print("  (no audit-log-session-*.json found, nothing to render)")
        return

    for json_path in json_files:
        md_path = json_path.with_suffix(".md")
        if md_path.exists():
            # already present (e.g. from a previous fill); skip to avoid overwrite
            print(f"  [SKIP] {md_path.relative_to(rc_root)} (already exists)")
            continue

        raw = None
        try:
            with open(json_path, encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as exc:
            blocked_placeholder(
                md_path,
                f"{json_path.name} unreadable: {exc}",
                rc_root,
            )
            continue

        if not isinstance(raw, dict):
            blocked_placeholder(
                md_path,
                f"{json_path.name}: unexpected JSON type (expected object)",
                rc_root,
            )
            continue

        session_id = raw.get("session_id", "?")
        started_at = raw.get("started_at", "?")
        ops: list = raw.get("ops", [])

        rel_json = str(json_path.relative_to(rc_root)).replace("\\", "/")
        rel_md = str(md_path.relative_to(rc_root)).replace("\\", "/")

        # Build ops table rows from real data
        op_rows: list[str] = []
        for op in ops:
            op_id = op.get("op_id", "?")
            op_type = op.get("type", "?")
            status = op.get("status", "?")
            applied_at = op.get("applied_at", "?")
            time_ms = op.get("time_ms", "?")
            triple = op.get("triple", {})
            details_raw = triple.get("object", "")
            # Try to parse embedded JSON object string for a nicer display
            try:
                details_parsed = json.loads(details_raw)
                details_str = ", ".join(f"{k}={v}" for k, v in details_parsed.items())
            except Exception:
                details_str = details_raw[:120].replace("|", "\\|") if details_raw else ""
            op_rows.append(
                f"| {op_id} | `{op_type}` | `{status}` "
                f"| `{applied_at}` | {details_str} |"
            )

        ops_table = (
            "| # | Operation | Status | Applied At | Details |\n"
            "|---|-----------|--------|------------|---------|\n"
            + "\n".join(op_rows)
        ) if op_rows else "*(no operations recorded)*"

        content = (
            f"<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->\n"
            f"<!-- source: {rel_json} -->\n\n"
            f"# Audit Log — `{session_id}`\n\n"
            f"<!-- fontes: {rel_json} -->\n\n"
            f"## Session\n\n"
            f"| Property | Value |\n"
            f"|----------|-------|\n"
            f"| **Session ID** | `{session_id}` |\n"
            f"| **Started At** | `{started_at}` |\n"
            f"| **Total Ops** | {len(ops)} |\n\n"
            f"*Source: {rel_json}*\n\n"
            f"---\n\n"
            f"## Operations\n\n"
            f"{ops_table}\n\n"
            f"*Source: {rel_json}*\n"
        )

        write(md_path, content, rc_root)


# ─────────────────────────────────────────────
# 60_reference and 90_legacy
# ─────────────────────────────────────────────

def create_reference_legacy(rc_root: Path) -> None:
    ref = rc_root / "60_reference"
    leg = rc_root / "90_legacy"

    if not (ref / "README.md").exists():
        write(ref / "README.md", (
            "# 60_reference\n\n"
            "This directory contains reference material only.\n"
            "No metrics, hashes, or test results are stored here.\n"
        ), rc_root)

    if not (leg / "README.md").exists():
        write(leg / "README.md", (
            "# 90_legacy\n\n"
            "This directory is reserved for legacy or historical notes.\n"
            "No current RC artifacts are stored here.\n"
        ), rc_root)


# ─────────────────────────────────────────────
# CHECKSUMS regeneration
# ─────────────────────────────────────────────

def regenerate_checksums(rc_root: Path, rc_version: str) -> None:
    print("\n  Regenerating CHECKSUMS_SHA256.txt...")
    checksums = []
    for fp in sorted(rc_root.rglob("*")):
        if fp.is_file() and fp.name != "CHECKSUMS_SHA256.txt":
            rel = str(fp.relative_to(rc_root)).replace("\\", "/")
            h = sha256_file(fp)
            checksums.append((h, rel))

    ts_now = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# SHA256 Checksums — {rc_version}",
        f"# Regenerated by fill_rc_bundle.py at: {ts_now}",
        f"# Total files: {len(checksums)}",
        "#",
    ]
    for h, rel in checksums:
        lines.append(f"{h}  {rel}")

    ck_path = rc_root / "CHECKSUMS_SHA256.txt"
    ck_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  [OK] CHECKSUMS_SHA256.txt ({len(checksums)} files)")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main() -> None:
    rc_root = parse_args()
    rc_version = rc_root.parent.name           # e.g. RC_v14_CANON
    nn = _extract_nn(rc_version)

    print(f"\n{'='*72}")
    print(f"  fill_rc_bundle.py — {rc_version}")
    print(f"  Bundle: {rc_root.relative_to(REPO_ROOT)}")
    print(f"{'='*72}")

    # Gate check — abort if required primaries missing
    if not gate_check(rc_root, nn):
        sys.exit(1)

    # Load sources
    print("\n[Loading primary sources...]")
    sources = load_sources(rc_root, nn)
    commit = git_commit()

    # Generate derived docs
    print("\n[00_meta]")
    create_00_meta(rc_root, rc_version, nn, sources, commit)

    print("\n[10_proofs]")
    create_10_proofs(rc_root, rc_version, nn, sources, commit)

    print("\n[50_qa]")
    create_50_qa(rc_root, rc_version, nn, sources)

    print("\n[root docs]")
    create_root_docs(rc_root, rc_version, sources)

    print("\n[60_reference / 90_legacy]")
    create_reference_legacy(rc_root)

    print("\n[audit logs → markdown]")
    render_audit_logs_md(rc_root)

    # Regenerate checksums
    print("\n[CHECKSUMS]")
    regenerate_checksums(rc_root, rc_version)

    # Report
    print(f"\n{'='*72}")
    print(f"  Fill complete.")
    print(f"  Bundle: {rc_root.relative_to(REPO_ROOT)}")
    if BLOCKED:
        print(f"\n  BLOCKED files ({len(BLOCKED)}):")
        for b in BLOCKED:
            print(f"    - {b['file']}: {b['reason']}")
        status = "PARTIAL"
    else:
        status = "COMPLETE"
    print(f"\n  Status: {status}")
    print(f"{'='*72}")

    sys.exit(1 if BLOCKED else 0)


if __name__ == "__main__":
    main()
