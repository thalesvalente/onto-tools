# Input Snapshot - RC_v13_CANON

## Primary Input Ontology

| Property | Value |
|----------|-------|
| **Path** | `data/examples/energy-domain-ontology.ttl` |
| **SHA256** | `a772ae732ef041b951b7af0c27d4a62a611c09c0dfc0a8d0f2477bf4eee2a8ae` |
| **Triple Count** | 6803 |
| **File Size** | 658,838 bytes |
| **Format** | Turtle (TTL) |

## Repository State

| Property | Value |
|----------|-------|
| **Git Commit** | `cc65d0898a1b6e41a9961be646f994e57b7167d2` |
| **Branch** | `main` (or current) |
| **Timestamp** | `2026-02-27T04:25:45` |

## Snapshot Purpose

This file documents the EXACT input used for RC_v13_CANON execution.
All pipeline runs use this single primary input - no "head_current" vs "article_repro" split.

Input hash is **identical to RC_v12_CANON**, confirming the ontology was not modified
between RC12 and RC13.

## Integrity Verification

To verify input integrity:
```bash
python -m onto_tools verify hash data/examples/energy-domain-ontology.ttl
# Expected: a772ae732ef041b951b7af0c27d4a62a611c09c0dfc0a8d0f2477bf4eee2a8ae
```
