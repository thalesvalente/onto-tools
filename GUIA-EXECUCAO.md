# ONTO-TOOLS — Guia de Execução Técnico

> Para instalação e primeiro uso: [INICIO-RAPIDO.md](INICIO-RAPIDO.md)
> Para visão arquitetural: [README.md](README.md)

---

## 1. Arquitetura

### 1.1 Padrão arquitetural

O projeto segue Arquitetura Hexagonal (Ports and Adapters):

- **Domain layer**: lógica de negócio pura, sem dependências externas
- **Application layer**: casos de uso, orquestração, pipeline de verificação
- **Adapters layer**: implementações concretas (RDFlib, CLI, Reporting, Logging)

A `OntoToolsFacade` é o único ponto de entrada para todos os 22 casos de uso (RES-115).
Nenhum adapter acessa o domínio diretamente.

### 1.2 Módulos e responsabilidades

#### Domain — `src/onto_tools/domain/ontology/`

| Módulo | Responsabilidade |
|--------|-----------------|
| `canonicalizer.py` | UC-103: Ordenação determinística de prefixos, sujeitos e predicados. Serializa TTL no estilo Protégé. Não altera semântica. |
| `normalizer.py` | UC-108: Correções semânticas — PascalCase em classes, lowerCamelCase em propriedades, Title Case em skos:prefLabel, ponto final em skos:definition, validação de dcterms:identifier. |
| `quality_validator.py` | Validação de restrições de qualidade configuradas em config.yaml (ex: DomainAttribute constraints). |
| `naming_validator.py` | Validação de convenções de nomenclatura sem aplicar correções. |
| `graph.py` | Wrapper sobre rdflib.Graph com utilitários de carga e acesso. |
| `uri_resolver.py` | Resolução e validação de URIs da ontologia. |

#### Application — Verificação: `src/onto_tools/application/verification/`

| Módulo | Responsabilidade |
|--------|-----------------|
| `hasher.py` | SHA-256 de arquivos e bytes. Saída em hexadecimal uppercase (64 chars). |
| `isomorphism.py` | Compara dois grafos RDF via `rdflib.compare.isomorphic`. Retorna `IsomorphismReport` com contagens de diferenças e amostras de triplas divergentes. |
| `idempotency.py` | Aplica uma transformação f duas vezes e verifica `f(f(x)) == f(x)`. Verifica primeiro por hash (byte-level); se diferentes, verifica por isomorfismo (semântico). |
| `manifest_writer.py` | Gera `run_manifest.json` com metadados completos da execução (inputs, outputs, ambiente, timestamps, verificações). Escrita atômica via renomeação de arquivo temporário. |
| `evidence_writer.py` | Organiza e agrega arquivos de evidência em um bundle estruturado. |
| `rc_workflow.py` | Orquestrador do protocolo RC (Reproducibility Certification). Coordena pipeline + testes + verificação + empacotamento de evidências. |

#### Application — Facade: `src/onto_tools/application/facade.py`

Ponto único de orquestração. Métodos principais:

| Método | UC |
|--------|----|
| `load_ontology(path, validate)` | UC-101 |
| `reorder_ontology()` | UC-103 (legado) |
| `canonicalize_ontology()` | UC-103 |
| `generate_review_output(output, filters)` | UC-104 |
| `normalize_ontology()` | UC-108 |
| `normalize_and_canonicalize()` | UC-108 + UC-103 |
| `execute_sparql(query)` | UC-201 |
| `export_json_structural(output)` | UC-302 |
| `export_json_hierarchical(output)` | UC-303 |
| `export_xlsx_catalog(output)` | UC-304 |
| `compare_artifacts(a, b)` | UC-501 |

#### Adapters — CLI: `src/onto_tools/adapters/cli/`

| Módulo | Responsabilidade |
|--------|-----------------|
| `commands.py` | CLI via Click. Entry point `ontotools`. |
| `menu.py` | TUI navegável. Entry point `python -m onto_tools.cli_menu`. |

#### Adapters — RDF: `src/onto_tools/adapters/rdf/`

| Módulo | Responsabilidade |
|--------|------------------|
| `rdflib_adapter.py` | Adaptador para rdflib (parse, serialização). |
| `protege_serializer.py` | Serialização no estilo Protégé (ordenação visual). |

#### Adapters — Reporting: `src/onto_tools/adapters/reporting/`

| Módulo | Responsabilidade |
|--------|------------------|
| `audit_formatter.py` | Formatação de relatórios de auditoria (Markdown). |

#### Adapters — Logging: `src/onto_tools/adapters/logging/`

| Módulo | Responsabilidade |
|--------|------------------|
| `audit_logger.py` | Logger estruturado de sessões de auditoria (JSON + MD). |

---

