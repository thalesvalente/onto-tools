# Traceability Matrix - RC_v13_CANON

## Problem → Objective → Evidence Mapping

This matrix traces article problems (Section 3) to objectives (Section 4) to RC_v13_CANON evidence.

| ID | Problem (Sec 3) | Objective (Sec 4) | Evidence RC_v13 | Metric/Result |
|----|-----------------|-------------------|-----------------|---------------|
| T1 | Non-deterministic serialization causes diff noise | Deterministic canonicalization | `30_gates/gate_determinism.json` | 2a hash == 2b hash: PASS |
| T2 | Semantic changes during serialization | Preserve graph isomorphism | `30_gates/gate_isomorphism.json` | are_isomorphic: true |
| T3 | Unstable re-serialization (f(f(x)) ≠ f(x)) | Idempotent canonicalization | `30_gates/gate_idempotency.json` | is_idempotent: true |
| T4 | Lack of quality validation | Rulebook-driven normalization | `20_runs/run3_*/normalize_log_run3.json` | 1831 issues detected |
| T5 | No audit trail | Execution manifests and logs | `20_runs/*/run_manifest_*.json` | All runs have manifests |
| T6 | Untested transformation code | Comprehensive test suite | `40_tests/pytest_summary.json` | 963 tests, 95.04% coverage |
| T7 | No evidence for reproducibility claims | Gates + verification artifacts | `30_gates/*.json` | All gates PASS |

## Implementation Traceability

| Component | Source File | Tests | Coverage |
|-----------|-------------|-------|----------|
| Canonicalizer | `src/onto_tools/domain/ontology/canonicalizer.py` | `tests/1-uc-ontology/unit/test_canonicalizer.py` | 97%+ |
| Normalizer | `src/onto_tools/domain/ontology/normalizer.py` | `tests/1-uc-ontology/unit/test_normalizer.py` | 97%+ |
| Isomorphism | `src/onto_tools/application/verification/isomorphism.py` | `tests/1-uc-ontology/unit/test_verification_*.py` | 92%+ |
| Idempotency | `src/onto_tools/application/verification/idempotency.py` | `tests/1-uc-ontology/unit/test_verification_*.py` | 93%+ |
| Hasher | `src/onto_tools/application/verification/hasher.py` | `tests/1-uc-ontology/unit/test_verification_*.py` | 100% |

## Call Chain Verification

Pipeline entry point to verification:

```
CLI (commands.py)
  → OntoToolsFacade (facade.py)
    → Canonicalizer.canonicalize() (canonicalizer.py)
    → compare_isomorphism() (isomorphism.py)
    → check_idempotency() (idempotency.py)
    → sha256_file() (hasher.py)
    → write_manifest_atomic() (manifest_writer.py)
```

Each step is traceable via:
- Function signatures
- Return types (CanonicalizationResult, IsomorphismReport, IdempotencyReport)
- Generated artifacts (manifests, JSON reports)

---
*Generated: 2026-02-27T04:26:57Z*
