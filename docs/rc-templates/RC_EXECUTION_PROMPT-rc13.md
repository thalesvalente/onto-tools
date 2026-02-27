# Prompt para Execução de RC Canônico (v2.0)

**Prompt de Sistema para Agente AI executar RC_vNN_CANON**

*Based on: RC_v13_CANON execution (2026-02-27)*

---

## Prompt Base

```
Execute o protocolo RC_vNN_CANON completo para o projeto OntoTools.

## Contexto

- Workspace: onto-tools-artigo
- Python: Conda environment `onto-tools-artigo` (Python 3.12.12)
- CLI: OntoTools 3.0.0
- Ontologia de entrada: data/examples/energy-domain-ontology.ttl
- Escopo de testes: tests/1-uc-ontology
- Coverage threshold: 95%

## PRÉ-REQUISITOS

1. Verificar que o RC anterior (RC_v{NN-1}_CANON) existe e está completo
2. Anotar hashes do RC anterior para comparação
3. Garantir que não há mudanças na ontologia de entrada entre RCs

## PASSO 1 — Criar script de execução

Criar `scripts/run_rcNN.py` baseado em `scripts/run_rc13.py`.
O script executa as Fases 1-6 automaticamente:

### FASE 1 - CREATE STRUCTURE
- Criar estrutura outputs/logs/RC_vNN_CANON/YYYYMMDD_HHMMSS/
- Subdiretórios: 00_meta, 10_proofs, 20_runs/{run2a,run2b,run3,run4},
  30_gates, 40_tests, 50_qa
- Salvar env_snapshot.json em 00_meta/
- Calcular SHA256 da ontologia de entrada
- Contar triples da ontologia

### FASE 2 - DETERMINISM
- Executar canonicalização 2x (Run2a, Run2b) via OntoToolsFacade
- Para cada run: load_ontology → canonicalize_ontology → generate_review_output
- Verificar: SHA256(Run2a) == SHA256(Run2b)
- Gerar idempotency_run2a.json, isomorphism_run2a.json, isomorphism_run2b.json
- Se diferir: FAIL FAST — não prosseguir

### FASE 3 - NORMALIZE + CANONICALIZE
- Run 3 (validate_only): normalizar sem aplicar fixes, depois canonicalizar
  - Gerar normalize_log_run3.json, isomorphism_run3.json
  - SHA256 deve ser IDÊNTICO ao Run2a/2b
- Run 4 (auto_fix): normalizar com fixes aplicados, depois canonicalizar
  - Gerar normalize_log_run4.json
  - SHA256 será DIFERENTE (743 triples modificadas)

### FASE 4 - GATES
- Gerar gate_determinism.json (hash 2a == hash 2b)
- Gerar gate_isomorphism.json (input ≅ output para cada run)
- Gerar gate_idempotency.json (f(f(x)) == f(x))
- Se qualquer gate FAIL: investigar antes de prosseguir

### FASE 5 - TESTS
- Executar: pytest tests/1-uc-ontology -v --tb=short
    --cov=src/onto_tools --cov-report=term-missing --cov-report=json
- Critério: 0 failed, 0 skipped, coverage >= threshold
- Gerar pytest_summary.json como SOURCE OF TRUTH
- Salvar pytest_full.txt (output completo)

### FASE 6 - EVIDENCE
- Gerar BASELINE_POST_SHA256.json com hash de todos os artefatos gerados
- Gerar rcNN_result.json com resumo machine-readable
- Gerar RC_vNN_CANON_SUMMARY.md
- Gerar results_index_RC_vNN_CANON.md
- Gerar CHECKSUMS_SHA256.txt (PARCIAL — será regenerado no Passo 2)

## PASSO 2 — Executar run_rcNN.py

```bash
conda run -n onto-tools-artigo python scripts/run_rcNN.py
```

## PASSO 3 — Criar script de preenchimento

Criar `scripts/fill_rcNN_bundle.py` baseado em `scripts/fill_rc13_bundle.py`.
O script cria todos os arquivos de documentação faltantes:

### FASE 7 - FILL BUNDLE

#### 00_meta/ (6 arquivos):
- BASELINE_PRE_SHA256.json
- ENV_SNAPSHOT.md
- INPUT_SNAPSHOT.md
- TOOL_VERSIONS.md
- RC_LAYOUT_STANDARD.md
- COMMAND_LOG.md

#### 10_proofs/ (7 arquivos):
- declaration_RC_vNN_CANON.md
- IMMUTABILITY_PROOF.json
- NORMALIZATION_REPORT_FROM_LOG.md
- ARTICLE_COMPATIBILITY_PROOF_STRONG_RCNN.md
- TRACEABILITY_MATRIX_RCNN.md
- EVIDENCE_MAP_RCNN.md
- RC_vNN_FINAL_REPORT.md

#### 20_runs/ (archivos complementares):
- run_manifest_run2a.json, run_manifest_run2b.json,
  run_manifest_run3.json, run_manifest_run4.json
- stdout_run2a.txt
- isomorphism_run2b.json (se não gerado pelo script principal)

#### 40_tests/ (3 arquivos):
- pytest_cmd.txt (comando exato)
- pytest_collection.txt (testes coletados)
- pytest_output.txt (linhas PASSED resumidas)

#### 50_qa/ (4 arquivos):
- QA_PLAN_RCNN.md
- QA_CHECKLIST_FINAL_RCNN.md
- COVERAGE_REPORT.txt
- DESIGNDOC_CONFORMANCE_MATRIX_RCNN.md

#### Diretórios placeholder:
- 60_reference/README.md
- 90_legacy/README.md

### FASE 8 - REGENERATE CHECKSUMS
- Recalcular CHECKSUMS_SHA256.txt com TODOS os arquivos do bundle

## PASSO 4 — Executar fill_rcNN_bundle.py

```bash
conda run -n onto-tools-artigo python scripts/fill_rcNN_bundle.py
```

## PASSO 5 — Verificação final

Criar e executar script temporário de verificação:

```bash
conda run -n onto-tools-artigo python scripts/_check_rcNN.py
```

O script deve verificar:
- 0 arquivos faltantes vs RC anterior
- Hashes dos canonical outputs coincidem com RC anterior
- Todos 3 gates PASS
- pytest_summary.json: passed == collected, failed == 0
- coverage >= threshold
- CHECKSUMS_SHA256.txt: todos os hashes validados

Apagar o script de verificação após execução.

## Regras

1. pytest_summary.json é SOURCE OF TRUTH para números de teste
2. BASELINE_POST_SHA256.json é SOURCE OF TRUTH para hashes
3. Docs derivados DEVEM referenciar as fontes, não hardcode
4. Se encontrar inconsistência: CORRIGIR antes de prosseguir
5. Nunca deixar TO_BE_COMPUTED em arquivos finalizados
6. Se o input SHA256 mudou vs RC anterior: documentar em
   ARTICLE_COMPATIBILITY_PROOF como "ontology evolution"
7. Run 2a/2b/3 DEVEM ter hash idêntico; Run 4 pode diferir
8. Usar clean-room: NUNCA copiar artefatos de RCs anteriores
```

