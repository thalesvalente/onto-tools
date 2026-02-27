# Estrutura do Projeto OntoTools

## Estrutura Atual (v3.0 — atualizado RC13)

```text
onto-tools-artigo/
│
├── src/                             # Código-fonte da aplicação
│   └── onto_tools/
│       ├── domain/
│       │   └── ontology/            # Lógica de domínio pura
│       │       ├── canonicalizer.py # UC-103: serialização determinística
│       │       ├── normalizer.py    # UC-108: correções semânticas
│       │       ├── quality_validator.py
│       │       ├── naming_validator.py
│       │       ├── graph.py         # Wrapper rdflib.Graph
│       │       └── uri_resolver.py  # Resolução de URIs
│       ├── application/
│       │   ├── facade.py            # Ponto único de orquestração (RES-115)
│       │   └── verification/        # Pipeline de certificação RC
│       │       ├── hasher.py        # SHA-256 de arquivos e bytes
│       │       ├── isomorphism.py   # Comparação semântica de grafos
│       │       ├── idempotency.py   # Verificação f(f(x)) == f(x)
│       │       ├── manifest_writer.py
│       │       ├── evidence_writer.py
│       │       └── rc_workflow.py   # Orquestrador do protocolo RC
│       ├── adapters/
│       │   ├── cli/                 # Interface de linha de comando
│       │   │   ├── commands.py      # CLI via Click (entry point `ontotools`)
│       │   │   └── menu.py          # TUI navegável
│       │   ├── rdf/                 # Adaptadores RDF
│       │   │   ├── rdflib_adapter.py
│       │   │   └── protege_serializer.py
│       │   ├── reporting/           # Formatação de relatórios
│       │   │   └── audit_formatter.py
│       │   └── logging/            # Logging e auditoria
│       │       └── audit_logger.py
│       ├── cli_menu.py              # Entry point TUI
│       ├── __init__.py
│       └── __main__.py
│
├── tests/                           # Testes organizados por UC
│   └── 1-uc-ontology/              # 963 testes (UC-101 a UC-108)
│       ├── unit/                    # Testes unitários isolados
│       ├── integration/             # Fluxos completos sem TUI
│       ├── e2e/                     # Testes via TUI (Wexpect)
│       ├── cli/                     # Testes da estrutura do menu
│       ├── conftest.py              # Fixtures compartilhadas
│       ├── fixtures/                # Ontologias de teste
│       └── data/                    # Dados adicionais de teste
│
├── scripts/                         # Scripts de automação
│   ├── run_rc13.py                  # Pipeline RC v13 (Fases 1-6)
│   ├── fill_rc13_bundle.py          # Preenchimento do bundle (Fases 7-8)
│   ├── gen_norm_report.py           # Geração de relatório de normalização
│   ├── isomorphism_check.py         # Verificação de isomorfismo standalone
│   ├── menu.bat                     # Menu interativo Windows
│   ├── menu.ps1                     # Menu interativo PowerShell
│   ├── setup.ps1                    # Setup do ambiente
│   └── setup_env.ps1               # Setup do ambiente Conda
│
├── data/                            # Dados e recursos
│   ├── edo/                         # Ontologia Energy Domain
│   │   ├── core/                    # Versões do core
│   │   └── governance/              # Governança da ontologia
│   ├── examples/                    # Ontologia canônica e regras
│   │   ├── energy-domain-ontology.ttl  # Ontologia de referência (6803 triples)
│   │   └── rules.json               # Regras de normalização
│   └── README.md
│
├── outputs/                         # Saídas geradas
│   ├── logs/                        # Bundles RC + logs de auditoria
│   │   ├── RC_v13_CANON/            # Último RC certificado
│   │   │   └── YYYYMMDD_HHMMSS/     # Bundle com ~60 artefatos
│   │   │       ├── 00_meta/         # Metadata e ambiente
│   │   │       ├── 10_proofs/       # Provas para artigo
│   │   │       ├── 20_runs/         # 4 runs do pipeline
│   │   │       ├── 30_gates/        # Gates JSON (3 gates)
│   │   │       ├── 40_tests/        # Artefatos de teste
│   │   │       ├── 50_qa/           # QA artifacts
│   │   │       ├── 60_reference/    # Referências externas
│   │   │       ├── 90_legacy/       # Notas de migração
│   │   │       ├── CHECKSUMS_SHA256.txt
│   │   │       └── RC_v13_CANON_SUMMARY.md
│   │   └── audit-log-session-*.json # Logs de sessão
│   └── review/                      # Pacotes de revisão (UC-104)
│
├── docs/                            # Documentação do projeto
│   └── rc-templates/                # Templates para RCs futuros
│       ├── RC_TEMPLATE_DESIGN-rc13.md  # Estrutura canônica (v2.0)
│       └── RC_EXECUTION_PROMPT-rc13.md # Prompt de execução (v2.0)
│
├── config/                          # Configurações centralizadas
│   ├── config.yaml                  # Configuração principal
│   ├── pytest.ini                   # Configuração pytest
│   └── README.md
│
├── coverage/                        # Relatórios de cobertura (gerados)
│   ├── coverage.xml
│   └── htmlcov/                     # Cobertura HTML
│
├── pyproject.toml                   # Configuração moderna Python (PEP 518)
├── setup.py                         # Setup tradicional (compatibilidade)
├── requirements.txt                 # Dependências Python
├── environment.yml                  # Ambiente Conda
├── pytest.ini                       # Configuração pytest (raiz)
├── README.md                        # Documentação principal
├── GUIA-EXECUCAO.md                 # Guia de execução técnico
├── INICIO-RAPIDO.md                 # Quick start
├── ESTRUTURA-PROJETO.md             # Este arquivo
└── .gitignore                       # Arquivos ignorados pelo Git
```

