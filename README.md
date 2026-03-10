# ONTO-TOOLS

Sistema de canonicalização, verificação e certificação de reprodutibilidade de ontologias RDF/TTL.

> Para execução imediata: [INICIO-RAPIDO.md](INICIO-RAPIDO.md)
> Para guia técnico completo: [GUIA-EXECUCAO.md](GUIA-EXECUCAO.md)
> Para estrutura detalhada: [ESTRUTURA-PROJETO.md](ESTRUTURA-PROJETO.md)

---

## Problema resolvido

Ontologias RDF serializadas em Turtle (.ttl) são sensíveis à ordem de serialização: o mesmo grafo semântico pode gerar arquivos bytewise distintos em diferentes ferramentas ou execuções. Isso torna inviável:

- Controle de versão efetivo (diffs espúrios)
- Comparação formal entre artefatos
- Rastreabilidade de revisões
- Certificação de reprodutibilidade

O ONTO-TOOLS resolve isso por meio de um pipeline determinístico que garante que o mesmo grafo RDF produza sempre o mesmo arquivo TTL byte a byte, com auditabilidade completa via SHA-256 e bundles de evidência.

---

## Conceitos centrais

**Canonicalização**
Processo de serialização determinística de um grafo RDF. Ordena prefixos, sujeitos e predicados de forma reprodutível, seguindo a convenção Protégé. Implementada em UC-103 (`Canonicalizer`). Não altera semântica.

**Isomorfismo**
Dois grafos RDF são isomórficos se representam o mesmo conjunto de triplas, independentemente da ordem de serialização ou de rótulos de blank nodes. Verificado via `rdflib.compare.isomorphic`.

**Idempotência**
Uma operação `f` é idempotente se `f(f(x)) == f(x)`. A canonicalização é idempotente por construção: aplicá-la duas vezes ao mesmo arquivo produz o mesmo resultado. Verificada em dois níveis: hash SHA-256 (byte-level) e isomorfismo (semântico).

**Manifesto de execução (`run_manifest.json`)**
Registro estruturado de uma execução do pipeline. Captura artefatos de entrada com SHA-256, artefatos de saída com SHA-256, metadados de ambiente (Python, SO, timestamp), parâmetros e resultado das verificações.

**Bundle de evidência**
Diretório gerado ao final de uma execução RC (Reproducibility Certification), contendo: manifesto, artefatos canônicos, relatórios de isomorfismo e idempotência, logs de auditoria. Estrutura definida em `docs/rc-templates/RC_TEMPLATE_DESIGN-rcNN-v3.md`.

---

## Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                          │
│  ontotools (CLI)       python -m onto_tools.cli_menu (TUI)   │
│  scripts/menu.ps1      scripts/run_rc.py (RC pipeline)       │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│  OntoToolsFacade (RES-115)        RCWorkflow                 │
│  Workflows                        Verification pipeline      │
│    load_normalize_export            hasher.py                │
│    canonicalize                     isomorphism.py           │
│                                     idempotency.py           │
│                                     manifest_writer.py       │
│                                     evidence_writer.py       │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    DOMAIN LAYER                              │
│  Canonicalizer (UC-103)          Normalizer (UC-108)         │
│  QualityValidator                NamingValidator             │
│  OntologyGraph                   UriResolver                 │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   ADAPTERS LAYER                             │
│  RDFlibAdapter         ProtegeSerializer    AuditLogger      │
│  AuditFormatter        CLI (commands.py)    TUI (menu.py)    │
└──────────────────────────────────────────────────────────────┘
```

Arquitetura Hexagonal (Ports & Adapters). O domínio não importa adaptadores. A Façade é o único ponto de orquestração (RES-115).

---

## Estrutura do projeto

```
src/onto_tools/
├── domain/ontology/         # Lógica de negócio pura
│   ├── canonicalizer.py     # UC-103: ordenação determinística
│   ├── normalizer.py        # UC-108: correções semânticas
│   ├── quality_validator.py # Validação de qualidade
│   ├── naming_validator.py  # Validação de nomenclatura
│   ├── graph.py             # Wrapper rdflib.Graph
│   └── uri_resolver.py      # Resolução de URIs
├── application/
│   ├── facade.py            # Ponto único de orquestração
│   └── verification/        # Pipeline de certificação
│       ├── hasher.py
│       ├── isomorphism.py
│       ├── idempotency.py
│       ├── manifest_writer.py
│       ├── evidence_writer.py
│       └── rc_workflow.py
└── adapters/
    ├── cli/                 # commands.py (CLI), menu.py (TUI)
    ├── rdf/                 # rdflib_adapter.py, protege_serializer.py
    ├── reporting/           # audit_formatter.py
    └── logging/             # audit_logger.py

