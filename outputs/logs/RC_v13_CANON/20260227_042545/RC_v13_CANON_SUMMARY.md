# RC_v13_CANON — Summary

## Status: ✅ SUCCESS

---

## Key Results

| Metric | Value |
|--------|-------|
| **Input SHA256** | A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE |
| **Canon SHA256 (Run2a/2b)** | E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49 |
| **Run3 SHA256 (validate)** | E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49 |
| **Run4 SHA256 (auto-fix)** | B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D |
| **Triples** | 6803 (all runs) |
| **Tests** | 963 passed, 0 failed |
| **Coverage** | 95.04% (threshold: 95.0%) |
| **Duration** | 71.2s |

---

## Gates

| Gate | Status |
|------|--------|
| Determinism (Run2a == Run2b) | ✅ PASS |
| Isomorphism (input ≅ output) | ✅ PASS |
| Idempotency (f(f(x)) == f(x)) | ✅ PASS |

---

## RC_v13 vs RC_v12 — Comparison

| Metric | RC_v12 | RC_v13 | Delta |
|--------|--------|--------|-------|
| **Input SHA256** | A772AE73... | A772AE73... | ✅ Identical |
| **Canon SHA256** | E1F9622F... | E1F9622F... | ✅ Identical |
| **Run4 SHA256** | B28D98AC... | B28D98AC... | ✅ Identical |
| **Triples** | 6803 | 6803 | ✅ Identical |
| **Tests Passed** | 938 | 963 | +25 (cleanup removed 11 dead tests, added 36 new) |
| **Tests Failed** | 0 | 0 | ✅ |
| **Coverage** | 94.05% | 95.04% | +0.99% |
| **Determinism** | PASS | PASS | ✅ |
| **Isomorphism** | PASS | PASS | ✅ |
| **Idempotency** | PASS | PASS | ✅ |
| **Threshold** | 90.0% | 95.0% | Raised bar |

### Key Observations

1. **Pipeline Stability**: All hashes are byte-identical between RC12 and RC13. The canonicalization and normalization pipeline produces the same output despite code cleanup.

2. **Test Count Change** (938 → 963):
   - Removed 11 tests of dead adapters (excel, json_io, sparql)
   - Net gain of +25 tests reflects test additions made between RC12 and RC13

3. **Coverage Improvement** (94.05% → 95.04%):
   - Removed dead code (empty domain packages, unused adapters)
   - Reduced denominator → coverage ratio improved
   - Threshold raised from 90% to 95%

4. **Code Cleanup (RC12 → RC13)**:
   - Deleted: `adapters/sparql/`, `adapters/excel/`, `adapters/json_io/`
   - Deleted: `domain/comparison/`, `domain/data_input/`, `domain/export/`, `domain/query/`
   - Deleted: broken one-off scripts (`fix_run3_manifest.py`, `generate_rc12_run4.py`)
   - Fixed: `menu.py` dead imports

---

## Article Claims Supported

| Claim | Evidence |
|-------|----------|
| (i) Idempotency | `gate_idempotency.json` — f(f(x)) == f(x) ✅ |
| (ii) Semantic Preservation | `gate_isomorphism.json` — input ≅ output ✅ |
| (iii) Byte-level Determinism | `gate_determinism.json` — Run2a == Run2b ✅ |
| (iv) Comprehensive Tests | `pytest_summary.json` — 963 tests, 95.04% coverage ✅ |
| (v) Reproducibility | All hashes identical to RC12 ✅ |

---

## Directory Structure

```
RC_v13_CANON/20260227_042545/
├── 00_meta/           # Environment snapshot
├── 10_proofs/         # BASELINE_POST_SHA256.json
├── 20_runs/           # Pipeline execution runs
│   ├── run2a_canonicalize/
│   ├── run2b_canonicalize/
│   ├── run3_normalize_canonicalize/
│   └── run4_normalize_canonicalize/
├── 30_gates/          # gate_determinism/isomorphism/idempotency.json
├── 40_tests/          # pytest_summary.json, pytest_full.txt
├── 50_qa/
├── CHECKSUMS_SHA256.txt
└── rc13_result.json
```

---

*Generated: 2026-02-27T04:27:00Z*
*Based on: RC_v13_CANON execution with 963 tests*
