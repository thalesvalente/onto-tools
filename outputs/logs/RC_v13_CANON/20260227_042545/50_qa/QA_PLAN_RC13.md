# QA Plan - RC_v13_CANON

## Purpose

This QA plan defines the verification criteria for the RC_v13_CANON release candidate.
All criteria must be satisfied for the RC to be considered valid.

## Scope

- **Target Domain**: Ontology processing (tests/1-uc-ontology)
- **Coverage Threshold**: 95.0% (line coverage)
- **RC Type**: Clean-room (no artifacts copied from prior RCs)

## Quality Gates

### G1: Structure Compliance
- [ ] RC follows canonical layout (no duplicate subtrees)
- [ ] All required directories exist (00_meta through 90_legacy)
- [ ] No "head_current" vs "article_repro" split

### G2: Input Documentation
- [ ] Input ontology SHA-256 recorded
- [ ] Triple count documented
- [ ] Git commit hash captured
- [ ] Timestamp recorded

### G3: Pipeline Execution
- [ ] Run 2a (canonicalize) completed with manifest
- [ ] Run 2b (canonicalize) completed with manifest
- [ ] Run 3 (normalize + canonicalize, validate) completed with manifest
- [ ] Run 4 (normalize + canonicalize, auto-fix) completed with manifest

### G4: Verification Gates
- [ ] gate_determinism.json exists and is PASS
- [ ] gate_isomorphism.json exists and is PASS
- [ ] gate_idempotency.json exists and is PASS

### G5: Test Suite
- [ ] pytest run on tests/1-uc-ontology only
- [ ] Collection recorded (pytest_collection.txt)
- [ ] All tests pass (0 failures)
- [ ] Coverage >= 95.0%

### G6: Evidence Documentation
- [ ] CHECKSUMS_SHA256.txt generated
- [ ] results_index_RC_v13_CANON.md generated
- [ ] EVIDENCE_MAP_RC13.md generated
- [ ] TRACEABILITY_MATRIX_RC13.md generated
- [ ] ARTICLE_COMPATIBILITY_PROOF_STRONG_RC13.md generated

### G7: Normalization Artifacts
- [ ] normalize_log_run3.json generated
- [ ] normalize_log_run4.json generated
- [ ] NORMALIZATION_REPORT_FROM_LOG.md generated

## Acceptance Criteria

1. All gates G1-G7 must be satisfied
2. No FAIL status in any gate file
3. All evidence traceable to article claims (i)-(iv)

## Responsible

- QA Lead: Automated RC workflow (scripts/run_rc13.py)
- Approver: Project Lead (manual review)

---
*Plan Version: 1.0*
*Created: 2026-02-27*
