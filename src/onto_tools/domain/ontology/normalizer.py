"""
Normalizer — Normalização Semântica de Ontologias TTL (UC-108)

Responsável por correções semânticas e validação de convenções de nomenclatura.
NÃO é responsável por ordenação (responsabilidade do Canonicalizer UC-103).

Separação de responsabilidades (Single Responsibility Principle):
- Canonicalizer (UC-103): Ordenação determinística para diff/revisão
- Normalizer (UC-108): Correções semânticas (PascalCase, Title Case, etc.)

Operações realizadas:
- Correção de nomenclatura de classes (PascalCase)
- Correção de nomenclatura de propriedades (lowerCamelCase)
- Correção de skos:prefLabel (Title Case por idioma)
- Correção de skos:definition (ponto final)
- Validação de dcterms:identifier
- Validação de convenções SKOS

Operações NÃO realizadas (responsabilidade do Canonicalizer):
- Ordenação de triplas
- Ordenação de prefixos
- Serialização Protégé
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rdflib import Graph

try:
    from .naming_validator import NamingValidator
except ImportError:
    NamingValidator = None


@dataclass
class NormalizationResult:
    """Resultado da normalização com estatísticas de correções."""
    graph: "Graph"
    validation_report: Optional[dict] = None
    fix_stats: Optional[dict] = None
    warnings: list[dict] = field(default_factory=list)
    auto_fix_applied: bool = False
    
    def to_dict(self) -> dict:
        """Converte para dicionário serializável."""
        return {
            "auto_fix_applied": self.auto_fix_applied,
            "warnings_count": len(self.warnings),
            "fix_stats": self.fix_stats,
            "validation_report_summary": {
                "total_errors": len(self.validation_report.get("errors", [])) if self.validation_report else 0,
                "total_warnings": len(self.validation_report.get("warnings", [])) if self.validation_report else 0,
            } if self.validation_report else None
        }


def _get_default_rules_path() -> str:
    """
    Retorna o caminho padrão para rules.json na nova estrutura.
    """
    project_root = Path(__file__).parent.parent.parent.parent.parent
    return str(project_root / "data" / "examples" / "rules.json")


class Normalizer:
    """
    UC-108: Normalização Semântica de Ontologias TTL.
    
    Aplica correções semânticas e valida convenções de nomenclatura OWL.
    NÃO ordena triplas (use Canonicalizer para isso).
    
    Correções aplicadas (quando auto_fix=True em rules.json):
    - Classes OWL: PascalCase (ex: AbandonmentCap)
    - Propriedades OWL: lowerCamelCase (ex: hasAttribute)
    - skos:prefLabel: Title Case por idioma (preposições em minúsculo)
    - skos:definition: Ponto final adicionado se ausente
    - dcterms:identifier: Corrigido para match com local name
    
    Validações sempre executadas:
    - Convenções de nomenclatura conforme rules.json
    - Bilinguismo em prefLabels (@en, @pt-br)
    - Consistência de dcterms:identifier
    """
    
    def __init__(self, rules_path: str = None, auto_fix: bool = None):
        """
        Args:
            rules_path: Caminho para rules.json (default: data/examples/rules.json)
            auto_fix: Forçar auto_fix (None = usar valor de rules.json)
        """
        self.rules_path = rules_path or _get_default_rules_path()
        self.rules = self._load_rules()
        self.validation_warnings = []
        self.naming_validation_report = None
        self.naming_fix_stats = None
        
        # Auto-fix pode ser overridden pelo parâmetro
        self._auto_fix_override = auto_fix
        
        # Inicializar NamingValidator se naming_syntax estiver configurado
        self.naming_validator = None
        if "naming_syntax" in self.rules and NamingValidator is not None:
            self.naming_validator = NamingValidator(rules_path=self.rules_path)

    def _load_rules(self) -> dict:
        """Carrega arquivo rules.json com regras de normalização (UC-108)"""
        rules_file = Path(self.rules_path)
        
        if not rules_file.exists():
            print(f"Aviso: rules.json não encontrado em {self.rules_path}, usando regras padrão")
            return self._default_rules()
        
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            return rules_data.get("rules", {})
        except Exception as e:
            print(f"Erro ao carregar rules.json: {e}")
            return self._default_rules()

    def _default_rules(self) -> dict:
        """Regras padrão de normalização semântica."""
        return {
            "validation": {
                "check_utf8_encoding": True,
                "validate_iris": True,
                "warn_on_deprecated_features": True
            },
            "naming_syntax": {
                "auto_fix": True,
                "owl_classes": {"pattern": "PascalCase"},
                "owl_properties": {"pattern": "lowerCamelCase"},
                "skos_preflabels": {
                    "required_languages": ["en", "pt-br"],
                    "validate_title_case": True
                }
            }
        }
    
    def _should_auto_fix(self) -> bool:
        """Determina se auto_fix deve ser aplicado."""
        if self._auto_fix_override is not None:
            return self._auto_fix_override
        naming_syntax = self.rules.get("naming_syntax", {})
        return naming_syntax.get("auto_fix", False)

    def normalize(self, graph: Graph) -> NormalizationResult:
        """
        UC-108: Aplica normalização semântica ao grafo.
        
        Foca em correções de nomenclatura e validação de convenções.
        NÃO ordena triplas (use Canonicalizer para isso).
        
        Args:
            graph: Grafo RDF a normalizar
        
        Returns:
            NormalizationResult com grafo normalizado e estatísticas
            
        Correções aplicadas (quando auto_fix=True):
        - Classes OWL: PascalCase
        - Propriedades OWL: lowerCamelCase
        - skos:prefLabel: Title Case por idioma
        - skos:definition: Ponto final
        - dcterms:identifier: Match com local name
        """
        from rdflib import Graph as RDFGraph
        
        # Limpar estado de execuções anteriores
        self.validation_warnings = []
        self.naming_validation_report = None
        self.naming_fix_stats = None
        
        # Copiar grafo para não modificar o original
        normalized = RDFGraph()
        for prefix, namespace in graph.namespaces():
            normalized.bind(prefix, namespace)
        for triple in graph:
            normalized.add(triple)
        
        # Aplicar validações gerais
        validation_rules = self.rules.get("validation", {})
        self._apply_validation_rules(normalized, validation_rules)
        
        # Aplicar validações e correções de nomenclatura
        naming_syntax_rules = self.rules.get("naming_syntax", {})
        auto_fix_applied = False
        
        if naming_syntax_rules and self.naming_validator:
            # Validar nomenclatura
            is_valid, self.naming_validation_report = self.naming_validator.validate_naming_syntax(normalized)
            
            # Registrar erros/warnings
            self._collect_naming_warnings()
            
            # RF-01: SEMPRE calcular propostas de correção, independente do modo
            # Isso garante invariância de reporte entre validate-only e auto-fix
            should_apply = self._should_auto_fix()
            normalized, self.naming_fix_stats = self._apply_naming_fixes(
                normalized, 
                self.naming_validation_report or {"errors": [], "warnings": [], "suggestions": []},
                apply_corrections=should_apply  # Controla se correções são realmente aplicadas
            )
            auto_fix_applied = should_apply
        
        return NormalizationResult(
            graph=normalized,
            validation_report=self.naming_validation_report,
            fix_stats=self.naming_fix_stats,
            warnings=self.validation_warnings.copy(),
            auto_fix_applied=auto_fix_applied
        )
    
    def normalize_legacy(self, graph: Graph) -> Graph:
        """
        Método legado para compatibilidade com código existente.
        
        Retorna apenas o grafo (sem NormalizationResult).
        DEPRECATED: Use normalize() e acesse result.graph
        """
        result = self.normalize(graph)
        return result.graph
    
    def _collect_naming_warnings(self) -> None:
        """Coleta erros e warnings do relatório de nomenclatura."""
        if not self.naming_validation_report:
            return
        
        # Erros severos
        for error in self.naming_validation_report.get("errors", []):
            self.validation_warnings.append({
                "type": "naming_convention",
                "severity": "error",
                "rule": error.get("rule", "unknown"),
                "subject": error.get("subject", "unknown"),
                "issue": error.get("issue", ""),
                "expected": error.get("expected", "")
            })
        
        # Avisos
        for warning in self.naming_validation_report.get("warnings", []):
            self.validation_warnings.append({
                "type": "naming_convention",
                "severity": "warning",
                "rule": warning.get("rule", "unknown"),
                "subject": warning.get("subject", "unknown"),
                "issue": warning.get("issue", ""),
                "expected": warning.get("expected", "")
            })
    
    def _apply_validation_rules(self, graph: Graph, validation_rules: dict) -> None:
        """
        Aplica regras de validação e adiciona warnings.
        
        Args:
            graph: Grafo RDF a validar
            validation_rules: Regras de validation do rules.json
        """
        from rdflib import URIRef
        
        # Validar IRIs se configurado
        if validation_rules.get("validate_iris", False):
            for s, p, o in graph:
                # Validar subject (sempre URI)
                if isinstance(s, URIRef) and not self._is_valid_iri(str(s)):
                    self.validation_warnings.append({
                        "type": "invalid_iri",
                        "subject": str(s),
                        "message": f"IRI inválida no subject: {s}"
                    })
                
                # Validar predicate (sempre URI)
                if isinstance(p, URIRef) and not self._is_valid_iri(str(p)):
                    self.validation_warnings.append({
                        "type": "invalid_iri",
                        "predicate": str(p),
                        "message": f"IRI inválida no predicate: {p}"
                    })
                
                # Validar object se for URI
                if isinstance(o, URIRef) and not self._is_valid_iri(str(o)):
                    self.validation_warnings.append({
                        "type": "invalid_iri",
                        "object": str(o),
                        "message": f"IRI inválida no object: {o}"
                    })
        
        # Avisar sobre features deprecated (ex: owl:DataRange deprecated em OWL 2)
        if validation_rules.get("warn_on_deprecated_features", False):
            from rdflib import OWL
            deprecated_features = [
                (OWL.DataRange, "owl:DataRange foi deprecated em OWL 2, use rdfs:Datatype")
            ]
            
            for deprecated_term, warning_msg in deprecated_features:
                # Verificar se o termo deprecated é usado
                if (None, None, deprecated_term) in graph or \
                   (None, deprecated_term, None) in graph or \
                   (deprecated_term, None, None) in graph:
                    self.validation_warnings.append({
                        "type": "deprecated_feature",
                        "feature": str(deprecated_term),
                        "message": warning_msg
                    })
    
    def _is_valid_iri(self, iri: str) -> bool:
        """
        Valida IRI conforme RFC 3987.
        
        Args:
            iri: IRI a validar
        
        Returns:
            bool: True se IRI é válida
        """
        # Validação básica: deve ter scheme e não pode ter espaços
        if ' ' in iri:
            return False
        
        # Deve ter scheme (http://, https://, urn:, etc)
        if ':' not in iri:
            return False
        
        # Blank nodes são sempre válidos
        if iri.startswith('_:'):
            return True
        
        return True
    
    def _apply_naming_fixes(self, graph: Graph, validation_report: dict, apply_corrections: bool = True) -> tuple[Graph, dict]:
        """
        Calcula e opcionalmente aplica correções de nomenclatura baseadas no relatório de validação.
        
        RF-01: Esta função SEMPRE calcula as propostas de correção, independente do modo.
        O parâmetro apply_corrections controla se as correções são realmente aplicadas ao grafo.
        
        Args:
            graph: Grafo RDF a corrigir
            validation_report: Relatório de validação do NamingValidator
            apply_corrections: Se True, aplica as correções. Se False, apenas calcula propostas.
        
        Returns:
            tuple[Graph, dict]: (Grafo com URIs e literais corrigidos, Estatísticas de correções)
            
        Estatísticas retornadas:
            {
                "uri_corrections": {...},
                "identifier_corrections": {...},
                "preflabel_corrections": {...},  # Correções aplicadas (quando apply_corrections=True)
                "definition_corrections": {...},  # Correções aplicadas (quando apply_corrections=True)
                "pending_preflabel_corrections": {...},  # Correções propostas não aplicadas
                "pending_definition_corrections": {...},  # Correções propostas não aplicadas
                "total_triples_modified": int,
                "total_uri_replacements": int,
                "total_identifier_fixes": int,
                "total_preflabel_fixes": int,
                "total_definition_fixes": int,
                "total_pending_preflabel_fixes": int,
                "total_pending_definition_fixes": int,
                "mode": "auto_fix" | "validate_only"  # Indica o modo de execução
            }
        """
        from rdflib import URIRef, Literal, Graph as RDFGraph, Namespace
        from rdflib.namespace import SKOS
        import yaml
        
        DCTERMS = Namespace("http://purl.org/dc/terms/")
        
        # RF-02: Usar self.rules já carregado pelo construtor (respeita rulebook injetado)
        # Não recarregar de path hardcoded — isso causava divergência de governança
        rules_data = {"rules": self.rules}  # Wrapper para manter compatibilidade de acesso
        
        # Carregar stopwords do rules já carregado (fonte principal)
        def load_stopwords(lang: str) -> set:
            stopwords_config = self.rules.get("naming_syntax", {}).get("stopwords", {})
            # Mapear idioma para chave do config
            if lang.startswith("pt"):
                return set(stopwords_config.get("pt_br", []))
            else:
                return set(stopwords_config.get("en", []))
        
        # Carregar acrônimos do rules já carregado
        acronyms_config = self.rules.get("naming_syntax", {}).get("acronyms", {})
        registered_acronyms = acronyms_config.get("list", [])
        # Acrônimos ambíguos: também são palavras comuns (ex: "SEM" = Scanning Electron Microscope vs "sem" = preposição pt)
        ambiguous_acronyms = set(acronyms_config.get("ambiguous", {}).get("list", []))
        
        # Verificar se deve normalizar acrônimos em definitions
        domain_attr_config = self.rules.get("validation", {}).get("domain_attribute_constraints", {})
        definitions_config = domain_attr_config.get("definitions", {})
        normalize_acronyms_in_definitions = definitions_config.get("normalize_acronyms", False)
        # Verificar se auto_fix está habilitado para definitions
        auto_fix_definitions = definitions_config.get("auto_fix", True) and apply_corrections
        
        # Carregar regras de palavras compostas
        preflabel_rules = self.rules.get("naming_syntax", {}).get("skos_preflabels", {})
        # Verificar se auto_fix está habilitado especificamente para prefLabels
        # Agora também depende do parâmetro apply_corrections para RF-01
        auto_fix_preflabels = preflabel_rules.get("auto_fix", True) and apply_corrections
        compound_rules = preflabel_rules.get("compound_words", {})
        apostrophe_prefixes = compound_rules.get("apostrophe_preposition", {}).get("prefixes", ["d'", "l'"])
        
        def correct_preflabel(label: str, lang: str = "pt-br") -> str:
            """Corrige o skos:prefLabel para atender às regras de capitalização por idioma.
            
            Regras:
            - Acrônimos registrados devem estar em UPPERCASE (PLET, HCR, CO2, etc.)
            - Preposições/stopwords em minúsculo (exceto primeira palavra)
            - Palavras com hífen: ambas partes capitalizadas (O-Ring, Pull-In)
            - Preposição+apóstrofo: preposição minúscula, palavra capitalizada (d'Água)
            - Outras palavras capitalizadas (primeira letra maiúscula)
            """
            import re
            stopwords = load_stopwords(lang)
            words = label.split()
            corrected_words = []
            
            for i, word in enumerate(words):
                # Verificar se é palavra com apóstrofo (d'Água, l'État)
                apostrophe_match = None
                for prefix in apostrophe_prefixes:
                    if word.lower().startswith(prefix.lower()):
                        apostrophe_match = prefix
                        break
                
                if apostrophe_match:
                    # Preposição minúscula + palavra capitalizada
                    rest = word[len(apostrophe_match):]
                    corrected_words.append(apostrophe_match.lower() + rest.capitalize())
                elif '-' in word and not word.startswith('-') and not word.endswith('-'):
                    # Palavra com hífen: capitalizar cada parte
                    parts = word.split('-')
                    corrected_parts = [p.capitalize() for p in parts]
                    corrected_words.append('-'.join(corrected_parts))
                elif word.lower() in stopwords and i != 0:
                    corrected_words.append(word.lower())
                else:
                    corrected_words.append(word.capitalize())
            
            # Juntar e depois substituir acrônimos por UPPERCASE
            result = " ".join(corrected_words)
            for acronym in registered_acronyms:
                # Acrônimos ambíguos (ex: SEM) só são substituídos quando:
                # 1. São a primeira palavra do label
                # 2. Estão entre parênteses
                # Não substituir quando aparecem no meio de frases (ex: "sem tensão")
                if acronym.upper() in ambiguous_acronyms:
                    # Só substituir se for primeira palavra ou entre parênteses
                    # Pattern para primeira palavra
                    pattern_start = re.compile(r'^' + re.escape(acronym) + r'(?![a-zA-Z])', re.IGNORECASE)
                    # Pattern para entre parênteses
                    pattern_parens = re.compile(r'\(' + re.escape(acronym) + r'\)', re.IGNORECASE)
                    result = pattern_start.sub(acronym.upper(), result)
                    result = pattern_parens.sub('(' + acronym.upper() + ')', result)
                else:
                    # Acrônimos normais: substituir em qualquer posição como palavra isolada
                    pattern = re.compile(r'(?<![a-zA-Z])' + re.escape(acronym) + r'(?![a-zA-Z])', re.IGNORECASE)
                    result = pattern.sub(acronym.upper(), result)
            
            return result
        
        # Coletar mapeamento de URIs antigas -> novas
        uri_mapping = {}
        
        # Coletar correções de dcterms:identifier (subject -> novo valor)
        identifier_fixes = {}
        
        # Coletar valores antigos de identifier para relatório
        old_identifier_values = {}
        
        # Processar erros com sugestões de correção
        for error in validation_report.get("errors", []):
            if "expected" in error and error.get("expected"):
                subject = error.get("subject", "")
                expected = error.get("expected", "")
                rule = error.get("rule", "")
                
                # Ignorar sugestões que não são nomes de classe válidos
                # (ex: "Add: dcterms:identifier \"ClassName\"")
                if ":" in expected or " " in expected or '"' in expected:
                    continue
                
                # Auto-fix para dcterms:identifier.pattern (corrigir valor literal)
                if rule == "dcterms_identifier.pattern" and subject:
                    # Encontrar valor antigo do identifier para relatório
                    for s, p, o in graph:
                        if str(s) == subject and p == DCTERMS.identifier:
                            old_identifier_values[URIRef(subject)] = str(o)
                            break
                    identifier_fixes[URIRef(subject)] = expected
                    continue
                
                # Ignorar regras que não são para correção de URI
                # (dcterms_identifier.must_match_local_name sugere manter o nome atual, não corrigir)
                if rule == "dcterms_identifier.must_match_local_name":
                    continue
                
                # Auto-fix para URIs de classes/propriedades (owl_classes.pattern, owl_properties.pattern)
                # Extrair URI completa do subject
                if subject and rule in ("owl_classes.pattern", "owl_properties.pattern"):
                    # Expected contém apenas o local name, precisamos reconstruir a URI
                    # Exemplo: subject="http://energy.com/edo#basicDesign", expected="BasicDesign"
                    if "#" in subject:
                        namespace, _ = subject.rsplit("#", 1)
                        new_uri = f"{namespace}#{expected}"
                        uri_mapping[URIRef(subject)] = URIRef(new_uri)
                    elif "/" in subject and not subject.endswith("/"):
                        # URI com / como separador
                        namespace, _ = subject.rsplit("/", 1)
                        new_uri = f"{namespace}/{expected}"
                        uri_mapping[URIRef(subject)] = URIRef(new_uri)
        
        # Criar novo grafo com correções aplicadas (sempre processar para corrigir prefLabels)
        fixed_graph = RDFGraph()
        
        # Copiar namespaces
        for prefix, namespace in graph.namespaces():
            fixed_graph.bind(prefix, namespace)
        
        # Estatísticas de correções
        uri_occurrence_count = {str(old_uri): 0 for old_uri in uri_mapping.keys()}
        identifier_corrections_detail = {}
        preflabel_corrections_detail = {}
        definition_corrections_detail = {}
        pending_preflabel_corrections = {}  # Correções não aplicadas quando auto_fix=false
        pending_definition_corrections = {}  # Correções não aplicadas quando auto_fix=false
        total_triples_modified = 0
        total_triples_would_be_modified = 0  # Contador para modo validate-only
        total_preflabel_fixes = 0
        total_definition_fixes = 0
        
        # Aplicar correções em todas as triplas
        for s, p, o in graph:
            original_s, original_p, original_o = s, p, o
            modified = False
            would_be_modified = False  # Rastreia se tripla seria modificada
            
            # Substituir subject se necessário (somente se apply_corrections=True)
            if s in uri_mapping:
                would_be_modified = True
                if apply_corrections:
                    new_s = uri_mapping[s]
                    uri_occurrence_count[str(s)] += 1
                    modified = True
                else:
                    uri_occurrence_count[str(s)] += 1
                    new_s = s
            else:
                new_s = s
            
            # Substituir predicate se necessário (somente se apply_corrections=True)
            if p in uri_mapping:
                would_be_modified = True
                if apply_corrections:
                    new_p = uri_mapping[p]
                    uri_occurrence_count[str(p)] += 1
                    modified = True
                else:
                    uri_occurrence_count[str(p)] += 1
                    new_p = p
            else:
                new_p = p
            
            # Substituir object se for URIRef e estiver no mapeamento (somente se apply_corrections=True)
            if isinstance(o, URIRef) and o in uri_mapping:
                would_be_modified = True
                if apply_corrections:
                    new_o = uri_mapping[o]
                    uri_occurrence_count[str(o)] += 1
                    modified = True
                else:
                    uri_occurrence_count[str(o)] += 1
                    new_o = o
            else:
                new_o = o
            
            # Corrigir dcterms:identifier se necessário (somente se apply_corrections=True)
            if p == DCTERMS.identifier and s in identifier_fixes:
                would_be_modified = True
                if apply_corrections:
                    old_value = str(o)
                    new_o = Literal(identifier_fixes[s])
                    identifier_corrections_detail[str(s)] = {
                        "old_value": old_value,
                        "new_value": identifier_fixes[s]
                    }
                    modified = True
                else:
                    # Coletar correção pendente para relatório (não aplicar)
                    old_value = str(o)
                    identifier_corrections_detail[str(s)] = {
                        "old_value": old_value,
                        "new_value": identifier_fixes[s],
                        "pending": True  # Marca como não aplicada
                    }
            
            # Corrigir skos:prefLabel se necessário
            if p == SKOS.prefLabel and isinstance(o, Literal):
                old_value = str(o)
                lang = str(o.language) if o.language else "pt-br"
                corrected_value = correct_preflabel(old_value, lang)
                if corrected_value != old_value:
                    would_be_modified = True
                    correction_info = {
                        "old_value": old_value,
                        "new_value": corrected_value,
                        "lang": lang
                    }
                    
                    if auto_fix_preflabels:
                        # Aplicar correção
                        new_o = Literal(corrected_value, lang=o.language)
                        if str(s) not in preflabel_corrections_detail:
                            preflabel_corrections_detail[str(s)] = []
                        preflabel_corrections_detail[str(s)].append(correction_info)
                        total_preflabel_fixes += 1
                        modified = True
                    else:
                        # Coletar correção pendente (não aplicar)
                        if str(s) not in pending_preflabel_corrections:
                            pending_preflabel_corrections[str(s)] = []
                        pending_preflabel_corrections[str(s)].append(correction_info)
            
            # Corrigir skos:definition se necessário (adicionar ponto final + acrônimos se configurado)
            if p == SKOS.definition and isinstance(o, Literal):
                old_value = str(o)
                corrected_value = old_value.strip()
                # Adicionar ponto final se não terminar com pontuação
                if corrected_value and not corrected_value[-1] in ".!?":
                    corrected_value = corrected_value + "."
                # Corrigir acrônimos para UPPERCASE se configurado em rules.json
                if normalize_acronyms_in_definitions:
                    for acronym in registered_acronyms:
                        import re
                        pattern = re.compile(r'(?<![a-zA-Z])' + re.escape(acronym) + r'(?![a-zA-Z])', re.IGNORECASE)
                        corrected_value = pattern.sub(acronym.upper(), corrected_value)
                if corrected_value != old_value:
                    would_be_modified = True
                    lang = str(o.language) if o.language else ""
                    correction_info = {
                        "old_value": old_value,
                        "new_value": corrected_value,
                        "lang": lang
                    }
                    
                    if auto_fix_definitions:
                        # Aplicar correção
                        new_o = Literal(corrected_value, lang=o.language)
                        if str(s) not in definition_corrections_detail:
                            definition_corrections_detail[str(s)] = []
                        definition_corrections_detail[str(s)].append(correction_info)
                        total_definition_fixes += 1
                        modified = True
                    else:
                        # Coletar correção pendente (não aplicar)
                        if str(s) not in pending_definition_corrections:
                            pending_definition_corrections[str(s)] = []
                        pending_definition_corrections[str(s)].append(correction_info)
            
            # Contar tripla como modificada se houver qualquer alteração
            if modified:
                total_triples_modified += 1
            if would_be_modified:
                total_triples_would_be_modified += 1
            
            # Adicionar tripla corrigida
            fixed_graph.add((new_s, new_p, new_o))
        
        # Construir estatísticas de correção
        uri_corrections = {}
        for old_uri, new_uri in uri_mapping.items():
            uri_corrections[str(old_uri)] = {
                "new_uri": str(new_uri),
                "occurrences": uri_occurrence_count[str(old_uri)]
            }
        
        # RF-01: Usar contador apropriado baseado no modo
        # Em validate_only: reportar triplas que SERIAM modificadas
        # Em auto_fix: reportar triplas que FORAM modificadas
        effective_triples_modified = total_triples_modified if apply_corrections else total_triples_would_be_modified
        
        stats = {
            "uri_corrections": uri_corrections,
            "identifier_corrections": identifier_corrections_detail,
            "preflabel_corrections": preflabel_corrections_detail,
            "definition_corrections": definition_corrections_detail,
            "pending_preflabel_corrections": pending_preflabel_corrections,
            "pending_definition_corrections": pending_definition_corrections,
            "total_triples_modified": effective_triples_modified,
            "total_uri_replacements": sum(uri_occurrence_count.values()),
            "total_identifier_fixes": len(identifier_corrections_detail),
            "total_preflabel_fixes": total_preflabel_fixes,
            "total_definition_fixes": total_definition_fixes,
            "total_pending_preflabel_fixes": sum(len(v) for v in pending_preflabel_corrections.values()),
            "total_pending_definition_fixes": sum(len(v) for v in pending_definition_corrections.values()),
            # RF-01: Indica o modo de execução para auditoria
            "mode": "auto_fix" if apply_corrections else "validate_only"
        }
        
        return fixed_graph, stats

    def validate_encoding(self, file_path: str) -> bool:
        """
        Valida encoding UTF-8 conforme UC-101 fluxo alternativo
        
        Args:
            file_path: Caminho do arquivo TTL
        
        Returns:
            bool: True se encoding válido
        """
        validation_rules = self.rules.get("validation", {})
        
        if not validation_rules.get("check_utf8_encoding", True):
            return True  # Validação desabilitada
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return True
        except UnicodeDecodeError:
            return False
        except FileNotFoundError:
            return False

    def validate_serialization(self, graph: Graph) -> list[dict]:
        """
        Valida se a serialização do grafo está livre de problemas conhecidos.
        
        Verifica:
            - Ausência de prefixos automáticos (ns1, ns2, etc.)
            - Todos os namespaces usados estão vinculados
            - Não há literais onde deveriam ser URIs (ex: "owl:Class")
        
        Args:
            graph: Grafo RDF a validar
        
        Returns:
            list[dict]: Lista de problemas encontrados
        """
        from rdflib import Literal, URIRef
        
        problems = []
        
        # 1. Verificar prefixos automáticos (ns1, ns2, etc.)
        for prefix, namespace in graph.namespaces():
            if prefix and prefix.startswith("ns") and prefix[2:].isdigit():
                problems.append({
                    "type": "auto_generated_prefix",
                    "prefix": prefix,
                    "namespace": str(namespace),
                    "message": f"Prefixo automático '{prefix}' detectado. Vincule explicitamente o namespace {namespace}"
                })
        
        # 2. Verificar literais que parecem ser URIs
        uri_patterns = ["owl:", "rdf:", "rdfs:", "xsd:", "skos:", "dcterms:"]
        for s, p, o in graph:
            if isinstance(o, Literal):
                o_str = str(o)
                for pattern in uri_patterns:
                    if pattern in o_str:
                        problems.append({
                            "type": "literal_looks_like_uri",
                            "subject": str(s),
                            "predicate": str(p),
                            "object": o_str,
                            "message": f"Literal '{o_str}' parece ser uma URI. Use URIRef em vez de Literal."
                        })
                        break
        
        # 3. Coletar namespaces usados e verificar se estão vinculados
        used_namespaces = set()
        for s, p, o in graph:
            for term in (s, p, o):
                if isinstance(term, URIRef):
                    term_str = str(term)
                    if '#' in term_str:
                        ns = term_str.rsplit('#', 1)[0] + '#'
                    elif '/' in term_str:
                        ns = term_str.rsplit('/', 1)[0] + '/'
                    else:
                        ns = term_str
                    used_namespaces.add(ns)
        
        bound_namespaces = {str(ns) for _, ns in graph.namespaces()}
        unbound = used_namespaces - bound_namespaces
        
        for ns in unbound:
            problems.append({
                "type": "unbound_namespace",
                "namespace": ns,
                "message": f"Namespace '{ns}' usado mas não vinculado a um prefixo"
            })
        
        return problems
    
    def ensure_protege_compatibility(self, graph: Graph) -> Graph:
        """
        Garante que o grafo é compatível com Protégé.
        
        Realiza:
            - Vinculação explícita de todos os namespaces padrão
            - Correção de prefixos automáticos (ns1 -> prefixo apropriado)
            - Validação de estrutura de triplas
        
        Args:
            graph: Grafo RDF a processar
        
        Returns:
            Graph: Grafo compatível com Protégé
        """
        from rdflib import Graph as RDFGraph, Namespace
        from rdflib.namespace import NamespaceManager, RDF, RDFS, OWL, XSD
        from .uri_resolver import STANDARD_PREFIXES
        
        # Criar novo grafo com NamespaceManager limpo
        result = RDFGraph()
        result.namespace_manager = NamespaceManager(RDFGraph(), bind_namespaces="none")
        
        # Coletar prefixos existentes (exceto automáticos)
        existing_prefixes = {}
        for prefix, namespace in graph.namespaces():
            if prefix and not (prefix.startswith("ns") and prefix[2:].isdigit()):
                existing_prefixes[prefix] = namespace
        
        # Adicionar prefixos padrão obrigatórios primeiro
        standard_ns = {
            "rdf": RDF,
            "rdfs": RDFS,
            "owl": OWL,
            "xsd": XSD,
        }
        for prefix, ns in standard_ns.items():
            result.bind(prefix, ns, override=True, replace=True)
        
        # Adicionar prefixos existentes
        for prefix, namespace in sorted(existing_prefixes.items()):
            if prefix not in standard_ns:
                result.bind(prefix, namespace, override=True, replace=True)
        
        # Detectar e vincular namespaces usados mas não vinculados
        for s, p, o in graph:
            for term in (s, p, o):
                term_str = str(term)
                # Extrair namespace
                if '#' in term_str:
                    ns_str = term_str.rsplit('#', 1)[0] + '#'
                elif '/' in term_str:
                    ns_str = term_str.rsplit('/', 1)[0] + '/'
                else:
                    continue
                
                # Verificar se já está vinculado
                is_bound = False
                for _, bound_ns in result.namespaces():
                    if str(bound_ns) == ns_str:
                        is_bound = True
                        break
                
                if not is_bound:
                    # Tentar encontrar prefixo conhecido
                    for prefix, known_ns in STANDARD_PREFIXES.items():
                        if known_ns == ns_str:
                            result.bind(prefix, Namespace(ns_str), override=True, replace=True)
                            break
        
        # Copiar triplas
        for s, p, o in graph:
            result.add((s, p, o))
        
        return result

    def get_warnings(self) -> list[dict]:
        """
        Retorna lista de avisos de validação da última normalização.
        
        Returns:
            list[dict]: Lista de avisos com estrutura:
                {
                    "type": str,  # Tipo do aviso (e.g., "missing_required_prefix")
                    "message": str,  # Mensagem legível
                    ...: ...,  # Campos específicos do tipo de aviso
                }
        """
        return self.validation_warnings.copy()
    
    def get_naming_validation_report(self) -> dict | None:
        """
        Retorna relatório completo de validação de nomenclatura.
        
        Returns:
            dict | None: Relatório de validação do NamingValidator ou None se não executado
        """
        return self.naming_validation_report
    
    def get_naming_fix_stats(self) -> dict | None:
        """
        Retorna estatísticas de correções aplicadas durante a normalização.
        
        Returns:
            dict | None: Estatísticas de correções ou None se não houve correções
            
        Estrutura:
            {
                "uri_corrections": {
                    "old_uri": {"new_uri": str, "occurrences": int},
                    ...
                },
                "identifier_corrections": {
                    "subject_uri": {"old_value": str, "new_value": str},
                    ...
                },
                "total_triples_modified": int,
                "total_uri_replacements": int,
                "total_identifier_fixes": int
            }
        """
        return self.naming_fix_stats

    @classmethod
    def compare_serialization(cls, a: str, b: str) -> bool:
        """Compara serializações ignorando comentários e whitespace"""
        lines_a = [line.strip() for line in a.splitlines() if line.strip() and not line.strip().startswith("#")]
        lines_b = [line.strip() for line in b.splitlines() if line.strip() and not line.strip().startswith("#")]
        
        return lines_a == lines_b
