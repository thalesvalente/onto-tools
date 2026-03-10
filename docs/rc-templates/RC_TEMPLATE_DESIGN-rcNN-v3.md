# RC Template - Design Doc (v3.0)

**Canonical Release Candidate Structure for OntoTools**

*Derived from the RC_v13 design and execution prompts, hardened to require real execution data for all derived documents.*

---

## Purpose

Este documento define a estrutura canônica para RCs (Release Candidates)
do OntoTools com foco em cinco propriedades:

1. **Reprodutibilidade** — o bundle deve poder ser regenerado a partir do run.
2. **Rastreabilidade** — toda afirmação deve apontar para uma fonte real.
3. **Executabilidade** — os artefatos primários devem nascer da execução.
4. **Auditabilidade** — um revisor deve conseguir verificar cada número.
5. **Paridade estrutural** — todo RC segue a mesma árvore lógica.

---

## Princípio central

O bundle RC_vNN_CANON é dividido em dois grupos:

### A. Artefatos primários de execução

São produzidos diretamente por `scripts/run_rcNN.py` durante o run real.
Esses arquivos são a base factual do RC.

### B. Artefatos derivados de documentação

São produzidos por `scripts/fill_rcNN_bundle.py`, mas **somente** a partir dos
artefatos primários já gerados no bundle atual.

**Proibição absoluta:**

- usar dicionários hardcoded com métricas de RC anterior;
- fixar timestamp, hash, coverage, número de testes, durations ou cwd;
- criar manifesto de run sem extrair dados do run correspondente;
- preencher docs com números não rastreáveis;
- declarar `PASS` em documento derivado se a fonte real diz `FAIL`.

---

## Estrutura de Diretórios

```text
outputs/logs/RC_vNN_CANON/
└── YYYYMMDD_HHMMSS/
    ├── 00_meta/
    │   ├── RC_LAYOUT_STANDARD.md
    │   ├── COMMAND_LOG.md
    │   ├── ENV_SNAPSHOT.md
    │   ├── env_snapshot.json
    │   ├── TOOL_VERSIONS.md
    │   ├── INPUT_SNAPSHOT.md
    │   └── BASELINE_PRE_SHA256.json
    │
    ├── 10_proofs/
    │   ├── BASELINE_POST_SHA256.json
    │   ├── declaration_RC_vNN_CANON.md
    │   ├── RC_vNN_FINAL_REPORT.md
    │   ├── IMMUTABILITY_PROOF.json
    │   ├── NORMALIZATION_REPORT_FROM_LOG.md
    │   ├── ARTICLE_COMPATIBILITY_PROOF_STRONG_RCNN.md
    │   ├── TRACEABILITY_MATRIX_RCNN.md
    │   └── EVIDENCE_MAP_RCNN.md
    │
    ├── 20_runs/
    │   ├── run2a_canonicalize/
    │   │   ├── canonical_output_run2a.ttl
    │   │   ├── run_manifest_run2a.json
    │   │   ├── idempotency_run2a.json
    │   │   ├── isomorphism_run2a.json
    │   │   ├── stdout_run2a.txt
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   ├── run2b_canonicalize/
    │   │   ├── canonical_output_run2b.ttl
    │   │   ├── run_manifest_run2b.json
    │   │   ├── isomorphism_run2b.json
    │   │   ├── stdout_run2b.txt
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   ├── run3_normalize_canonicalize/
    │   │   ├── canonical_output_run3.ttl
    │   │   ├── run_manifest_run3.json
    │   │   ├── isomorphism_run3.json
    │   │   ├── normalize_log_run3.json
    │   │   ├── stdout_run3.txt
    │   │   ├── export-log.json
    │   │   └── audit-log-session-*.json/.md
    │   └── run4_normalize_canonicalize/
    │       ├── canonical_output_run4.ttl
    │       ├── run_manifest_run4.json
    │       ├── normalize_log_run4.json
    │       ├── stdout_run4.txt
    │       ├── export-log.json
    │       └── audit-log-session-*.json/.md
    │
    ├── 30_gates/
    │   ├── gate_determinism.json
    │   ├── gate_isomorphism.json
    │   └── gate_idempotency.json
    │
    ├── 40_tests/
    │   ├── pytest_summary.json
    │   ├── pytest_full.txt
    │   ├── pytest_output.txt
    │   ├── pytest_collection.txt
    │   └── pytest_cmd.txt
    │
    ├── 50_qa/
    │   ├── QA_PLAN_RCNN.md
    │   ├── QA_CHECKLIST_FINAL_RCNN.md
    │   ├── COVERAGE_REPORT.txt
    │   └── DESIGNDOC_CONFORMANCE_MATRIX_RCNN.md
    │
    ├── 60_reference/
    │   └── README.md
    │
    ├── 90_legacy/
    │   └── README.md
    │
    ├── RC_vNN_CANON_SUMMARY.md
    ├── results_index_RC_vNN_CANON.md
    ├── rcNN_result.json
    └── CHECKSUMS_SHA256.txt
```

