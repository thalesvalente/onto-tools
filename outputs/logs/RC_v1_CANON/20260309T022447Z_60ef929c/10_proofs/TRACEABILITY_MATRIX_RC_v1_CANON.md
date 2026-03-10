<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: rc_result.json -->
<!-- source: 30_gates/gate_determinism.json -->
<!-- source: 30_gates/gate_isomorphism.json -->
<!-- source: 30_gates/gate_idempotency.json -->
<!-- source: 40_tests/pytest_summary.json -->
<!-- source: 10_proofs/BASELINE_POST_SHA256.json -->

# Traceability Matrix — RC_v1_CANON

<!-- fontes: rc_result.json, 30_gates/gate_determinism.json, 30_gates/gate_isomorphism.json, 30_gates/gate_idempotency.json, 40_tests/pytest_summary.json, 10_proofs/BASELINE_POST_SHA256.json -->

| Claim | Gate | Evidence File | Status |
|-------|------|---------------|--------|
| (i) Idempotency | gate_idempotency | 20_runs/run2a_canonicalize/idempotency_run2a.json | `PASS` |
| (ii) Isomorphism | gate_isomorphism | 20_runs/run2a_canonicalize/isomorphism_run2a.json | `PASS` |
| (iii) Determinism | gate_determinism | 30_gates/gate_determinism.json | `PASS` |
| (iv) Tests | pytest_summary | 40_tests/pytest_summary.json | `PASS` |
| (v) Coverage | pytest_summary | 40_tests/pytest_summary.json | `PASS` |

*All values derived from primary artifacts; no hardcoded data.*
