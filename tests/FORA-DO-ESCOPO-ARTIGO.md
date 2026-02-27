# Mapeamento de Testes: Escopo do Artigo vs. Fora do Escopo

> **Como usar este documento**
> A Parte 1 lista exatamente o que **DEVE PERMANECER** no repositório.
> A Parte 2 lista exatamente o que **DEVE SER REMOVIDO**, com os comandos prontos.
> Nenhuma decisão está em aberto — cada item já tem ação definida.

---

## PARTE 1 — Testes que compõem o artigo (`tests/1-uc-ontology/`)

Suite executada no RC_v12_CANON: **938 testes, 0 falhas, 94.05% de cobertura**  
Comando: `pytest tests/1-uc-ontology -v --tb=short`

### Arquivos de teste (38 arquivos, ~17.749 linhas)

#### CLI (2 arquivos — 837 linhas)

| Arquivo | Linhas | O que testa |
|---|---|---|
| `cli/test_cli_commands.py` | 541 | Comandos de linha de comando, formatação de saída |
| `cli/test_cli_menu.py` | 296 | Menu interativo, navegação, ações |

#### E2E — End-to-End (2 arquivos — 553 linhas)

| Arquivo | Linhas | O que testa |
|---|---|---|
| `e2e/test_canonicalization_e2e.py` | 165 | Canonicalização completa ponta-a-ponta, idempotência |
| `e2e/test_cli_simulation_scenarios.py` | 388 | Cenários C1–C5 via simulação de CLI |

#### Integration (6 arquivos — 1.727 linhas)

| Arquivo | Linhas | O que testa |
|---|---|---|
| `integration/test_facade_flows.py` | 163 | Fluxos via fachada (canonicalize, normalize) |
| `integration/test_normalization_complete.py` | 226 | Normalização completa com rulebook real |
| `integration/test_real_coverage.py` | 581 | Cobertura de caminhos reais (módulos de domínio) |
| `integration/test_uc104_verification.py` | 307 | Verificação UC-1.04 (manifesto condicional) |
| `integration/test_verification_integration.py` | 321 | Gates: determinismo, isomorfismo, idempotência |
| `integration/test_verify_only_flow.py` | 129 | Fluxo validate-only (auto-fix desabilitado) |

#### Unit (28 arquivos — 14.632 linhas)

| Arquivo | Linhas | O que testa |
|---|---|---|
| `unit/test_adapters.py` | 390 | Adaptadores RDF/rdflib |
| `unit/test_audit_formatter.py` | 592 | Formatador de log de auditoria |
| `unit/test_canonicalizer.py` | 942 | Canonicalizador (núcleo) |
| `unit/test_canonicalizer_determinism_v9.py` | 210 | Determinismo byte-a-byte (3 runs) |
| `unit/test_facade.py` | 308 | Fachada de aplicação |
| `unit/test_naming_validator.py` | 1.569 | Validador de nomenclatura |
| `unit/test_normalize_reporting_invariance.py` | 452 | Invariância de relatórios entre modos |
| `unit/test_normalizer.py` | 1.180 | Normalizador (núcleo) |
| `unit/test_ontology_graph.py` | 762 | Grafo RDF interno |
| `unit/test_preflabel_correction.py` | 224 | Correção de prefLabel |
| `unit/test_protege_serializer_coverage.py` | 271 | Cobertura do serializador Protégé |
| `unit/test_protege_style_alignment.py` | 345 | Alinhamento de estilo Protégé |
| `unit/test_protege_style_serializer_snapshot.py` | 208 | Snapshot do serializador Protégé |
| `unit/test_protege_style_validity.py` | 297 | Validade de saída estilo Protégé |
| `unit/test_quality_domainattribute_constraints.py` | 829 | Restrições de atributos de domínio |
| `unit/test_quality_ifc_constraints.py` | 287 | Restrições IFC |
| `unit/test_quality_validator.py` | 1.895 | Validador de qualidade (QualityValidator) |
| `unit/test_rdflib_adapter.py` | 270 | Adaptador rdflib |
| `unit/test_sparql_engine.py` | 278 | Motor SPARQL (usado em normalização) |
| `unit/test_title_case.py` | 347 | Regra TitleCase |
| `unit/test_uri_resolver.py` | 585 | Resolução de URIs/IRIs |
| `unit/test_verification_evidence.py` | 260 | Escritor de evidências |
| `unit/test_verification_hasher.py` | 180 | Hasher SHA-256 |
| `unit/test_verification_idempotency.py` | 462 | Gate de idempotência |
| `unit/test_verification_isomorphism.py` | 341 | Gate de isomorfismo RDF |
| `unit/test_verification_manifest.py` | 464 | Escritor de manifesto |
| `unit/test_verification_rc_workflow.py` | 517 | Workflow RC (pipeline completo) |
| `unit/test_verify_only.py` | 167 | Modo verify-only |

