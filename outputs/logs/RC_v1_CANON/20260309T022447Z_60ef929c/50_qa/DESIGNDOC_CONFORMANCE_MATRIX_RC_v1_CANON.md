<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: 40_tests/pytest_summary.json -->
<!-- source: rc_result.json -->
<!-- source: 30_gates/gate_determinism.json -->
<!-- source: 30_gates/gate_isomorphism.json -->
<!-- source: 30_gates/gate_idempotency.json -->

# Design Doc Conformance Matrix — RC_v1_CANON

<!-- fontes: 40_tests/pytest_summary.json, rc_result.json, 30_gates/gate_determinism.json, 30_gates/gate_isomorphism.json, 30_gates/gate_idempotency.json -->

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
