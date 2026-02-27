# Dados de Teste - UC-1 Ontology

Esta pasta contém arquivos de dados para testes do módulo de ontologia (UC-1).

## Estrutura

```
data/
├── ontologies/          # Ontologias de teste em formato TTL
│   ├── valid/           # Ontologias válidas
│   └── invalid/         # Ontologias com erros intencionais
├── rules/               # Arquivos de regras de normalização
├── expected/            # Resultados esperados para comparação
└── fixtures/            # Fixtures JSON/YAML para testes
```

## Uso

Os testes devem carregar dados desta pasta usando paths relativos:

```python
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ONTOLOGIES_DIR = DATA_DIR / "ontologies"

def load_test_ontology(name: str) -> Graph:
    path = ONTOLOGIES_DIR / "valid" / f"{name}.ttl"
    g = Graph()
    g.parse(path, format="turtle")
    return g
```

## Princípio

**Dados separados do código** - Os dados de teste devem ser armazenados em arquivos externos, não embutidos no código Python.

Benefícios:
- Facilita manutenção e atualização dos dados
- Permite reutilização de dados entre testes
- Melhora legibilidade dos testes
- Facilita validação manual dos dados de teste