### Suporte (não são testes, mas fazem parte da suite)

| Item | Descrição |
|---|---|
| `tests/__init__.py` | `__init__.py` da raiz de `tests/` — **PERMANECE** |
| `conftest.py` (raiz UC-1) | Fixtures globais do UC-1 |
| `cli/__init__.py`, `cli/conftest.py` | Init e fixtures de CLI |
| `data/__init__.py` | Init do diretório de dados |
| `integration/__init__.py` | Init dos testes de integração |
| `e2e/conftest.py` | Fixtures de E2E |
| `data/ontologies/valid/*.ttl` | Ontologias válidas para testes |
| `data/ontologies/invalid/*.ttl` | Ontologias inválidas para testes negativos |
| `data/rules/*.json` | Rulebooks mínimos de teste |
| `fixtures/*.ttl` | Fixtures de domínio (IFC, Protégé, etc.) |
| `coverage/` (vazio) | Pasta criada por `coverage.py` — **FICA** (vazia, inofensiva) |

---

---

## PARTE 2 — O que remover (ação definida, sem ambiguidade)

### ⚠️ Atenção: conflito de nome de arquivo

`tests/1-uc-ontology/unit/test_sparql_engine.py` (278 linhas) **PERMANECE** — testa
o motor SPARQL usado internamente pela normalização (escopo UC-1).

`tests/2-uc-sparql/unit/test_sparql_engine.py` (110 linhas) **É REMOVIDO** junto com
todo o diretório `2-uc-sparql/`. São arquivos diferentes com o mesmo nome.

---

### Ação 1 — Remover `tests/2-uc-sparql/` (inteiro)

**Motivo:** testa UC-2 (consultas SPARQL interativas ao usuário), fora do escopo do artigo.

```powershell
Remove-Item -Recurse -Force "tests\2-uc-sparql"
```

Arquivos eliminados:
- `__init__.py`, `conftest.py`
- `integration/__init__.py`, `integration/test_sparql_pipeline.py` (186 linhas)
- `unit/__init__.py`
- `unit/test_sparql_adapter.py` (151 linhas)
- `unit/test_sparql_engine.py` (110 linhas) ← **diferente** do `1-uc-ontology/unit/test_sparql_engine.py`
- `unit/test_sparql_query_service.py` (311 linhas)
- `unit/test_template_manager.py` (573 linhas)
- `data/.gitignore`
- todos `__pycache__/`

---

### Ação 2 — Remover `tests/3-uc-export/` (inteiro)

**Motivo:** testa UC-3 (exportação JSON/XLSX), fora do escopo do artigo.

```powershell
Remove-Item -Recurse -Force "tests\3-uc-export"
```

Arquivos eliminados:
- `__init__.py`
- `test_json_exporter.py` (316 linhas)
- `test_sparql_integration.py` (584 linhas)
- `test_xlsx_exporter.py` (351 linhas)
- todos `__pycache__/`

---

### Ação 3 — Remover `tests/5-uc-comparison/` (inteiro)

**Motivo:** testa UC-5 (comparação/diff de ontologias), fora do escopo do artigo.

```powershell
Remove-Item -Recurse -Force "tests\5-uc-comparison"
```

Arquivos eliminados:
- `__init__.py`
- `test_comparators.py` (276 linhas)
- `test_diff_engine.py` (379 linhas)
- todos `__pycache__/`

---

