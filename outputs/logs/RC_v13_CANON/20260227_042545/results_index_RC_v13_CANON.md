# Results Index - RC_v13_CANON

## RC Information

| Property | Value |
|----------|-------|
| **RC Version** | RC_v13_CANON |
| **Timestamp** | 2026-02-27T04:25:45Z |
| **Input Ontology** | data/examples/energy-domain-ontology.ttl |
| **Input SHA-256** | A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE |

## Gate Results Summary

| Gate | Status | Evidence |
|------|--------|----------|
| **Idempotency (i)** | ✅ PASS | `30_gates/gate_idempotency.json` |
| **Isomorphism (ii)** | ✅ PASS | `30_gates/gate_isomorphism.json` |
| **Determinism (iii)** | ✅ PASS | `30_gates/gate_determinism.json` |
| **Test Suite (iv)** | ✅ PASS | `40_tests/pytest_summary.json` |

## Artifact Index

### 00_meta/ (Metadata)
| File | Purpose | Claim Support |
|------|---------|---------------|
| `env_snapshot.json` | Environment + input state | All claims |

### 10_proofs/ (Proofs)
| File | Purpose | Claim Support |
|------|---------|---------------|
| `BASELINE_POST_SHA256.json` | Post-execution file hashes | Immutability |

### 20_runs/ (Pipeline Runs)
| Subdirectory | Purpose | Claim Support |
|--------------|---------|---------------|
| `run2a_canonicalize/` | First canonicalization | (i), (ii), (iii) |
| `run2b_canonicalize/` | Second canonicalization (determinism) | (iii) |
| `run3_normalize_canonicalize/` | Normalize + canonicalize (validate-only) | Pipeline |
| `run4_normalize_canonicalize/` | Normalize + canonicalize (auto-fix) | Auto-fix |

### 30_gates/ (Verification Gates)
| File | Purpose | Result |
|------|---------|--------|
| `gate_idempotency.json` | f(f(x)) == f(x) | PASS |
| `gate_isomorphism.json` | RDF graph equivalence | PASS |
| `gate_determinism.json` | Byte-identical outputs | PASS |

### 40_tests/ (Test Artifacts)
| File | Purpose |
|------|---------|
| `pytest_full.txt` | Full pytest output |
| `pytest_summary.json` | Results summary (SOURCE OF TRUTH) |

## Key Metrics

| Metric | RC_v13 | RC_v12 (for comparison) |
|--------|--------|------------------------|
| Tests Collected | 963 | 938 |
| Tests Passed | 963 | 938 |
| Code Coverage | 95.04% | 94.05% |
| Coverage Threshold | 95.0% | 90.0% |
| Triple Count (all runs) | 6803 | 6803 |
| Canon SHA-256 | E1F9622F... | E1F9622F... (identical) |
