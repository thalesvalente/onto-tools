# RC Template - Design Doc (v2.0)

**Canonical Release Candidate Structure for OntoTools**

*Based on: RC_v13_CANON execution (2026-02-27)*

---

## Purpose

Este documento define a estrutura canônica para RCs (Release Candidates) do OntoTools, garantindo:

1. **Reprodutibilidade** — Qualquer pessoa pode verificar os resultados
2. **Rastreabilidade** — Hashes SHA256 ligam entrada → saída
3. **Validação Automática** — Gates executáveis verificam integridade
4. **Paridade Estrutural** — Todo RC segue **a mesma árvore** de diretórios

---

## Estrutura de Diretórios

```
outputs/logs/RC_vNN_CANON/
└── YYYYMMDD_HHMMSS/                    # Bundle (timestamp da execução)
    │
    ├── 00_meta/                         # Metadata e ambiente
    │   ├── RC_LAYOUT_STANDARD.md        # Este layout
    │   ├── COMMAND_LOG.md               # Todos os comandos executados
    │   ├── ENV_SNAPSHOT.md              # Snapshot do ambiente (legível)
    │   ├── env_snapshot.json            # Snapshot do ambiente (JSON)
    │   ├── TOOL_VERSIONS.md             # Versões de ferramentas
    │   ├── INPUT_SNAPSHOT.md            # Input ontologia com SHA256
    │   └── BASELINE_PRE_SHA256.json     # Status pré-execução
    │
    ├── 10_proofs/                       # Provas e relatórios para artigo
    │   ├── BASELINE_POST_SHA256.json    # SOURCE OF TRUTH para hashes
    │   ├── declaration_RC_vNN_CANON.md  # Declaração formal do RC
    │   ├── RC_vNN_FINAL_REPORT.md       # Relatório final
    │   ├── IMMUTABILITY_PROOF.json      # Prova de imutabilidade
    │   ├── NORMALIZATION_REPORT_FROM_LOG.md
    │   ├── ARTICLE_COMPATIBILITY_PROOF_STRONG_RCNN.md
    │   ├── TRACEABILITY_MATRIX_RCNN.md
    │   └── EVIDENCE_MAP_RCNN.md
    │
    ├── 20_runs/                         # Execuções do pipeline
    │   ├── run2a_canonicalize/          # 1ª canonicalização
    │   │   ├── canonical_output_run2a.ttl
    │   │   ├── run_manifest_run2a.json
    │   │   ├── idempotency_run2a.json
    │   │   ├── isomorphism_run2a.json
    │   │   ├── stdout_run2a.txt
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   │
    │   ├── run2b_canonicalize/          # 2ª canonicalização (determinismo)
    │   │   ├── canonical_output_run2b.ttl
    │   │   ├── run_manifest_run2b.json
    │   │   ├── isomorphism_run2b.json
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   │
    │   ├── run3_normalize_canonicalize/ # Normalize + canon (validate only)
    │   │   ├── canonical_output_run3.ttl
    │   │   ├── run_manifest_run3.json
    │   │   ├── isomorphism_run3.json
    │   │   ├── normalize_log_run3.json
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   │
    │   └── run4_normalize_canonicalize/ # Normalize + canon (auto-fix)
    │       ├── canonical_output_run4.ttl
    │       ├── run_manifest_run4.json
    │       ├── normalize_log_run4.json
    │       ├── export-log.json
    │       └── audit-log-session-*.json/.md
    │
    ├── 30_gates/                        # Verification gates (JSON)
    │   ├── gate_determinism.json
    │   ├── gate_isomorphism.json
    │   └── gate_idempotency.json
    │
    ├── 40_tests/                        # Test execution artifacts
    │   ├── pytest_summary.json          # SOURCE OF TRUTH para números
    │   ├── pytest_full.txt              # Output completo do pytest
    │   ├── pytest_output.txt            # Output resumido (PASSED lines)
    │   ├── pytest_collection.txt        # Lista de testes coletados
    │   └── pytest_cmd.txt               # Comando exato executado
    │
    ├── 50_qa/                           # QA artifacts
    │   ├── QA_PLAN_RCNN.md
    │   ├── QA_CHECKLIST_FINAL_RCNN.md
    │   ├── COVERAGE_REPORT.txt
    │   └── DESIGNDOC_CONFORMANCE_MATRIX_RCNN.md
    │
    ├── 60_reference/                    # Referências externas (vazio por design)
    │   └── README.md
    │
    ├── 90_legacy/                       # Notas de migração (vazio por design)
    │   └── README.md
    │
    ├── RC_vNN_CANON_SUMMARY.md          # Resumo executivo
    ├── results_index_RC_vNN_CANON.md    # Índice de resultados
    ├── rcNN_result.json                 # Resultado machine-readable
    └── CHECKSUMS_SHA256.txt             # SHA256 de TODOS os arquivos
```

---

## Arquivos Source of Truth

### 1. pytest_summary.json

Única fonte para números de teste. Todos os documentos derivados (COVERAGE_REPORT,
QA_CHECKLIST, FINAL_REPORT, declaration) DEVEM referenciar este arquivo.

