# Evidence Map - RC_v13_CANON

## Overview

This document maps article claims to evidence files with their SHA-256 hashes for verification.

## Evidence Index

### Claim (i) Idempotency

| Evidence File | Purpose | Key Field | Value |
|--------------|---------|-----------|-------|
| `20_runs/run2a_canonicalize/idempotency_run2a.json` | Idempotency verification | `is_idempotent` | `true` |
| `20_runs/run2a_canonicalize/idempotency_run2a.json` | Hash comparison | `hashes_match` | `true` |
| `30_gates/gate_idempotency.json` | Gate status | `status` | `PASS` |

### Claim (ii) Semantic Preservation

| Evidence File | Purpose | Key Field | Value |
|--------------|---------|-----------|-------|
| `20_runs/run2a_canonicalize/isomorphism_run2a.json` | Isomorphism check | `are_isomorphic` | `true` |
| `20_runs/run2b_canonicalize/isomorphism_run2b.json` | Isomorphism check | `are_isomorphic` | `true` |
| `20_runs/run3_normalize_canonicalize/isomorphism_run3.json` | Isomorphism check | `are_isomorphic` | `true` |
| `30_gates/gate_isomorphism.json` | Gate status | `status` | `PASS` |

### Claim (iii) Determinism

| Evidence File | Purpose | Key Field | Value |
|--------------|---------|-----------|-------|
| `20_runs/run2a_canonicalize/run_manifest_run2a.json` | Run 2a output hash | `outputs[0].sha256` | `E1F9622F50AF55FA...` |
| `20_runs/run2b_canonicalize/run_manifest_run2b.json` | Run 2b output hash | `outputs[0].sha256` | `E1F9622F50AF55FA...` |
| `30_gates/gate_determinism.json` | Gate status | `status` | `PASS` |

### Claim (iv) Test Suite

| Evidence File | Purpose | Key Field | Value |
|--------------|---------|-----------|-------|
| `40_tests/pytest_summary.json` | Test results | `results.passed` | `963` |
| `40_tests/pytest_summary.json` | Coverage | `coverage.total_percent` | `95.04` |
| `40_tests/pytest_collection.txt` | Collected tests | - | 963 items |
| `40_tests/pytest_full.txt` | Full output | - | Complete run log |

## Critical Hashes

| Artifact | SHA-256 |
|----------|---------|
| Input ontology | `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE` |
| Run 2a canonical output | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| Run 2b canonical output | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| Run 3 canonical output | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| Run 4 auto-fix output | `B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D` |

## Directory Structure

```
RC_v13_CANON/20260227_042545/
├── 00_meta/         # Environment and input snapshots
├── 10_proofs/       # Article proofs and reports
├── 20_runs/         # Pipeline execution runs (run2a, run2b, run3, run4)
├── 30_gates/        # Verification gates
├── 40_tests/        # Test artifacts
├── 50_qa/           # QA artifacts
├── 60_reference/    # Reference pointers only
└── 90_legacy/       # Legacy notes
```

---
*Generated: 2026-02-27T04:26:57Z*