data/
├── edo/                     # Ontologia Energy Domain (artefato de trabalho)
│   ├── core/                # Versões do core
│   └── governance/          # Governança da ontologia
└── examples/                # Ontologia canônica de referência + rules.json
    ├── energy-domain-ontology.ttl
    └── rules.json

tests/
└── 1-uc-ontology/           # 973 testes (UC-101 a UC-108)
    ├── unit/
    ├── integration/
    ├── e2e/
    └── cli/

scripts/
├── run_rc.py                # Pipeline RC (Fases 1-6)
├── fill_rc_bundle.py        # Preenchimento do bundle (Fases 7-8)
├── menu.ps1                 # Menu interativo PowerShell
└── menu.bat                 # Menu interativo Windows

outputs/
├── logs/                    # Logs + bundles RC
│   └── RC_v1_CANON/         # Último RC certificado
└── review/                  # Pacotes de revisão gerados

config/
└── config.yaml              # Configuração central do sistema

docs/
└── rc-templates/            # Templates para RCs futuros
    ├── RC_TEMPLATE_DESIGN-rcNN-v3.md
    └── RC_EXECUTION_PROMPT-rcNN-v3.md
```

---

## Fluxo de execução macro

```
Ontologia TTL (entrada)
        │
        ▼
 [UC-101] Carregar + validar encoding
        │
        ▼
 [UC-108] Normalizar (correções semânticas — opcional)
        │
        ▼
 [UC-103] Canonizar (ordenação determinística)
        │
        ├──▶ SHA-256 do arquivo canônico
        ├──▶ Verificação de idempotência: f(f(x)) == f(x)
        ├──▶ Verificação de isomorfismo: mesmo grafo semântico
        │
        ▼
 run_manifest.json + evidence bundle → outputs/logs/
        │
        ▼
 [UC-104] Pacote de revisão → outputs/review/
```

---

## Protocolo RC (Reproducibility Certification)

O protocolo RC garante reprodutibilidade formal. Cada RC é um bundle completo
com ~60 artefatos verificáveis. Último: **RC_v1_CANON** (973 testes, 95.04% coverage).

```
Pipeline (run_rcNN.py):
  FASE 1: Create Structure    → 00_meta/, 20_runs/, 30_gates/, 40_tests/, 50_qa/
  FASE 2: Determinism         → Run2a + Run2b, gate_determinism.json
  FASE 3: Normalize + Canon   → Run3 (validate), Run4 (auto-fix)
  FASE 4: Gates               → gate_isomorphism.json, gate_idempotency.json
  FASE 5: Tests + Coverage    → pytest_summary.json (SOURCE OF TRUTH)
  FASE 6: Evidence Bundle     → BASELINE_POST, CHECKSUMS, rcNN_result.json

Bundle (fill_rcNN_bundle.py):
  FASE 7: Fill Bundle         → 00_meta/*, 10_proofs/*, 50_qa/*, 60_reference/, 90_legacy/
  FASE 8: Regenerate Checksums→ CHECKSUMS_SHA256.txt com todos os arquivos
```

Templates e prompt de execução: `docs/rc-templates/RC_TEMPLATE_DESIGN-rcNN-v3.md`

---

## Instalação

Pré-requisito: Python ≥ 3.12, Conda (Anaconda ou Miniconda)

```bash
conda create -n onto-tools-artigo python=3.12
conda activate onto-tools-artigo
conda run -n onto-tools-artigo pip install -e .
```

---

## Execução

```bash
# Menu interativo
python -m onto_tools.cli_menu

# CLI direta
ontotools --help
ontotools ontology load
ontotools ontology reorder
ontotools ontology review

# Pipeline RC completo
conda run -n onto-tools-artigo python scripts/run_rc.py
conda run -n onto-tools-artigo python scripts/fill_rc_bundle.py
```

---

## Testes

```bash
# Todos os testes (973)
pytest tests/1-uc-ontology/ -v

# Com cobertura (threshold 95%)
pytest tests/1-uc-ontology/ --cov=src/onto_tools --cov-report=term-missing
```

---

## Dependências principais

| Pacote     | Versão | Uso                                      |
|------------|--------|------------------------------------------|
| rdflib     | ≥7.0   | Parse, serialização e isomorfismo RDF    |
| click      | ≥8.1   | Interface CLI                            |
| pyyaml     | ≥6.0   | Configuração                             |
| openpyxl   | ≥3.1   | Exportação Excel                         |
| deepdiff   | ≥6.7   | Comparação de artefatos                  |
| jsonschema | ≥4.20  | Validação de esquemas JSON               |
| pytest     | ≥7.4   | Framework de testes                      |
