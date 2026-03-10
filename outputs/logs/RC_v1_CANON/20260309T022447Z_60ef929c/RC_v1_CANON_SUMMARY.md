<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: rc_result.json -->
<!-- source: 40_tests/pytest_summary.json -->
<!-- source: 30_gates/gate_determinism.json -->
<!-- source: 30_gates/gate_isomorphism.json -->
<!-- source: 30_gates/gate_idempotency.json -->
<!-- source: 10_proofs/BASELINE_POST_SHA256.json -->

# RC_v1_CANON Summary

<!-- fontes: rc_result.json, 40_tests/pytest_summary.json, 30_gates/gate_determinism.json, 30_gates/gate_isomorphism.json, 30_gates/gate_idempotency.json, 10_proofs/BASELINE_POST_SHA256.json -->

## Identity

| Property | Value |
|----------|-------|
| **RC Version** | `RC_v1_CANON` |
| **Execution ID** | `20260309T022447Z_60ef929c` |
| **Overall Status** | `SUCCESS` |
| **Total Duration** | `72.32 s` |

*Source: rc_result.json*

---

## Gates

| Gate | Status |
|------|--------|
| Determinism (Claim iii) | `PASS` |
| Isomorphism (Claim ii) | `PASS` |
| Idempotency (Claim i) | `PASS` |

