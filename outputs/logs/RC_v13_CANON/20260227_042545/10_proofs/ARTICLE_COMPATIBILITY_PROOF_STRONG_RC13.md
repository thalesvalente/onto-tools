# Article Compatibility Proof (Strong) - RC_v13_CANON

## Overview

This document provides **strong evidence** that RC_v13_CANON artifacts support the claims
made in the article. Each claim is mapped to:
1. The code/module that implements it
2. The pipeline stage where it executes
3. The specific evidence file(s) with verification data

## Claim Mapping Table

| Claim | Description | Module | Pipeline Stage | Evidence File | Evidence Field |
|-------|-------------|--------|----------------|---------------|----------------|
| **(i) Idempotency** | f(f(x)) == f(x) | `canonicalizer.py` | Canonicalize | `30_gates/gate_idempotency.json` | `is_idempotent: true` |
| **(ii) Isomorphism** | Semantic preservation | `isomorphism.py` | Verification | `30_gates/gate_isomorphism.json` | `are_isomorphic: true` |
| **(iii) Determinism** | Byte-identical outputs | `canonicalizer.py` | Multi-run | `30_gates/gate_determinism.json` | `hashes_match: true` |
| **(iv) Test Suite** | All tests pass, coverage >= 95.0% | pytest | Test Phase | `40_tests/pytest_summary.json` | `passed: 963, coverage: 95.04%` |

## Detailed Evidence

### (i) Idempotency

**Claim**: Re-canonicalizing a canonical file must not change it.

**Implementation Path**:
```
CLI: verify idempotency <file>
  → check_idempotency() @ verification/idempotency.py
  → canonicalize_graph() @ domain/ontology/canonicalizer.py
  → SHA-256 comparison
```

**Evidence**:
- File: `20_runs/run2a_canonicalize/idempotency_run2a.json`
- Result: `is_idempotent: true`, `hashes_match: true`
- Gate: `30_gates/gate_idempotency.json` → **PASS**

### (ii) Semantic Preservation (Isomorphism)

**Claim**: Canonicalized output is semantically equivalent to input (RDF graph isomorphism).

**Implementation Path**:
```
CLI: verify isomorphism <file_a> <file_b>
  → compare_isomorphism() @ verification/isomorphism.py
  → rdflib.compare.isomorphic()
  → IsomorphismReport
```

**Evidence**:
- File: `20_runs/run2a_canonicalize/isomorphism_run2a.json`
- Result: `are_isomorphic: true`, input triples == output triples (6803)
- Gate: `30_gates/gate_isomorphism.json` → **PASS**

### (iii) Byte-level Determinism

**Claim**: Multiple executions with identical inputs produce byte-identical outputs.

**Implementation Path**:
```
Run 2a: canonicalize(input) → output_2a.ttl
Run 2b: canonicalize(input) → output_2b.ttl
Verify: SHA-256(output_2a) == SHA-256(output_2b)
```

**Evidence**:
- Run 2a hash: `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49`
- Run 2b hash: `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49`
- Match: **YES**
- Gate: `30_gates/gate_determinism.json` → **PASS**

### (iv) Test Suite

**Claim**: Comprehensive test suite validates pipeline behavior.

**Evidence**:
- Command: `pytest tests/1-uc-ontology`
- Collected: 963 tests
- Passed: 963 tests (100%)
- Coverage: 95.04% (threshold: 95.0%)
- Gate: `40_tests/pytest_summary.json` → **PASS**

## Continuity from RC_v12_CANON

| Artifact | RC_v12 Hash | RC_v13 Hash | Match |
|----------|-------------|-------------|-------|
| Input ontology | `A772AE732EF041B9...` | `A772AE732EF041B9...` | YES |
| Canonical output | `E1F9622F50AF55FA...` | `E1F9622F50AF55FA...` | YES |
| Auto-fix output | `B28D98AC2A22E4C7...` | `B28D98AC2A22E4C7...` | YES |

All cryptographic hashes match RC_v12_CANON, confirming full reproducibility.

---
*Generated: 2026-02-27T04:26:57Z*