### Ação 4 — Remover `tests/coverage/` (raiz, inteiro)

**Motivo:** cópia de relatório HTML gerada por `coverage.py`. Não é código de teste.
Artefato de saída não pertence a `tests/`. O relatório autorizado está em
`outputs/reports/coverage/` (gerado pelo RC_v12_CANON).

> ⚠️ **Não confundir com `tests/1-uc-ontology/coverage/`** — esta subpasta está vazia
> e é criada automaticamente pelo pytest-cov; não deve ser removida.

> ℹ️ `pytest.ini` já tem `norecursedirs = coverage`, portanto `tests/coverage/` nunca
> foi coletado pelo pytest. A remoção é higiene de repositório, não afeta resultados.

```powershell
Remove-Item -Recurse -Force "tests\coverage"
```

---

### Ação 5 — Remover `tests/test_rulebook_resolver.py`

**Motivo:** testa resolução de path do arquivo de configuração do rulebook (infraestrutura
interna). Este comportamento já é coberto implicitamente pelos testes de integração em
`1-uc-ontology/integration/` que carregam rulebooks reais. Não acrescenta evidência
direta às afirmações do artigo.

```powershell
Remove-Item -Force "tests\test_rulebook_resolver.py"
```

---

### Ação 6 — Atualizar `pytest.ini`

**Motivo:** `testpaths = tests` faz o pytest descobrir todos os diretórios sob `tests/`.
Após as Ações 1–3 removerem os diretórios UC-2, UC-3 e UC-5, o pytest já não os
encontrará — mas restringir o `testpaths` explicitamente torna o escopo inequívoco
independente de qualquer diretório que venha a existir no futuro.

> ℹ️ Nota: `norecursedirs = coverage` já está configurado e protege `tests/coverage/`
> desde antes. A mudança de `testpaths` é complementar, não redundante.

Localização: `pytest.ini` na raiz do projeto.

Alterar:
```ini
# ANTES
testpaths = tests

# DEPOIS
testpaths = tests/1-uc-ontology
```

---

### Ação 7 — Atualizar `coverage/coverage.xml` e `coverage/htmlcov/`

**Motivo:** o `coverage.xml` atual (gerado em 2026-02-25) mede o pacote inteiro
(`5.949 linhas`, `72.48%`). Após restringir o escopo de testes, regerar com:

```powershell
pytest tests/1-uc-ontology --cov=src/onto_tools/domain/ontology --cov=src/onto_tools/application/verification --cov-report=xml:coverage/coverage.xml --cov-report=html:coverage/htmlcov
```

O resultado esperado: **~2.118 statements, 94.05%** — consistente com o artigo.

---

## Resumo das ações

| # | Ação | Tipo | Impacto |
|---|---|---|---|
| 1 | `Remove-Item -Recurse tests\2-uc-sparql` | Remoção de diretório | −1.331 linhas de teste |
| 2 | `Remove-Item -Recurse tests\3-uc-export` | Remoção de diretório | −1.251 linhas de teste |
| 3 | `Remove-Item -Recurse tests\5-uc-comparison` | Remoção de diretório | −655 linhas de teste |
| 4 | `Remove-Item -Recurse tests\coverage` | Remoção de artefato | — |
| 5 | `Remove-Item tests\test_rulebook_resolver.py` | Remoção de arquivo | −1 arquivo |
| 6 | Editar `pytest.ini`: `testpaths` | Configuração | Escopo restrito a UC-1 |
| 7 | Regerar `coverage/coverage.xml` | Medição | 72.48% → 94.05% |

Após todas as ações: `pytest tests/1-uc-ontology` deve continuar produzindo
**938 testes, 0 falhas, 94.05%** — idêntico ao RC_v12_CANON.

---

## PARTE 3 — `outputs/reports/`: tudo pode ser removido

Todos os arquivos em `outputs/reports/` são artefatos de fases anteriores ao RC_v12_CANON
(novembro/2025 – janeiro/2026). **Nenhum é citado no artigo** e nenhum faz parte da cadeia
de rastreabilidade. A evidência do artigo está em `outputs/logs/RC_v12_CANON/`.