## 2. Entry points

| Forma | Comando |
|-------|---------|
| CLI instalada | `ontotools <grupo> <comando>` |
| Módulo Python | `python -m onto_tools` |
| Menu TUI | `python -m onto_tools.cli_menu` |
| Script Windows | `.\scripts\menu.ps1` |

O entry point `ontotools` é registrado em `pyproject.toml`:

```toml
[project.scripts]
ontotools = "onto_tools.adapters.cli.commands:cli"
```

---

## 3. Configuração

O sistema lê `config/config.yaml` a partir da raiz do projeto.

```yaml
ontologies:
  directory: "data/examples"           # Diretório com arquivos .ttl
  default: "energy-domain-ontology.ttl"

outputs:
  logs: "outputs/logs"                  # Manifestos e logs de auditoria
  review: "outputs/review"              # Pacotes de revisão (UC-104)

normalization:
  rules_file: "data/examples/rules.json"
```

---

## 4. Pipeline de execução

### 4.1 Fluxo completo (UC-108 + UC-103)

```
Arquivo TTL de entrada
        |
        v
 [UC-101] load_ontology()
   - Parse via rdflib
   - Validação de encoding UTF-8
   - Cálculo de SHA-256 do input
        |
        v
 [UC-108] normalize_ontology()          (opcional)
   - PascalCase em classes OWL
   - lowerCamelCase em propriedades
   - Title Case em skos:prefLabel
   - Ponto final em skos:definition
   - Validação de dcterms:identifier
        |
        v
 [UC-103] canonicalize_ontology()
   - Ordenar prefixos alfabeticamente
   - Ordenar sujeitos por URI
   - Ordenar predicados conforme PREDICATE_ORDER (Protégé)
   - Serializar TTL deterministicamente
   - Verificar idempotência: f(f(x)) == f(x)?
        |
        v
 Arquivo TTL canônico
   + SHA-256 do output
   + run_manifest.json
   + evidence bundle
```

### 4.2 Separação de responsabilidades UC-103 vs UC-108

| Operação | UC-103 Canonicalizer | UC-108 Normalizer |
|----------|---------------------|-------------------|
| Ordenar prefixos | sim | não |
| Ordenar triplas | sim | não |
| Serializar no estilo Protégé | sim | não |
| Corrigir nomenclatura (PascalCase) | não | sim |
| Corrigir skos:prefLabel | não | sim |
| Validar dcterms:identifier | não | sim |
| Alterar semântica | nunca | sim (correções) |

---

## 5. Verificações implementadas

### 5.1 SHA-256

Calculado via `hasher.sha256_file()`. Lê o arquivo em blocos de 64KB.
Retorna hash hexadecimal uppercase de 64 caracteres.

Usado em:
- Registro do input em `run_manifest.json`
- Registro dos outputs em `run_manifest.json`
- Verificação de imutabilidade de baseline (RC Workflow)

### 5.2 Isomorfismo

Implementado em `isomorphism.compare_isomorphism()`. Usa `rdflib.compare.isomorphic`
como verificação primária. Se os grafos não são isomórfos, calcula `rdflib.compare.graph_diff`
para identificar triplas divergentes.

`IsomorphismReport` captura:
- `are_isomorphic`: booleano
- `graph_a_triple_count`, `graph_b_triple_count`
- `triples_only_in_a`, `triples_only_in_b`: contagens
- `sample_diff_a`, `sample_diff_b`: até 5 triplas de exemplo

### 5.3 Idempotência

Implementado em `idempotency.check_idempotency()`.

Algoritmo:
1. Aplica `transform_fn(input, output1)` → resultado1
2. Aplica `transform_fn(output1, output2)` → resultado2
3. Compara SHA-256(resultado1) == SHA-256(resultado2)
4. Se hashes diferem, verifica isomorfismo como fallback semântico
5. Considera idempotente se hashes batem OU se grafos são isomórfos

`IdempotencyReport` captura:
- `is_idempotent`: booleano
- `first_result_hash`, `second_result_hash`
- `hashes_match`: booleano (byte-level)
- `isomorphism_report`: report detalhado se hashes diferirem

---

## 6. Manifesto de execução

Arquivo `run_manifest.json` gerado ao final de cada execução do pipeline.

Estrutura:

```json
{
  "run_id": "<uuid>",
  "created_at": "2026-02-27T00:00:00+00:00",
  "environment": {
    "python_version": "3.12.x",
    "platform": "Windows-11",
    "onto_tools_version": "3.0.0"
  },
  "inputs": [
    {
      "path": "data/examples/energy-domain-ontology.ttl",
      "sha256": "<hash-uppercase-64-chars>",
      "size_bytes": 1234567,
      "format": "turtle"
    }
  ],
  "outputs": [
    {
      "path": "outputs/review/ontology-review.ttl",
      "sha256": "<hash-uppercase-64-chars>",
      "size_bytes": 1234567,
      "format": "turtle",
      "artifact_type": "canonical_ontology"
    }
  ],
  "verifications": {
    "idempotency": {
      "is_idempotent": true,
      "hashes_match": true
    },
    "isomorphism": {
      "are_isomorphic": true
    }
  },
  "status": "success"
}
```

