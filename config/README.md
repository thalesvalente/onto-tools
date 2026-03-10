# Config Directory

Diretório centralizado para arquivos de configuração do projeto.

## Arquivos

```text
config/
├── config.yaml         # Configuração principal da aplicação
├── pytest.ini          # Configuração do pytest
└── README.md           # Este arquivo
```

Nota: `.coveragerc` está na **raiz do projeto** (não em config/).

## Configurações

### config.yaml

Configuração principal do OntoTools:

- Paths de entrada/saída
- Configurações de logging
- Parâmetros de processamento

#### Parâmetros Críticos de Canonização

**`trim_whitespace: false`**
- **Rationale**: Preservação semântica RDF. Literais `"  value  "` e `"value"` são **semanticamente distintos** segundo RDF 1.1.
- **Impacto**: Whitespace em literais é preservado durante canonização (UC-103).
- **Validação**: GATE-B (Input ≅ Canonicalized) garante isomorfismo.
- **Exemplo**: `" Seal Ring"@en` → mantido sem alteração.

**`normalize_language_tags: "none"`**
- **Rationale**: BCP 47 permite case variation (`pt-BR` vs `pt-br`), mas rdflib trata como strings distintas.
- **Impacto**: Language tags preservados exatamente como no input.
- **Validação**: Testes T-702 verificam preservação de multilinguismo.

### pytest.ini

Configuração de testes:

- Test discovery patterns
- Markers personalizados
- Opções de execução
- Report settings

## 🔗 Compatibilidade

Symlinks na raiz do projeto apontam para estes arquivos para manter compatibilidade com ferramentas que esperam encontrá-los na raiz.