| Arquivo / Pasta | Data | O que é | Ação |
|---|---|---|---|
| `coverage/` (htmlcov) | 2025-11-14 | Relatório HTML do pacote completo — 113 módulos, escopo antigo. **Não é o 94.05%** do artigo. | Remover |
| `RELATORIO-TESTES-NUCLEO-1.md` | 2025-11-14 | Relatório de **113 testes** (versão v3.0, branch develop). Supersedido pelo RC12 com 938 testes. | Remover |
| `PLANO-NORMALIZACAO-100.md` | 2025-11-14 | Plano de normalização (documento de planejamento). Não é evidência. | Remover |
| `query-edo_get_hierarchy-20251218_191013.json` | 2025-12-18 | Resultado de query SPARQL de hierarquia. Não citado no artigo. | Remover |
| `RC_INTEGRATION_AUDIT_20260130.md` | 2026-01-30 | Auditoria que concluiu que scripts RC_v8 **NÃO estavam integrados** ao pipeline. Documento de processo intermediário. | Remover |

> ⚠️ **Atenção especial ao `coverage/`**: contém `index.html` que reporta a cobertura
> do pacote inteiro (escopo pre-RC12). Se mantido, um revisor pode confundir com o
> relatório de cobertura do artigo (94.05%). A remoção elimina risco de confusão.

```powershell
Remove-Item -Recurse -Force "outputs\reports\coverage"
Remove-Item -Force "outputs\reports\RELATORIO-TESTES-NUCLEO-1.md"
Remove-Item -Force "outputs\reports\PLANO-NORMALIZACAO-100.md"
Remove-Item -Force "outputs\reports\query-edo_get_hierarchy-20251218_191013.json"
Remove-Item -Force "outputs\reports\RC_INTEGRATION_AUDIT_20260130.md"
```

---

## PARTE 3b — `outputs/logs/UC104_AUDIT*`: artefatos intermediários — remover

Existem duas sessões de auditoria anteriores ao RC_v12_CANON, geradas em 2026-01-31
durante o desenvolvimento da funcionalidade UC-104 (manifesto condicional):

| Pasta | Testes | Triples | Cobertura | Status |
|---|---|---|---|---|
| `UC104_AUDIT/20260131_194057/` | 14 (UC104) / 904 (total à época) | 6.727 | 27.16% (escopo parcial) | Superado |
| `UC104_AUDIT_PHASE2_20260131_202107/` | 14 (UC104) / 1.106 (total à época) | 6.727 | — | Superado |
| **RC_v12_CANON (artigo)** | **938** | **6.803** | **94.05%** | **✅ Evidência final** |

> ⚠️ **Risco de confusão**: os números são diferentes dos do artigo em três dimensões:
> - Testes: 904 / 1.106 vs. **938** (artigo)
> - Triples: 6.727 vs. **6.803** (artigo) — o EDO foi atualizado entre as sessões
> - Cobertura: 27.16% vs. **94.05%** (artigo) — escopo totalmente diferente
>
> Se estes arquivos permanecerem, qualquer revisor que os encontrar verá números
> inconsistentes com o artigo sem contexto para interpretá-los.

**O que preservar dos UC104_AUDIT antes de remover:**
Os 14 testes de `test_uc104_verification.py` **já estão incorporados** ao suite UC-1
(38 arquivos, Parte 1 deste documento) e continuam passando nos 938 do RC12.
Os logs de auditoria em si não precisam ser mantidos.

```powershell
Remove-Item -Recurse -Force "outputs\logs\UC104_AUDIT"
Remove-Item -Recurse -Force "outputs\logs\UC104_AUDIT_PHASE2_20260131_202107"
```

---

## PARTE 4 — Evidências primárias fora de `tests/` que NÃO devem ser removidas

Estes arquivos estão em `outputs/logs/RC_v12_CANON/20260203_221711/` e são a fonte
primária dos números citados no artigo. **Não devem ser deletados, movidos ou alterados.**