---

## Classificação de artefatos

### 1. Primários de execução

Devem ser gerados por `run_rcNN.py` durante a execução real:

- `00_meta/env_snapshot.json`
- `00_meta/BASELINE_PRE_SHA256.json`
- `20_runs/**/canonical_output_*.ttl`
- `20_runs/**/normalize_log_*.json`
- `20_runs/**/idempotency_*.json`
- `20_runs/**/isomorphism_*.json`
- `20_runs/**/run_manifest_*.json`
- `20_runs/**/stdout_*.txt`
- `30_gates/*.json`
- `40_tests/pytest_summary.json`
- `40_tests/pytest_full.txt`
- `40_tests/pytest_cmd.txt`
- `40_tests/pytest_collection.txt`
- `40_tests/pytest_output.txt`
- `10_proofs/BASELINE_POST_SHA256.json`
- `rcNN_result.json`

Se qualquer um destes existir apenas por preenchimento sintético, o RC deve ser
marcado como **INVALID**.

### 2. Derivados documentais

Podem ser gerados por `fill_rcNN_bundle.py`, mas somente a partir dos primários:

- `00_meta/ENV_SNAPSHOT.md`
- `00_meta/INPUT_SNAPSHOT.md`
- `00_meta/TOOL_VERSIONS.md`
- `00_meta/COMMAND_LOG.md`
- `10_proofs/declaration_RC_vNN_CANON.md`
- `10_proofs/IMMUTABILITY_PROOF.json`
- `10_proofs/NORMALIZATION_REPORT_FROM_LOG.md`
- `10_proofs/ARTICLE_COMPATIBILITY_PROOF_STRONG_RCNN.md`
- `10_proofs/TRACEABILITY_MATRIX_RCNN.md`
- `10_proofs/EVIDENCE_MAP_RCNN.md`
- `10_proofs/RC_vNN_FINAL_REPORT.md`
- `50_qa/*`
- `RC_vNN_CANON_SUMMARY.md`
- `results_index_RC_vNN_CANON.md`
- `60_reference/README.md`
- `90_legacy/README.md`

---

## Source of Truth

### 1. Testes e cobertura

`40_tests/pytest_summary.json` é a única fonte oficial para:

- collected
- passed
- failed
- skipped
- errors
- duration_seconds
- coverage.total_percent
- coverage.threshold_required
- coverage.passed
- comando realmente executado
- escopo realmente executado

Nenhum documento derivado pode repetir números de teste/cobertura sem apontar
explicitamente para este arquivo.

### 2. Integridade pós-run

`10_proofs/BASELINE_POST_SHA256.json` é a fonte oficial para hashes dos
artefatos gerados pelo pipeline primário.

### 3. Integridade total do bundle

`CHECKSUMS_SHA256.txt` é a fonte oficial para hashes de todos os arquivos do
bundle final, regenerado somente após todos os arquivos existirem.

### 4. Status final

`rcNN_result.json` é a fonte oficial do resultado machine-readable do RC.

### 5. Gates

`30_gates/*.json` são as fontes oficiais dos gates executáveis.

---

## Regras de consistência obrigatórias

### Regra 1 — Escopo de teste coerente

O comando real executado e o escopo declarado devem coincidir.
Se o comando foi `pytest tests/1-uc-ontology ...`, então:

- `pytest_cmd.txt` deve registrar exatamente isso;
- `pytest_summary.json` deve declarar o mesmo escopo;
- docs derivados não podem dizer `tests/` ou outro escopo.

### Regra 2 — Fill não cria fatos

`fill_rcNN_bundle.py` pode:

- ler arquivos primários;
- resumir;
- reorganizar;
- renderizar markdown/json derivado;
- apontar lacunas.

`fill_rcNN_bundle.py` não pode:

- inventar métricas;
- inferir hash ausente sem computar;
- fabricar stdout;
- gerar `pytest_collection.txt` sem coleta real;
- gerar `pytest_output.txt` sem output real;
- criar `run_manifest_runX.json` do nada.

### Regra 3 — Ausência de fonte gera bloqueio

Se a fonte necessária não existir, o script de fill deve:

- registrar `BLOCKED`;
- apontar o arquivo ausente;
- não preencher o documento como se estivesse completo.

### Regra 4 — Derivados não podem contradizer a fonte

Se `pytest_summary.json` diz coverage `74.89`, nenhum relatório derivado pode
escrever `95.04`.

### Regra 5 — Checksums só no final

`CHECKSUMS_SHA256.txt` deve ser regenerado apenas após a criação de todos os
arquivos derivados e placeholders válidos.

---

## Gates obrigatórios