Escrita atômica: o arquivo é primeiro escrito em um temporário e depois renomeado,
evitando leituras de arquivos parciais.

---

## 7. Bundle de evidência

Diretório gerado por `evidence_writer.EvidenceWriter`. Estrutura:

```
outputs/logs/<run_id>/
  run_manifest.json          <- manifesto principal
  artifacts/
    ontology-review.ttl      <- artefato canônico
  reports/
    idempotency_report.json
    isomorphism_report.json
  logs/
    audit.json
  bundle_index.json          <- índice do bundle com SHA-256 de cada arquivo
```

`bundle_index.json` captura:

```json
{
  "bundle_id": "<uuid>",
  "created_at": "...",
  "files": [
    {
      "filename": "run_manifest.json",
      "sha256": "...",
      "file_type": "manifest",
      "description": "Main run manifest"
    }
  ],
  "summary": {}
}
```

---

## 8. Fluxo RC (Reproducibility Certification)

O protocolo RC garante reprodutibilidade formal. Cada RC gera um bundle
completo com ~60 artefatos verificáveis.

**Último RC**: RC_v1_CANON — 973 testes, 95.04% coverage, 3/3 gates PASS.

### 8.1 Execução via scripts

O protocolo é executado via dois scripts automatizados:

```bash
# Fases 1-6: Pipeline + gates + testes + evidência
conda run -n onto-tools-artigo python scripts/run_rc.py

# Fases 7-8: Documentação complementar + regenerar checksums
conda run -n onto-tools-artigo python scripts/fill_rc_bundle.py
```

### 8.2 Fases do protocolo

```
FASE 1: Create Structure    → 00_meta/, 20_runs/, 30_gates/, 40_tests/, 50_qa/
FASE 2: Determinism         → Run2a + Run2b: SHA256 idêntico
FASE 3: Normalize + Canon   → Run3 (validate-only), Run4 (auto-fix)
FASE 4: Gates               → gate_determinism, gate_isomorphism, gate_idempotency
FASE 5: Tests + Coverage    → pytest (973 tests), coverage >= 95%
FASE 6: Evidence Bundle     → BASELINE_POST, CHECKSUMS, rcNN_result.json
FASE 7: Fill Bundle         → 00_meta/*, 10_proofs/*, 50_qa/*, placeholders
FASE 8: Regenerate Checksums→ CHECKSUMS_SHA256.txt com todos os ~60 arquivos
```

### 8.3 Gates obrigatórios

| Gate | Critério |
|------|----------|
| **Determinism** | SHA256(Run2a) == SHA256(Run2b) |
| **Isomorphism** | Input ≅ Output (rdflib.compare) para cada run |
| **Idempotency** | f(f(x)) == f(x) — hash do 2º pass idêntico |

### 8.4 Estrutura do bundle RC

```
outputs/logs/RC_vNN_CANON/YYYYMMDDTHHMMSSZ_<uuid8>/
├── 00_meta/          # Metadata, env snapshot, input snapshot
├── 10_proofs/        # Provas formais, relatórios, declaração
├── 20_runs/          # 4 runs (2a, 2b, 3, 4) com outputs e logs
├── 30_gates/         # 3 gates JSON (determinism, isomorphism, idempotency)
├── 40_tests/         # pytest_summary.json (SOURCE OF TRUTH) + outputs
├── 50_qa/            # QA plan, checklist, coverage report
├── 60_reference/     # Referências externas (placeholder)
├── 90_legacy/        # Notas de migração (placeholder)
├── CHECKSUMS_SHA256.txt
├── RC_vNN_CANON_SUMMARY.md
├── results_index_RC_vNN_CANON.md
└── rcNN_result.json
```

### 8.5 Sources of Truth

- **`pytest_summary.json`** → números de teste e cobertura
- **`BASELINE_POST_SHA256.json`** → hashes dos artefatos do pipeline
- **`CHECKSUMS_SHA256.txt`** → hashes de todos os arquivos do bundle

### 8.6 Templates e documentação

Templates para criação de RCs futuros em `docs/rc-templates/`:
- `RC_TEMPLATE_DESIGN-rcNN-v3.md` — estrutura canônica do bundle (v3.0)
- `RC_EXECUTION_PROMPT-rcNN-v3.md` — prompt de execução para agente AI (v3.0)