| Arquivo | Caminho completo | Contém |
|---|---|---|
| `pytest_full.txt` | `40_tests/pytest_full.txt` | Output bruto do pytest: linha `938 passed in 75.30s` e tabela `TOTAL 94.05%` |
| `pytest_summary.json` | `40_tests/pytest_summary.json` | JSON estruturado: `collected=938, passed=938, failed=0, coverage=94.05` |
| `gate_determinism.json` | `30_gates/gate_determinism.json` | Gate de byte-determinism: hashes run2a == run2b |
| `gate_isomorphism.json` | `30_gates/gate_isomorphism.json` | Gate de isomorfismo: 6.803 triples in/out |
| `gate_idempotency.json` | `30_gates/gate_idempotency.json` | Gate de idempotência C(C(G))=C(G) |
| `RC_v12_CANON_SUMMARY.md` | raiz da sessão | Resumo consolidado de todos os resultados |

### Cadeia de rastreabilidade completa

```
pytest_full.txt  (raw output)
    └→ pytest_summary.json  (structured)
            └→ paper/v3/evidence-ledger.md  (E-040, E-041)
                    └→ paper/v3/claims-ledger.md  (C-008)
                            └→ paper/v3/appendix-traceability.md
                                    └→ paper/section-6.md  (artigo)
```

Qualquer remoção de `outputs/logs/RC_v12_CANON/` quebra essa cadeia.

---

---

## PARTE 5 — `scripts/`: mapeamento de escopo

### ✅ Dentro do escopo RC_v12_CANON (manter)

| Script | Função |
|---|---|
| `generate_rc12_run4.py` | Gera run4 (auto-fix) do RC_v12 — pipeline direto |
| `gen_norm_report.py` | Gera relatório de normalização a partir de log RC_v12 |
| `isomorphism_check.py` | Gate de isomorfismo RDF (correspondente a `gate_isomorphism.json`) |
| `fix_run3_manifest.py` | Corrige manifesto run3 RC_v12 |
| `menu.bat` / `menu.ps1` | Execução do pipeline interativo |
| `setup.ps1` / `setup_env.ps1` | Setup do ambiente |
| `README.md` | Documentação dos scripts |

### ❌ Fora do escopo — era pre-RC_v12 (candidatos a remoção)

| Script | Era | O que era |
|---|---|---|
| `rc_v9_runs.py` | RC_v9 | Executa runs de reprodutibilidade RC_v9 |
| `create_rc_v8_compat.py` | RC_v8 | Cria cópias byte-idênticas RC_v8_COMPAT |
| `gen_immutability_proof.py` | RC_v8 | Gera `RC_V8_IMMUTABILITY_PROOF.json` |
| `fase0_inventory.py` | RC_v8/v9 | Inventário forense RC_v8 e RC_v9 |
| `fase4_parity_strong.py` | RC_v8 | Paridade RC_v8 vs RC_V8_COMPAT |
| `generate_baseline.py` | pré-RC_v12 | Baseline de integridade pré-limpeza |
| `docfix_baseline.py` | RC_v9 | Baseline SHA256 dos arquivos RC_v9 |
| `docfix_immutability_proof.py` | RC_v9 | Prova de imutabilidade DOCFIX |
| `rc10_baseline.py` | RC_v10 | Baseline RC_v10 |
| `rc10_gates.py` | RC_v10 | Gates RC_v10 |
| `rc10_immutability_proof.py` | RC_v10 | Prova de imutabilidade RC_v10 vs RC_v8 |
| `rc10_rc_v8_compat.py` | RC_v10 | Cópia byte-idêntica RC_v8 para RC_v10 |
| `create_pytest_summary.py` | RC_v9 | Cria pytest summary para RC_v9 |

### ❌ Fora do escopo — demos/testes de infraestrutura (candidatos a remoção)

Exercitam funcionalidade de menu/rulebook (UI interativa) — não são evidência do artigo
e são cobertos pelos testes formais em `tests/1-uc-ontology/`.

| Script | O que é |
|---|---|
| `demo_error_handling.py` | Demo visual: erro vs sucesso no rulebook |
| `demo_menu_protection.py` | Demo visual: bloqueio de menu com config errada |
| `demo_rulebook_config.py` | Demo: exibe qual rulebook foi carregado |
| `test_menu_rulebook_display.py` | Testa exibição do rulebook no menu |
| `test_menu_validation.py` | Testa bloqueio de menu por rulebook inválido |
| `test_rulebook_error_messages.py` | Testa mensagens de erro do rulebook |