---

## Variações

### Modo "Done Done" (Máximo Rigor)

Adicionar ao prompt:

```
Modo: DONE DONE (à prova de revisor chato)

Requisitos adicionais:
- Verificar CADA número em CADA documento contra pytest_summary.json
- Comparar arquivo por arquivo, pasta por pasta, com RC anterior
- Executar script de verificação final
- Documentar TODAS as decisões tomadas
- Garantir 60_reference/ e 90_legacy/ existem com README.md
```

### Modo "Quick Validation"

```
Modo: QUICK VALIDATION (apenas verificar RC existente)

Executar apenas:
- Listar RC13 vs RC12 (checagem de paridade estrutural)
- Verificar hash dos canonical outputs
- Verificar gates (3 JSONs)
- Verificar pytest_summary.json
- Verificar CHECKSUMS_SHA256.txt
```

### Modo "Incremental" (RC sobre RC anterior)

```
Modo: INCREMENTAL (baseado em RC anterior)

- Usar RC_v{NN-1}_CANON como baseline de comparação
- Documentar deltas (novos testes, mudanças de threshold, etc.)
- Confirmar que hashes de input/canonical são idênticos
- Manter rastreabilidade cruzada
```

---

## Scripts de Referência (RC13)

| Script | Propósito | Mantido? |
|--------|-----------|----------|
| `scripts/run_rc13.py` | Execução FASES 1-6 do pipeline | Sim |
| `scripts/fill_rc13_bundle.py` | Preenchimento FASES 7-8 (docs) | Sim |

Para criar RC14, duplicar e adaptar estes scripts:

```bash
cp scripts/run_rc13.py scripts/run_rc14.py
cp scripts/fill_rc13_bundle.py scripts/fill_rc14_bundle.py
# Editar: versão, timestamp, threshold, dados derivados
```

---

## Checklist Pós-Execução

```markdown
## Pipeline (run_rcNN.py)
- [ ] FASE 1: Estrutura criada com 9 subdiretórios
- [ ] FASE 2: Run2a + Run2b determinísticos (hash idêntico)
- [ ] FASE 3: Run3 (validate) + Run4 (auto-fix) executados
- [ ] FASE 4: 3 gates PASS (determinism, isomorphism, idempotency)
- [ ] FASE 5: pytest collected == passed, failed == 0, coverage >= threshold
- [ ] FASE 6: BASELINE_POST, rcNN_result.json, SUMMARY gerados

## Bundle (fill_rcNN_bundle.py)
- [ ] FASE 7: 00_meta/ completo (6 arquivos)
- [ ] FASE 7: 10_proofs/ completo (8 arquivos com BASELINE_POST)
- [ ] FASE 7: 20_runs/ com manifests e stdout
- [ ] FASE 7: 40_tests/ com pytest_cmd/collection/output
- [ ] FASE 7: 50_qa/ completo (4 arquivos)
- [ ] FASE 7: 60_reference/ e 90_legacy/ com README.md
- [ ] FASE 8: CHECKSUMS_SHA256.txt regenerado (≈60 entradas)

## Verificação Final
- [ ] 0 arquivos faltantes vs RC anterior
- [ ] Hashes canonicais coincidem com RC anterior
- [ ] CHECKSUMS integridade: todos hashes validados
- [ ] Script _check_rcNN.py: ALL CHECKS PASS
- [ ] Script _check_rcNN.py removido após verificação
```

---

## Dados de Referência (RC13)

| Métrica | Valor |
|---------|-------|
| Input SHA256 | `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE` |
| Canon SHA256 (2a/2b/3) | `E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49` |
| Run4 SHA256 (auto-fix) | `B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D` |
| Triples | 6803 |
| Tests | 963 passed / 0 failed |
| Coverage | 95.04% (threshold 95%) |
| Arquivos no bundle | ~60 |
| Gates | 3/3 PASS |

---

*Prompt Version: 2.0*  
*Based on: RC_v13_CANON execution (2026-02-27)*  
*Supersedes: v1.0 (RC_v11_CANON)*