---

## 9. Interface CLI

### 9.1 Grupos e comandos

```bash
ontotools --version
ontotools --help
ontotools ontology --help
ontotools query --help
ontotools export --help
ontotools data-input --help
ontotools comparison --help
```

### 9.2 Comandos do grupo ontology

```bash
# UC-101: Carregar ontologia
ontotools ontology load [FILE] [--validate/--no-validate]

# UC-103: Canonizar (serializar deterministicamente)
ontotools ontology reorder

# UC-104: Gerar pacote de revisão
ontotools ontology review [--output PATH] [--filters FILTER...]

# UC-108: Normalizar (correções semânticas)
ontotools ontology normalize
```

### 9.3 Exemplos

```bash
# Carregar arquivo específico com validação
ontotools ontology load energy-domain-ontology.ttl --validate

# Gerar revisão com output customizado
ontotools ontology review --output outputs/review/v2.0.ttl
```

---

## 10. Interface TUI (Menu Interativo)

```bash
python -m onto_tools.cli_menu
```

O menu entra diretamente no submenu de Ontology. Opções disponíveis:

```
  [1] UC-101: Carregar Ontologia
  [2] UC-103: Canonizar Ontologia (Ordenar p/ Diff)
  [3] UC-104: Gerar Pacote de Revisão
  [7] UC-108: Normalizar Ontologia (Correções)
  [S] Sair
```

Navegação: digite o número da opção. `[S]` para sair.

---

## 11. Testes

### 11.1 Estrutura

```
tests/1-uc-ontology/        <- 973 testes (UC-101 a UC-108)
  unit/         <- testes unitários de classes/funções isoladas
  integration/  <- testes de fluxos completos sem TUI
  e2e/          <- testes via menu TUI (Wexpect)
  cli/          <- testes da estrutura do menu
  conftest.py   <- fixtures compartilhadas
  fixtures/     <- ontologias e dados de teste
  data/         <- dados adicionais de teste
```

### 11.2 Execução

```bash
# Todos os testes (973)
pytest tests/1-uc-ontology/ -v

# Apenas testes unitários
pytest tests/1-uc-ontology/unit/ -v

# Com cobertura (threshold 95%)
pytest tests/1-uc-ontology/ --cov=src/onto_tools --cov-report=term-missing --cov-report=html

# Por marker
pytest tests/1-uc-ontology/ -m unit -v
pytest tests/1-uc-ontology/ -m integration -v
pytest tests/1-uc-ontology/ -m "not e2e" -v
```

### 11.3 Markers disponíveis

| Marker | Descrição |
|--------|-----------|
| `unit` | Testes unitários isolados |
| `integration` | Fluxos sem TUI |
| `e2e` | Testes via TUI (requer wexpect) |
| `smoke` | Sanidade rápida |
| `regression` | Bugs corrigidos |
| `slow` | Testes demorados |
| `critical` | P0 — caminho crítico |

---

## 12. Boas práticas

**Reprodutibilidade**
- Sempre canonizar antes de fazer commit da ontologia
- Verificar idempotência após qualquer alteração no Canonicalizer
- Manter manifestos no controle de versão junto com os artefatos

**Separação de responsabilidades**
- Usar UC-103 para diff/revisão (sem alteração semântica)
- Usar UC-108 somente antes da geração de versão formal
- Não misturar normalização e canonização em scripts de automação sem inspeção

**Auditabilidade**
- Os logs em `outputs/logs/` não devem ser deletados manualmente
- O bundle de evidência é imutável após geração

---

## 13. Troubleshooting

**`import onto_tools` falha**

O pacote não foi instalado. Execute na raiz do projeto:

```bash
conda activate onto-tools-artigo
conda run -n onto-tools-artigo pip install -e .
```

**`config/config.yaml` não encontrado**

O CLI procura o arquivo a partir da raiz detectada automaticamente. Verifique se o
arquivo existe em `config/config.yaml` relativo à raiz do projeto.

**`ontotools: command not found`**

O pacote foi instalado mas o script não está no PATH. Verifique que o ambiente conda
está ativado:

```bash
conda activate onto-tools-artigo
```

**Idempotência falha**

Se `is_idempotent=False` após canonização, verifique:
- Se o arquivo de entrada tem blank nodes não nomeados (podem causar variação)
- Se há literais com whitespace inconsistente
- O `isomorphism_report` no manifesto indicará as triplas divergentes

**Testes e2e falham no Windows**

Os testes E2E requerem `wexpect`. Instale:

```bash
conda run -n onto-tools-artigo pip install wexpect>=4.0
```

Se continuar falhando, execute apenas os unit e integration tests:

```bash
pytest tests/1-uc-ontology/ -m "not e2e" -v
```
