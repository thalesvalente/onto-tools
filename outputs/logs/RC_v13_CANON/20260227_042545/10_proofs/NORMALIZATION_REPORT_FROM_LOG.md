# Normalization Report (Generated from Log)

## Summary

| Property | Value |
|----------|-------|
| **Input File** | `data/examples/energy-domain-ontology.ttl` |
| **Input Hash** | `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE` |
| **Input Triples** | 6803 |
| **Timestamp** | 2026-02-27T04:25:45 |
| **Mode** | validate_only (Run3) / auto_fix (Run4) |

## Detected Issues

| Category | Count |
|----------|-------|
| **Total Issues** | 1,831 |
| **Errors** | 260 |
| **Warnings** | 1,571 |
| **Classes Checked** | 737 |

### Issue Breakdown
- **Naming Convention Errors**: 260 (underscore in PascalCase class names)
- **Quality Validator Warnings**: 806 (includes duplicates, identifier issues, etc.)

## Proposed Corrections

| Type | Entities | Total Fixes | Status |
|------|----------|-------------|--------|
| **PrefLabel** | 206 | 328 | Blocked by rulebook |
| **Definition** | 195 | 293 | Blocked by rulebook |
| **IRI** | 63 | 746 | Available for auto-fix |
| **Identifier** | 58 | 58 | Available for auto-fix |
| **Total** | 522 | 621 | - |

## Applied Corrections (Run3 - Validate Only)

| Type | Applied |
|------|---------|
| **PrefLabel** | 0 (validate-only mode) |
| **Definition** | 0 (validate-only mode) |
| **IRI** | 0 (validate-only mode) |
| **Identifier** | 0 (validate-only mode) |
| **Total Triples Modified** | 0 |

## Auto-Fix Comparison (Run4 vs Run3)

| Metric | Run3 (validate) | Run4 (auto-fix) | Delta |
|--------|----------------|-----------------|-------|
| **Output Hash** | E1F9622F50AF55FA... | B28D98AC2A22E4C7... | Different |
| **Triples Modified** | 0 | 743 | +743 |
| **IRI Replacements** | 0 | 746 | +746 ops |
| **Identifier Fixes** | 0 | 58 | +58 ops |
| **Overlap** | - | 61 | (IRI+ID in same triple) |

**Auto-fix Formula**: 746 IRI ops + 58 ID ops - 61 overlap = **743 unique triples modified**

## Test Coverage Metrics

| Metric | Value |
|--------|-------|
| **Total Tests** | 963 |
| **Passed** | 963 (100%) |
| **Failed** | 0 |
| **Skipped** | 0 |
| **Coverage** | 95.04% |
| **Test Suite** | `tests/1-uc-ontology` |
| **Duration** | 65.43s |