*Source: 30_gates/*.json via rc_result.json*

---

## Tests and Coverage

| Metric | Value |
|--------|-------|
| **Test scope** | `tests/1-uc-ontology` |
| **CWD** | `H:\certi\bim\onto-tools-prp` |
| Collected | 973 |
| Passed | 973 |
| Failed | 0 |
| Errors | 0 |
| Skipped | 0 |
| Duration | 65.53 s |
| Coverage | 95.04% |
| Coverage Threshold | 95.0% |
| Coverage Passed | True |

*Source: 40_tests/pytest_summary.json*

### Pytest Command

```
PYTHONPATH=H:\certi\bim\onto-tools-prp\src C:\Users\selah\.conda\envs\onto-tools-artigo\python.exe -m pytest tests/1-uc-ontology -v --no-header --tb=short --durations=10 --junitxml=H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\junit.xml --cov=src/onto_tools --cov-report=term --cov-report=xml:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage.xml --cov-report=json:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage.json --cov-report=html:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage_html
```

*Source: 40_tests/pytest_cmd.txt*

### Test Collection

Real collection via `--collect-only -q` (see `40_tests/pytest_collection.txt`)

---

## CI/Audit Artifacts

| Artifact | Status |
|----------|--------|
| `40_tests/pytest_cmd.txt` | ✓ present |
| `40_tests/pytest_collection.txt` | ✓ present |
| `40_tests/pytest_full.txt` | ✓ present |
| `40_tests/pytest_output.txt` | ✓ present |
| `40_tests/pytest_summary.json` | ✓ present |
| `40_tests/pytest_durations.txt` | ✓ present |
| `40_tests/junit.xml` | ✓ present |
| `40_tests/coverage.xml` | ✓ present |
| `40_tests/coverage.json` | ✓ present |
| `40_tests/coverage_html/` | ✓ present |

*Source: real directory listing at fill time*

### Audit Logs (20_runs/)

| Type | Count |
|------|-------|
| JSON (`audit-log-session-*.json`) | 5 |
| Markdown (`audit-log-session-*.md`) | 5 |

*Source: glob scan of 20_runs/ at fill time*

---

## Key Hashes

| Artifact | SHA256 |
|----------|--------|
| Input | `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE` |
| Canonical output (run2a/2b/3) | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| Auto-fix output (run4) | `B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D` |

*Source: rc_result.json*

---

## All Bundle Artifacts

| Path | Size (bytes) |
|------|--------------|
| `00_meta/BASELINE_PRE_SHA256.json` | 216 |
| `00_meta/COMMAND_LOG.md` | 1511 |
| `00_meta/env_snapshot.json` | 353 |
| `00_meta/ENV_SNAPSHOT.md` | 869 |
| `00_meta/INPUT_SNAPSHOT.md` | 685 |
| `00_meta/RC_LAYOUT_STANDARD.md` | 1536 |
| `00_meta/TOOL_VERSIONS.md` | 443 |
| `10_proofs/ARTICLE_COMPATIBILITY_PROOF_STRONG_RC_v1_CANON.md` | 1472 |
| `10_proofs/BASELINE_POST_SHA256.json` | 9256 |
| `10_proofs/declaration_RC_v1_CANON.md` | 1968 |
| `10_proofs/EVIDENCE_MAP_RC_v1_CANON.md` | 1867 |
| `10_proofs/IMMUTABILITY_PROOF.json` | 993 |
| `10_proofs/NORMALIZATION_REPORT_FROM_LOG.md` | 3283315 |
| `10_proofs/RC_v1_CANON_FINAL_REPORT.md` | 1574 |
| `10_proofs/TRACEABILITY_MATRIX_RC_v1_CANON.md` | 1190 |
| `20_runs/run2a_canonicalize/audit-log-session-20260308-232447.json` | 2700 |
| `20_runs/run2a_canonicalize/audit-log-session-20260308-232447.md` | 528 |
| `20_runs/run2a_canonicalize/audit-log-session-20260308-232452.json` | 5204 |
| `20_runs/run2a_canonicalize/audit-log-session-20260308-232452.md` | 827 |
| `20_runs/run2a_canonicalize/canonical_output_run2a.ttl` | 454510 |
| `20_runs/run2a_canonicalize/export-log.json` | 614 |
| `20_runs/run2a_canonicalize/idempotency_run2a.json` | 451 |
| `20_runs/run2a_canonicalize/isomorphism_run2a.json` | 478 |
| `20_runs/run2b_canonicalize/audit-log-session-20260308-232448.json` | 2700 |
| `20_runs/run2b_canonicalize/audit-log-session-20260308-232448.md` | 528 |
| `20_runs/run2b_canonicalize/canonical_output_run2b.ttl` | 454510 |
| `20_runs/run2b_canonicalize/export-log.json` | 614 |
| `20_runs/run3_normalize_canonicalize/audit-log-session-20260308-232448.json` | 722697 |
| `20_runs/run3_normalize_canonicalize/audit-log-session-20260308-232448.md` | 356056 |
| `20_runs/run3_normalize_canonicalize/canonical_output_run3.ttl` | 454510 |
| `20_runs/run3_normalize_canonicalize/export-log.json` | 622 |
| `20_runs/run3_normalize_canonicalize/isomorphism_run3.json` | 486 |
| `20_runs/run3_normalize_canonicalize/normalize_log_run3.json` | 1642011 |
| `20_runs/run4_normalize_canonicalize/audit-log-session-20260308-232450.json` | 721497 |
| `20_runs/run4_normalize_canonicalize/audit-log-session-20260308-232450.md` | 303755 |
| `20_runs/run4_normalize_canonicalize/canonical_output_run4.ttl` | 454333 |
| `20_runs/run4_normalize_canonicalize/export-log.json` | 622 |
| `20_runs/run4_normalize_canonicalize/normalize_log_run4.json` | 1640310 |
| `30_gates/gate_determinism.json` | 445 |
| `30_gates/gate_idempotency.json` | 459 |
| `30_gates/gate_isomorphism.json` | 508 |
| `40_tests/coverage.json` | 281837 |
| `40_tests/coverage.xml` | 153235 |
| `40_tests/coverage_html/.gitignore` | 29 |
| `40_tests/coverage_html/class_index.html` | 53241 |
| `40_tests/coverage_html/coverage_html_cb_188fc9a4.js` | 26185 |
| `40_tests/coverage_html/favicon_32_cb_c827f16f.png` | 1732 |
| `40_tests/coverage_html/function_index.html` | 215140 |
| `40_tests/coverage_html/index.html` | 23249 |
| `40_tests/coverage_html/keybd_closed_cb_900cfef5.png` | 9004 |
| `40_tests/coverage_html/status.json` | 9593 |
| `40_tests/coverage_html/style_cb_5c747636.css` | 16493 |
| `40_tests/coverage_html/z_155ba8e47d823084___init___py.html` | 19277 |
| `40_tests/coverage_html/z_155ba8e47d823084_evidence_writer_py.html` | 87636 |
| `40_tests/coverage_html/z_155ba8e47d823084_hasher_py.html` | 28947 |
| `40_tests/coverage_html/z_155ba8e47d823084_idempotency_py.html` | 90695 |
| `40_tests/coverage_html/z_155ba8e47d823084_isomorphism_py.html` | 66670 |
| `40_tests/coverage_html/z_155ba8e47d823084_manifest_writer_py.html` | 109234 |
| `40_tests/coverage_html/z_155ba8e47d823084_rc_workflow_py.html` | 132186 |
| `40_tests/coverage_html/z_20af5db558a7bde0___init___py.html` | 6683 |
| `40_tests/coverage_html/z_20af5db558a7bde0_commands_py.html` | 171116 |
| `40_tests/coverage_html/z_38236421897dcdc8___init___py.html` | 11883 |
| `40_tests/coverage_html/z_38236421897dcdc8_canonicalizer_py.html` | 117079 |
| `40_tests/coverage_html/z_38236421897dcdc8_graph_py.html` | 136655 |
| `40_tests/coverage_html/z_38236421897dcdc8_naming_validator_py.html` | 227432 |
| `40_tests/coverage_html/z_38236421897dcdc8_normalizer_py.html` | 273090 |
| `40_tests/coverage_html/z_38236421897dcdc8_quality_validator_py.html` | 304251 |
| `40_tests/coverage_html/z_38236421897dcdc8_uri_resolver_py.html` | 83701 |
| `40_tests/coverage_html/z_5271df3e90ef9c41___init___py.html` | 5070 |
| `40_tests/coverage_html/z_5271df3e90ef9c41_protege_serializer_py.html` | 114858 |
| `40_tests/coverage_html/z_5271df3e90ef9c41_rdflib_adapter_py.html` | 32311 |
| `40_tests/coverage_html/z_595be51ff1a7529d___init___py.html` | 7124 |
| `40_tests/coverage_html/z_595be51ff1a7529d_audit_logger_py.html` | 65457 |
| `40_tests/coverage_html/z_84e137c4ce2dc434___init___py.html` | 5946 |
| `40_tests/coverage_html/z_d389b2ab2fb5e40c___init___py.html` | 5951 |
| `40_tests/coverage_html/z_d389b2ab2fb5e40c_audit_formatter_py.html` | 193281 |
| `40_tests/coverage_html/z_ea6fbe74d4ed1d44_facade_py.html` | 225330 |
| `40_tests/coverage_html/z_f232af085125eccc___init___py.html` | 5048 |
| `40_tests/junit.xml` | 149977 |
| `40_tests/pytest_cmd.txt` | 677 |
| `40_tests/pytest_collection.txt` | 64543 |
| `40_tests/pytest_durations.txt` | 1633 |
| `40_tests/pytest_full.txt` | 247206 |
| `40_tests/pytest_output.txt` | 247204 |
| `40_tests/pytest_summary.json` | 1821 |
| `50_qa/COVERAGE_REPORT.txt` | 3945 |
| `50_qa/DESIGNDOC_CONFORMANCE_MATRIX_RC_v1_CANON.md` | 1247 |
| `50_qa/QA_CHECKLIST_FINAL_RC_v1_CANON.md` | 1062 |
| `50_qa/QA_PLAN_RC_v1_CANON.md` | 818 |
| `rc1_result.json` | 961 |
| `rc_result.json` | 961 |
| `results_index_RC_v1_CANON.md` | 7034 |

*Total: 92 files (excluding CHECKSUMS_SHA256.txt)*
*Source: real directory listing at fill time*

---

## Provenance

All values derived from primary artifacts of the current run.
No hardcoded data. Sources: rc_result.json, 40_tests/pytest_summary.json, 30_gates/gate_determinism.json, 30_gates/gate_isomorphism.json, 30_gates/gate_idempotency.json, 10_proofs/BASELINE_POST_SHA256.json.