## Camadas da Arquitetura

### Domain Layer — `src/onto_tools/domain/ontology/`

Lógica de negócio pura, sem dependências externas.

| Módulo | Responsabilidade |
|--------|-----------------|
| `canonicalizer.py` | UC-103: Ordenação determinística (Protégé style) |
| `normalizer.py` | UC-108: Correções semânticas (PascalCase, lowerCamelCase, etc.) |
| `quality_validator.py` | Validação de restrições de qualidade |
| `naming_validator.py` | Validação de convenções de nomenclatura |
| `graph.py` | Wrapper sobre rdflib.Graph |
| `uri_resolver.py` | Resolução e validação de URIs |

### Application Layer — `src/onto_tools/application/`

| Módulo | Responsabilidade |
|--------|-----------------|
| `facade.py` | Ponto único de orquestração (RES-115) |
| `verification/hasher.py` | SHA-256 de arquivos e bytes |
| `verification/isomorphism.py` | Comparação semântica de grafos RDF |
| `verification/idempotency.py` | Verificação f(f(x)) == f(x) |
| `verification/manifest_writer.py` | Geração de run_manifest.json |
| `verification/evidence_writer.py` | Empacotamento de evidências |
| `verification/rc_workflow.py` | Orquestrador do protocolo RC |

### Adapters Layer — `src/onto_tools/adapters/`

| Módulo | Responsabilidade |
|--------|-----------------|
| `cli/commands.py` | CLI via Click (entry point `ontotools`) |
| `cli/menu.py` | TUI navegável |
| `rdf/rdflib_adapter.py` | Adaptador RDFLib |
| `rdf/protege_serializer.py` | Serialização no estilo Protégé |
| `reporting/audit_formatter.py` | Formatação de relatórios de auditoria |
| `logging/audit_logger.py` | Logger de auditoria |

## Scripts de Automação

| Script | Propósito |
|--------|-----------|
| `scripts/run_rc13.py` | Pipeline RC v13 completo (Fases 1-6) |
| `scripts/fill_rc13_bundle.py` | Preenchimento do bundle RC v13 (Fases 7-8) |
| `scripts/gen_norm_report.py` | Geração de relatório de normalização |
| `scripts/isomorphism_check.py` | Verificação standalone de isomorfismo |
| `scripts/menu.ps1` / `menu.bat` | Menu interativo |
| `scripts/setup.ps1` / `setup_env.ps1` | Setup do ambiente |

## Instalação

```bash
conda create -n onto-tools-artigo python=3.12
conda activate onto-tools-artigo
conda run -n onto-tools-artigo pip install -e .
```

## Executar Testes

```bash
# Todos os testes (963)
pytest tests/1-uc-ontology/ -v

# Com coverage (threshold 95%)
pytest tests/1-uc-ontology/ \
  --cov=src/onto_tools \
  --cov-report=term-missing
```

## Executar Pipeline RC

```bash
# Execução completa (Fases 1-6)
conda run -n onto-tools-artigo python scripts/run_rc13.py

# Preenchimento do bundle (Fases 7-8)
conda run -n onto-tools-artigo python scripts/fill_rc13_bundle.py
```

## Executar Aplicação

```bash
# Via menu interativo
.\scripts\menu.ps1           # PowerShell
.\scripts\menu.bat           # Windows Batch

# Via CLI direta
ontotools --help
python -m onto_tools.cli_menu
```

## Referências

- **PEP 518**: pyproject.toml specification
- **PEP 621**: Project metadata in pyproject.toml
- **Src Layout**: <https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout>
- **RC Templates**: `docs/rc-templates/RC_TEMPLATE_DESIGN-rc13.md`