```json
{
  "test_suite": "tests/1-uc-ontology",
  "timestamp": "2026-02-27T04:26:56.882557+00:00",
  "results": {
    "collected": 963,
    "passed": 963,
    "failed": 0,
    "skipped": 0,
    "errors": 0,
    "duration_seconds": 65.43
  },
  "coverage": {
    "total_percent": 95.04,
    "threshold_required": 95.0,
    "passed": true
  }
}
```

### 2. BASELINE_POST_SHA256.json

Contém hash SHA256 de **todos** os artefatos gerados pelo pipeline.
Usado como prova de integridade pós-execução.

### 3. CHECKSUMS_SHA256.txt

Hash SHA256 de **todos** os arquivos do bundle (incluindo docs gerados depois).
Regenerado no final após criação de todos os arquivos.

### 4. Gate JSONs (30_gates/)

Arquivos machine-readable com status PASS/FAIL.

---

## Gates Obrigatórios

| # | Gate | File | Critério de Sucesso |
|---|------|------|---------------------|
| 1 | **Determinism** | `gate_determinism.json` | SHA256(Run2a) == SHA256(Run2b) |
| 2 | **Isomorphism** | `gate_isomorphism.json` | Input ≅ Output (rdflib.compare) |
| 3 | **Idempotency** | `gate_idempotency.json` | f(f(x)) == f(x) — hashes match |
| 4 | **Test Suite** | `pytest_summary.json` | collected == passed, failed == 0 |
| 5 | **Coverage** | `pytest_summary.json` | coverage >= threshold |

Todos os gates são executados automaticamente pelo script `scripts/run_rcNN.py`.
Se qualquer gate falhar: **FAIL FAST** — interromper e investigar.

---

## Runs do Pipeline

| Run | Operação | Propósito | Output Hash esperado |
|-----|----------|-----------|----------------------|
| **Run 2a** | Canonicalize | Primeira execução | CANON_SHA |
| **Run 2b** | Canonicalize | Confirmar determinismo | CANON_SHA (idêntico) |
| **Run 3** | Normalize + Canon (validate) | Detectar problemas sem corrigir | CANON_SHA (idêntico) |
| **Run 4** | Normalize + Canon (auto-fix) | Aplicar correções | RUN4_SHA (diferente!) |

**Importante**: Run 2a/2b/3 DEVEM produzir hash idêntico. Run 4 é diferente porque aplica correções.

---

## Regras de Consistência

### Single Source of Truth

```
pytest_summary.json  →  números de teste e cobertura
BASELINE_POST_SHA256.json  →  hashes dos artefatos do pipeline
CHECKSUMS_SHA256.txt  →  hashes de todos os arquivos do bundle
```

### Proibições

- Números "hardcoded" em docs derivados sem referenciar fonte
- `TO_BE_COMPUTED` em arquivos finalizados
- Duplicação de artefatos entre diretórios
- Testes em domínio fora de `tests/1-uc-ontology`
- Copiar artefatos de RCs anteriores (clean-room)

---

## Workflow de Criação

Executado pelo script `scripts/run_rcNN.py`:

```
FASE 1: Create Structure     → 00_meta/, 20_runs/, 30_gates/, 40_tests/, 50_qa/
FASE 2: Determinism           → Run2a + Run2b, gate_determinism.json
FASE 3: Normalize + Canon     → Run3 (validate), Run4 (auto-fix)
FASE 4: Gates                 → gate_isomorphism.json, gate_idempotency.json
FASE 5: Tests + Coverage      → pytest_summary.json, pytest_full.txt
FASE 6: Evidence Bundle       → BASELINE_POST, CHECKSUMS, rcNN_result.json
```

Após execução do script, rodar `scripts/fill_rcNN_bundle.py` para gerar:

```
FASE 7: Fill Bundle           → 00_meta/*, 10_proofs/*, 40_tests extras,
                                 50_qa/*, 60_reference/, 90_legacy/
FASE 8: Regenerate Checksums  → CHECKSUMS_SHA256.txt com todos os arquivos
```

---

## Scripts

| Script | Propósito |
|--------|-----------|
| `scripts/run_rcNN.py` | Execução principal do pipeline (Fases 1-6) |
| `scripts/fill_rcNN_bundle.py` | Gera docs faltantes (Fases 7-8) |
| `scripts/_check_rcNN.py` | Verificação final do bundle (temporário) |

---

## Checklist de Finalização

```markdown
- [ ] FASE 1-6 executadas via run_rcNN.py
- [ ] FASE 7-8 executadas via fill_rcNN_bundle.py
- [ ] Todos 3 gates PASS (determinism, isomorphism, idempotency)
- [ ] pytest: collected == passed, failed == 0, skipped == 0
- [ ] coverage >= threshold (95% para RC13+)
- [ ] BASELINE_POST_SHA256.json sem TO_BE_COMPUTED
- [ ] CHECKSUMS_SHA256.txt regenerado após fill
- [ ] 0 arquivos faltando vs RC anterior (verificar com script)
- [ ] 60_reference/ e 90_legacy/ presentes com README.md
- [ ] RC_vNN_CANON_SUMMARY.md e results_index presentes
```

---

*Template Version: 2.0*  
*Based on: RC_v13_CANON execution (2026-02-27)*  
*Supersedes: v1.0 (RC_v11_CANON)*
