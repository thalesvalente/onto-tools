<!-- gerado automaticamente por fill_rc_bundle.py; não editar manualmente -->
<!-- source: 40_tests/pytest_cmd.txt -->
<!-- source: rc_result.json -->

# Command Log — RC_v1_CANON

<!-- fontes: 40_tests/pytest_cmd.txt, rc_result.json -->

## Overview

All commands executed via `scripts/run_rc.py` during `RC_v1_CANON` generation.
Bundle execution_id: `20260309T022447Z_60ef929c`

---

## FASE 5 — Tests

### Pytest Execution (exact command)

```
PYTHONPATH=H:\certi\bim\onto-tools-prp\src C:\Users\selah\.conda\envs\onto-tools-artigo\python.exe -m pytest tests/1-uc-ontology -v --no-header --tb=short --durations=10 --junitxml=H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\junit.xml --cov=src/onto_tools --cov-report=term --cov-report=xml:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage.xml --cov-report=json:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage.json --cov-report=html:H:\certi\bim\onto-tools-prp\outputs\logs\RC_v1_CANON\20260309T022447Z_60ef929c\40_tests\coverage_html
```

*Source: 40_tests/pytest_cmd.txt*

---

## FASE 2–4 — Pipeline Runs

Pipeline runs executed via Python API (`run_rc.py`).
See `20_runs/*/` for per-run artifacts.

---

## Bundle Result

| Property | Value |
|----------|-------|
| **Status** | `SUCCESS` |
| **Execution ID** | `20260309T022447Z_60ef929c` |

*Source: rc_result.json*
