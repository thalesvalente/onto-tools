<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: 00_meta/env_snapshot.json -->
<!-- source: rc_result.json -->

# RC_v1_CANON Layout Standard

<!-- fontes: 00_meta/env_snapshot.json, rc_result.json -->

## Overview

This document defines the canonical directory structure for RC_v1_CANON.
Generated from `rc_result.json` and `env_snapshot.json`.

## Bundle Root

`outputs/logs/RC_v1_CANON/20260309T022447Z_60ef929c/`

## Directory Structure

```
RC_v1_CANON/20260309T022447Z_60ef929c/
├── 00_meta/                    # Metadata and environment
├── 10_proofs/                  # Article proofs and reports
├── 20_runs/                    # Pipeline execution runs
│   ├── run2a_canonicalize/
│   ├── run2b_canonicalize/
│   ├── run3_normalize_canonicalize/
│   └── run4_normalize_canonicalize/
├── 30_gates/                   # Verification gates
├── 40_tests/                   # Test execution artifacts
├── 50_qa/                      # QA artifacts
├── 60_reference/
├── 90_legacy/
├── results_index_RC_v1_CANON.md
├── RC_v1_CANON_SUMMARY.md
├── rc_result.json           # PRIMARY — source of truth
└── CHECKSUMS_SHA256.txt
```

## RC Status

| Property | Value |
|----------|-------|
| **RC Version** | `RC_v1_CANON` |
| **Bundle Timestamp** | `20260309T022447Z_60ef929c` |
| **Overall Status** | `SUCCESS` |

*Source: rc_result.json*
