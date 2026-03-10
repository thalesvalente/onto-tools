<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: rc_result.json -->
<!-- source: 30_gates/gate_determinism.json -->
<!-- source: 30_gates/gate_isomorphism.json -->
<!-- source: 30_gates/gate_idempotency.json -->
<!-- source: 40_tests/pytest_summary.json -->
<!-- source: 10_proofs/BASELINE_POST_SHA256.json -->

# Article Compatibility Proof (Strong) — RC_v1_CANON

<!-- fontes: rc_result.json, 30_gates/gate_determinism.json, 30_gates/gate_isomorphism.json, 30_gates/gate_idempotency.json, 40_tests/pytest_summary.json, 10_proofs/BASELINE_POST_SHA256.json -->

## Claim i — Idempotency

**Claim**: f(f(x)) == f(x)
**Gate**: `PASS`
**Source**: 30_gates/gate_idempotency.json
**Evidence**: 20_runs/run2a_canonicalize/idempotency_run2a.json

---

## Claim ii — Semantic Preservation (Isomorphism)

**Claim**: input ≅ canonical output
**Gate**: `PASS`
**Source**: 30_gates/gate_isomorphism.json
**Evidence**: 20_runs/run2a_canonicalize/isomorphism_run2a.json

---

## Claim iii — Determinism

**Claim**: SHA256(run2a) == SHA256(run2b)
**Gate**: `PASS`
**Source**: 30_gates/gate_determinism.json
**Evidence**: run2a hash = `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` (same as run2b)

---

## Claim iv — Test Coverage

**Tests Passed**: 973 / 973
**Coverage**: 95.04% (threshold: 95.0%)
**Coverage Passed**: True
**Source**: 40_tests/pytest_summary.json