| # | Gate | Fonte | Critério |
|---|------|-------|----------|
| 1 | Determinism | `30_gates/gate_determinism.json` | `run2a_hash == run2b_hash` |
| 2 | Isomorphism | `30_gates/gate_isomorphism.json` | `input ≅ output` nos runs exigidos |
| 3 | Idempotency | `30_gates/gate_idempotency.json` | `f(f(x)) == f(x)` |
| 4 | Test Suite | `40_tests/pytest_summary.json` | `failed == 0` e `errors == 0` |
| 5 | Coverage | `40_tests/pytest_summary.json` | `coverage >= threshold` |
| 6 | Traceability | bundle | docs derivados citam fontes reais |
| 7 | No hardcode | bundle | nenhum número factual sem fonte |

Se qualquer gate falhar, o RC fica `FAIL` ou `BLOCKED`.

---

## Workflow canônico

### Fases 1–6 — Execução real (`run_rcNN.py`)

1. Criar estrutura
2. Capturar ambiente
3. Executar runs do pipeline
4. Gerar gates
5. Executar testes reais
6. Gerar artefatos primários e resultado machine-readable

### Fases 7–8 — Derivação documental (`fill_rcNN_bundle.py`)

7. Ler artefatos primários e renderizar docs derivados
8. Regenerar `CHECKSUMS_SHA256.txt`

**Regra:** as fases 7–8 nunca substituem nem corrigem as fases 1–6;
elas apenas documentam o que já aconteceu.

---

## Requisitos para `run_rcNN.py`

O script principal deve:

- usar execução real via subprocessos quando necessário;
- registrar o comando de teste exato;
- registrar stdout/stderr reais;
- gravar escopo real de teste;
- produzir manifests de run a partir da execução do run;
- falhar explicitamente em caso de comando com retorno não zero quando
  configurado como obrigatório;
- usar timestamps dinâmicos do run atual;
- nunca reutilizar dados de RC anterior como se fossem resultados atuais.

---

## Requisitos para `fill_rcNN_bundle.py`

O script derivado deve:

- localizar o bundle do run atual ou receber `--rc-root` explícito;
- validar a presença das fontes primárias antes de renderizar docs;
- copiar apenas placeholders estruturais permitidos;
- gerar relatórios citando origem de cada número;
- registrar lacunas reais como `BLOCKED`;
- abortar se detectar valores hardcoded incompatíveis com as fontes.

---

## Campos mínimos de `pytest_summary.json`

```json
{
  "test_suite": "tests/1-uc-ontology",
  "pytest_cmd": "pytest tests/1-uc-ontology -v --tb=short --cov=src/onto_tools --cov-report=term-missing --cov-report=json",
  "timestamp": "<ISO-8601>",
  "results": {
    "collected": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "errors": 0,
    "duration_seconds": 0.0
  },
  "coverage": {
    "total_percent": 0.0,
    "threshold_required": 0.0,
    "passed": false
  }
}
```

---

## Proibições explícitas

- `RCNN = {...}` com métricas embutidas no fill
- `RCNN_BASE = outputs/logs/RC_vNN_CANON/<timestamp fixo>`
- copiar `pytest_output.txt` de RC anterior
- criar collection sintética com “abbreviated for brevity”
- escrever `APPROVED` em relatório se `rcNN_result.json` disser `FAIL`
- preencher `COMMAND_LOG.md` com comandos não executados
- escrever durations estimadas sem fonte de timing

---

## Checklist de finalização

```markdown
- [ ] Fases 1–6 executadas por `run_rcNN.py`
- [ ] Artefatos primários existem e são coerentes
- [ ] `pytest_summary.json` registra comando e escopo reais
- [ ] `BASELINE_POST_SHA256.json` gerado a partir do bundle atual
- [ ] `fill_rcNN_bundle.py` não contém métricas hardcoded
- [ ] Docs derivados citam fontes primárias
- [ ] `CHECKSUMS_SHA256.txt` regenerado ao final
- [ ] Nenhum documento derivado contradiz `pytest_summary.json`
- [ ] Nenhum documento derivado contradiz `rcNN_result.json`
- [ ] Bundle marcado `READY` apenas se não houver bloqueios
```

---

## Status possíveis

- `READY` — execução real completa, docs derivados consistentes
- `FAIL` — execução real falhou em gate obrigatório
- `BLOCKED` — fonte primária ausente ou inconsistência impede derivação
- `INVALID` — foi detectado hardcode factual ou contaminação de RC anterior

---

## Compatibilidade retroativa

Este v3 substitui o comportamento permissivo do v2 em dois pontos:

1. o fill deixa de ser “preenchimento” e vira “derivação documental”;
2. arquivos complementares em `20_runs/` e `40_tests/` deixam de poder ser
   sintéticos.

Quando houver conflito entre v2 e v3, **v3 prevalece**.

---

*Template Version: 3.0*  
*Compatibility note: supersedes v2.0 for all future RCs*  
*Policy note: factual fields must come from the current run only*
