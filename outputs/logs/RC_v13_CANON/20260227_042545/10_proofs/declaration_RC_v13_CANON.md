# Declaration - RC_v13_CANON

## Release Candidate Declaration

**RC Version**: RC_v13_CANON  
**Date**: 2026-02-27  
**Timestamp**: 2026-02-27T04:25:45Z

---

## Input Ontology

| Property | Value |
|----------|-------|
| **File** | `data/examples/energy-domain-ontology.ttl` |
| **SHA-256** | `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE` |
| **Triple Count** | 6803 |

## Commands Executed

```bash
# Run 2a - Canonicalize
python scripts/run_rc13.py  # via RC workflow API

# Run 2b - Canonicalize (determinism check)
# (via Canonicalizer API - second independent run)

# Run 3 - Normalize + Canonicalize (validate only)
# (via Normalizer + canonicalize_graph API)

# Run 4 - Normalize + Canonicalize (auto-fix)
# (via Normalizer with auto_fix=True + canonicalize_graph API)

# Tests
pytest tests/1-uc-ontology --cov=src/onto_tools
```

## Gate Status

| Gate | Status |
|------|--------|
| Idempotency (i) | PASS |
| Isomorphism (ii) | PASS |
| Determinism (iii) | PASS |
| Test Suite (iv) | PASS |

## Test/Coverage Status

| Metric | Value |
|--------|-------|
| Tests Collected | 963 |
| Tests Passed | 963 |
| Tests Failed | 0 |
| Coverage | 95.04% |

## Canonical Output

| Property | Value |
|----------|-------|
| **SHA-256 (canon)** | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| **SHA-256 (auto-fix)** | `B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D` |
| **Triple Count** | 6803 |
| **Deterministic** | Yes (Run 2a == Run 2b) |

---

## Declaration

I hereby declare that RC_v13_CANON:

1. Was generated using the official OntoTools pipeline (CLI → Facade → Domain)
2. Contains no copied artifacts from prior RCs (clean-room)
3. All evidence was generated fresh during this RC execution
4. All verification gates passed
5. All tests passed with coverage >= 95.0%

---
*Generated: 2026-02-27T04:26:57Z*
