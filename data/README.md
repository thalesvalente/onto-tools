# Data Directory

Diretório para dados e recursos do projeto.

## Estrutura

```text
data/
├── edo/                # Ontologia Energy Domain
│   ├── core/           # Versões do core
│   └── governance/     # Governança da ontologia
├── examples/           # Ontologia canônica de referência e regras
│   ├── energy-domain-ontology.ttl  # Ontologia de referência (6803 triples)
│   └── rules.json     # Regras de normalização (UC-108)
└── README.md
```

## Propósito

- **edo/**: Artefato de trabalho da ontologia Energy Domain
- **examples/**: Ontologia canônica usada como entrada do pipeline RC e regras de normalização

## Notas

- `energy-domain-ontology.ttl` é o input de referência para o pipeline RC
- SHA256 do input: `A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE`
- `rules.json` define as regras aplicadas pelo Normalizer (UC-108)
