"""
Domain Layer — Ontology Module

Componentes de domínio para processamento de ontologias OWL/TTL.

Classes principais:
- Canonicalizer (UC-103): Ordenação determinística para diff/revisão
- Normalizer (UC-108): Correções semânticas de nomenclatura
- NamingValidator: Validação de convenções de nomenclatura
- OntologyQualityValidator: Validação de qualidade da ontologia
- URIResolver: Resolução e canonização de URIs
"""

from .canonicalizer import Canonicalizer, CanonicalizationResult
from .normalizer import Normalizer, NormalizationResult
from .naming_validator import NamingValidator
from .quality_validator import OntologyQualityValidator
from .uri_resolver import URIResolver, STANDARD_PREFIXES

__all__ = [
    # UC-103 Canonização
    "Canonicalizer",
    "CanonicalizationResult",
    # UC-108 Normalização
    "Normalizer", 
    "NormalizationResult",
    # Validação
    "NamingValidator",
    "OntologyQualityValidator",
    # URI
    "URIResolver",
    "STANDARD_PREFIXES",
]