> ℹ️ Nota: `scripts/outputs/` e `scripts/patches/v8/` foram removidos em 2026-02-26
> — não tinham referências no código ativo.

---

---

---

## PARTE 6 — `outputs/`: mapeamento das pastas restantes

As PARTES 3, 3b e 4 já cobrem `outputs/reports/`, `outputs/logs/UC104_AUDIT*` e
`outputs/logs/RC_v12_CANON/`. Esta parte mapeia o restante.

---

### 6.1 — `outputs/cli_simulation/`

Contém 5 sessões de simulação de CLI (cenários C1–C5):

| Pasta | Data/hora | Conteúdo | Status |
|---|---|---|---|
| `20260204_001508/` | 2026-02-04 00:15 | C1-C5 + cross_validation + logs + SUMMARY.md (8,6 KB) | ✅ Manter — verificação pós-CANON |
| `cli_test_02/` | desenvolvimento | C1-C5 + SUMMARY.md (9 KB) | ❌ Remover — era pré-CANON |
| `cli_test_03/` | desenvolvimento | C1-C5 + SUMMARY.md (8,7 KB) | ❌ Remover — era pré-CANON |
| `cli_test_04/` | desenvolvimento | C1-C5 + SUMMARY.md (9,1 KB) + TEST_REPORT.md + verification_report.json | ❌ Remover — era pré-CANON |
| `cli_test_05/` | desenvolvimento | C1-C5 + SUMMARY.md (7,8 KB) + TEST_REPORT.md | ❌ Remover — era pré-CANON |

> **Critério:** `20260204_001508/` foi gerado após o RC_v12_CANON (22:17 de 2026-02-03)
> e cobre C1-C5 completos — evidência suplementar da simulação. As sessões `cli_test_*`
> são iterações de desenvolvimento sem numeração RC, anteriores ao CANON.

```powershell
Remove-Item -Recurse -Force "outputs\cli_simulation\cli_test_02"
Remove-Item -Recurse -Force "outputs\cli_simulation\cli_test_03"
Remove-Item -Recurse -Force "outputs\cli_simulation\cli_test_04"
Remove-Item -Recurse -Force "outputs\cli_simulation\cli_test_05"
```

---

### 6.2 — `outputs/cli_simulation_real/`

| Pasta | Data/hora | Conteúdo | Status |
|---|---|---|---|
| `20260203_213152/` | 2026-02-03 21:31 | C1 apenas + SUMMARY.json (2,2 KB) | ❌ Remover — incompleta, pré-CANON |

> **Critério:** gerada 46 minutos **antes** do RC_v12_CANON (21:31 vs 22:17), contém
> apenas C1 — parcial e superada. O CANON contém a execução completa e definitiva.

```powershell
Remove-Item -Recurse -Force "outputs\cli_simulation_real"
```

---

### 6.3 — `outputs/coverage_html/`

Relatório HTML de cobertura focalizado apenas em `naming_validator.py` (1 arquivo de módulo,
175 KB). **Não é o relatório 94.05% do artigo.**

| Arquivo | Tamanho | Observação |
|---|---|---|
| `z_38236421897dcdc8_naming_validator_py.html` | 175,1 KB | Módulo único — escopo parcial |
| `index.html`, `function_index.html`, etc. | instrumentação HTML | Scaffolding do pytest-cov |

> **Critério:** O relatório de cobertura autoritativo é `outputs/reports/coverage/` (que
> já está marcado para remoção na PARTE 3) e o `coverage/htmlcov/` da raiz do projeto
> (gerado pelo `coverage/coverage.xml`). O `outputs/coverage_html/` é um terceiro
> artefato parcial sem referência no artigo.

```powershell
Remove-Item -Recurse -Force "outputs\coverage_html"
```

---

### 6.4 — `outputs/exports/`

