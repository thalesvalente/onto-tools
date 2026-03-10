# ONTO-TOOLS — Início Rápido

> Documentação técnica completa: [GUIA-EXECUCAO.md](GUIA-EXECUCAO.md)
> Estrutura do projeto: [ESTRUTURA-PROJETO.md](ESTRUTURA-PROJETO.md)

---

## Pré-requisitos

- Python ≥ 3.12
- Conda (Anaconda ou Miniconda)
- Git

---

## Instalação

```bash
conda create -n onto-tools-artigo python=3.12
conda activate onto-tools-artigo
conda run -n onto-tools-artigo pip install -e .
```

Verifique:

```bash
python -c "import onto_tools; print('OK')"
```

---

## Executar o menu interativo

```bash
python -m onto_tools.cli_menu
```

Ou via script:

```powershell
.\scripts\menu.ps1
```

O sistema entra diretamente no menu de ontologias:

```
  [1] Carregar Ontologia
  [2] Canonizar Ontologia (Ordenar p/ Diff)
  [3] Gerar Pacote de Revisão
  [7] Normalizar Ontologia (Correções)
  [S] Sair
```

---

## Exemplo mínimo: canonizar uma ontologia

**Passo 1 — Carregar**

No menu, escolha `[1]`. O sistema lista os arquivos `.ttl` disponíveis em `data/examples/`. Selecione `energy-domain-ontology.ttl`.

**Passo 2 — Canonizar**

Escolha `[2]`. O sistema aplica ordenação determinística e salva o resultado. O output inclui:

- SHA-256 do arquivo canônico
- Contagem de triplas
- Confirmação de idempotência

**Passo 3 — Verificar resultado**

Os artefatos gerados ficam em:

```
outputs/logs/       ← run_manifest.json, audit log
outputs/review/     ← ontology-review.ttl (pacote de revisão)
```

---

## Onde olhar os resultados

| Artefato | Local |
|----------|-------|
| Manifesto de execução | `outputs/logs/run_manifest.json` |
| Log de auditoria | `outputs/logs/` |
| Ontologia canônica (revisão) | `outputs/review/ontology-review.ttl` |
| Bundle RC certificado | `outputs/logs/RC_v1_CANON/` |

---

## Rodar os testes

```bash
# Todos os testes (973)
pytest tests/1-uc-ontology/ -v

# Com cobertura (threshold 95%)
pytest tests/1-uc-ontology/ --cov=src/onto_tools --cov-report=term-missing
```

---

## Executar pipeline RC (Reproducibility Certification)

O protocolo RC gera um bundle completo (~60 artefatos) com provas formais
de reprodutibilidade, determinismo, isomorfismo e idempotência.

```bash
# Pipeline completo (Fases 1-6)
conda run -n onto-tools-artigo python scripts/run_rc.py

# Documentação complementar (Fases 7-8)
conda run -n onto-tools-artigo python scripts/fill_rc_bundle.py
```

Último RC: **RC_v1_CANON** — 973 testes, 95.04% coverage, 3/3 gates PASS.

---

Problemas? Consulte a seção Troubleshooting em [GUIA-EXECUCAO.md](GUIA-EXECUCAO.md).
