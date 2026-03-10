# Scripts Directory

Scripts utilitários, executores e automação do projeto.

## Estrutura

```text
scripts/
├── run_rc.py                # Pipeline RC (Fases 1-6)
├── fill_rc_bundle.py        # Preenchimento do bundle (Fases 7-8)
├── gen_norm_report.py       # Geração de relatório de normalização
├── isomorphism_check.py     # Verificação standalone de isomorfismo
├── refactor_remove_disabled.py  # Refatoração: remoção de código desabilitado
├── menu.bat                 # Menu interativo Windows (Batch)
├── menu.ps1                 # Menu interativo PowerShell
├── setup.ps1                # Setup rápido do ambiente
└── setup_env.ps1            # Setup avançado com validações
```

## Pipeline RC (Reproducibility Certification)

### run_rc.py

Executa o protocolo RC completo (Fases 1-6):

```bash
conda run -n onto-tools-artigo python scripts/run_rc.py
```

**O que faz:** Cria estrutura do bundle, executa 4 runs do pipeline (2a, 2b, 3, 4), gera gates (determinism, isomorphism, idempotency), roda testes com coverage, gera evidências.

### fill_rc_bundle.py

Preenche a documentação complementar do bundle (Fases 7-8):

```bash
conda run -n onto-tools-artigo python scripts/fill_rc_bundle.py
```

**O que faz:** Gera ~28 arquivos faltantes (00_meta/*, 10_proofs/*, 50_qa/*, etc.) e regenera CHECKSUMS_SHA256.txt.

## Utilitários

### gen_norm_report.py

Gera relatório de normalização a partir dos logs.

### isomorphism_check.py

Verificação standalone de isomorfismo entre dois grafos RDF.

### refactor_remove_disabled.py

Script de refatoração para remoção de código desabilitado.

## Executores

### menu.bat / menu.ps1

Menu interativo para executar operações do OntoTools:

```powershell
.\scripts\menu.ps1
```

## Scripts de Setup

### setup.ps1 (Recomendado)

Setup rápido do ambiente Conda:

```powershell
.\scripts\setup.ps1
```

### setup_env.ps1 (Avançado)

Setup com validações detalhadas do YAML:

```powershell
.\scripts\setup_env.ps1
```

## Notas

- `environment.yml` está na **raiz do projeto**, não em `scripts/`
- Scripts de setup procuram o arquivo automaticamente
- Para executar o menu, o ambiente `onto-tools-artigo` deve estar ativo
- Para criar RCs futuros, usar `run_rc.py` / `fill_rc_bundle.py` que já auto-versionam