| Item | Data | Tamanho | O que é | Ação |
|---|---|---|---|---|
| `json/query-edo_get_hierarchy-20251218_191645.json` | 2025-12-18 | 52,2 KB | Resultado de query SPARQL de hierarquia (UC-2) | Remover |
| `xlsx/query-edo_get_hierarchy-20251218_191533.xlsx` | 2025-12-18 | 11,7 KB | Mesmo resultado em Excel (UC-2) | Remover |
| `ontology-modified-test.ttl` | — | 435,2 KB | Ontologia modificada por teste de auto-fix — artefato descartável | Remover |

> **Critério:** as exportações de Dec-2025 pertencem ao UC-2 (consultas SPARQL interativas),
> que está fora do escopo do artigo. O `.ttl` é um artefato de teste sem rastreabilidade
> para nenhuma evidência do artigo.

```powershell
Remove-Item -Force "outputs\exports\json\query-edo_get_hierarchy-20251218_191645.json"
Remove-Item -Force "outputs\exports\xlsx\query-edo_get_hierarchy-20251218_191533.xlsx"
Remove-Item -Force "outputs\exports\ontology-modified-test.ttl"
# Remover pastas vazias se ficarem vazias:
# Remove-Item -Force "outputs\exports\json"
# Remove-Item -Force "outputs\exports\xlsx"
```

---

### 6.5 — `outputs/logs/` (arquivos na raiz — sessões de 20260226)

Gerados durante a verificação de regressão dos Patches 1-7 (see `docs/qa/patch-audit-formatter-facade-20260226.md`):

| Arquivo | Tamanho | O que é | Ação |
|---|---|---|---|
| `audit-log-session-20260226-160441.json` | 705 KB | Sessão validate-only — confirmou 1831 issues, 260 erros, 1571 avisos | Manter |
| `audit-log-session-20260226-160441.md` | 347,6 KB | Renderização Markdown da mesma sessão | Manter |
| `audit-log-session-20260226-160624.json` | 703,8 KB | Sessão auto-fix — confirmou 621 semânticos, 743 aplicados | Manter |
| `audit-log-session-20260226-160624.md` | 296,7 KB | Renderização Markdown da mesma sessão | Manter |
| `audit-log-session-20260226-160735.json` | 2,8 KB | Sessão abortada / erro — conteúdo mínimo | ❌ Remover |
| `audit-log-session-20260226-160735.md` | 0,5 KB | Markdown da sessão abortada | ❌ Remover |

> **Critério de manutenção:** as sessões `160441` (validate-only) e `160624` (auto-fix)
> são a evidência direta de que a ferramenta, **após os Patches 1-7**, reproduz todos
> os 10 métricas do RC_v12_CANON. São referenciadas pelo `patch-audit-formatter-facade-20260226.md`.
> São grandes (≈ 700 KB cada) mas não duplicam o CANON — são runs separados com timestamps distintos.
>
> A sessão `160735` (< 3 KB JSON, 0,5 KB MD) foi abortada e não contém evidência útil.

```powershell
Remove-Item -Force "outputs\logs\audit-log-session-20260226-160735.json"
Remove-Item -Force "outputs\logs\audit-log-session-20260226-160735.md"
```

---

### 6.6 — Resumo das ações da PARTE 6

| # | Alvo | Tamanho estimado | Ação |
|---|---|---|---|
| 6a | `outputs/cli_simulation/cli_test_02-05/` | ~4 sessões × ~6 pastas | Remover |
| 6b | `outputs/cli_simulation_real/` | 1 sessão parcial | Remover |
| 6c | `outputs/coverage_html/` | ~250 KB total | Remover |
| 6d | `outputs/exports/json/` + `xlsx/` + `.ttl` | ~500 KB total | Remover |
| 6e | `outputs/logs/*-160735.*` | 3,3 KB | Remover |
| **MANTER** | `outputs/cli_simulation/20260204_001508/` | evidência pós-CANON | Preservar |
| **MANTER** | `outputs/logs/*-160441.*` + `*-160624.*` | evidência regressão Patches 1-7 | Preservar |
| **MANTER** | `outputs/logs/RC_v12_CANON/` | evidência primária do artigo | Preservar (PARTE 4) |

---

---

*Gerado em 2026-02-26 para alinhamento entre repositório e artigo. PARTE 6 adicionada em 2026-02-26.*
