# RC_v13_CANON Layout Standard

## Overview
This document defines the canonical directory structure for RC_v13_CANON release candidate.
All artifacts are organized in a single PRIMARY tree with no structural duplicates.

## Directory Structure

```
RC_v13_CANON/
├── 00_meta/                    # Metadata and environment
│   ├── RC_LAYOUT_STANDARD.md   # This file
│   ├── COMMAND_LOG.md          # All commands executed
│   ├── ENV_SNAPSHOT.md         # Environment snapshot
│   ├── TOOL_VERSIONS.md        # Tool versions
│   ├── INPUT_SNAPSHOT.md       # Input ontology snapshot
│   ├── BASELINE_PRE_SHA256.json # Pre-RC checksums
│   └── env_snapshot.json       # Machine-readable env snapshot
├── 10_proofs/                  # Article proofs and reports
│   ├── BASELINE_POST_SHA256.json
│   ├── declaration_RC_v13_CANON.md
│   ├── RC_v13_FINAL_REPORT.md
│   ├── ARTICLE_COMPATIBILITY_PROOF_STRONG_RC13.md
│   ├── TRACEABILITY_MATRIX_RC13.md
│   ├── EVIDENCE_MAP_RC13.md
│   ├── NORMALIZATION_REPORT_FROM_LOG.md
│   └── IMMUTABILITY_PROOF.json
├── 20_runs/                    # Pipeline execution runs
│   ├── run2a_canonicalize/     # First canonicalize run
│   ├── run2b_canonicalize/     # Second canonicalize run (determinism)
│   ├── run3_normalize_canonicalize/ # Normalize + canonicalize (validate only)
│   └── run4_normalize_canonicalize/ # Normalize + canonicalize (auto-fix)
├── 30_gates/                   # Verification gates
│   ├── gate_determinism.json
│   ├── gate_isomorphism.json
│   └── gate_idempotency.json
├── 40_tests/                   # Test execution artifacts
│   ├── pytest_cmd.txt
│   ├── pytest_collection.txt
│   ├── pytest_output.txt
│   ├── pytest_full.txt
│   └── pytest_summary.json
├── 50_qa/                      # QA artifacts
│   ├── QA_PLAN_RC13.md
│   ├── QA_CHECKLIST_FINAL_RC13.md
│   ├── COVERAGE_REPORT.txt
│   └── DESIGNDOC_CONFORMANCE_MATRIX_RC13.md
├── 60_reference/               # References only (no copies)
│   └── README.md
├── 90_legacy/                  # Legacy notes (if any)
│   └── README.md
├── results_index_RC_v13_CANON.md
├── RC_v13_CANON_SUMMARY.md
├── rc13_result.json
└── CHECKSUMS_SHA256.txt
```

## Principles

1. **Single PRIMARY tree**: No duplicate structures (head_current, article_repro, etc.)
2. **Clean-room RC**: All evidence generated fresh, not copied from prior RCs
3. **Traceable artifacts**: Every file has SHA256 in CHECKSUMS_SHA256.txt
4. **Gate-driven workflow**: Each phase has PASS/FAIL gates
5. **Run4 added**: RC13 includes auto-fix run (run4) in addition to validate-only run (run3)

## Created
- Date: 2026-02-27
- RC Version: v13_CANON
