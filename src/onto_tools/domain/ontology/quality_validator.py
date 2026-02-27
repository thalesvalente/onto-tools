"""
OntologyQualityValidator — Validação de qualidade de ontologias

Implementa regras de validação conforme especificação de domínio:
- skos:prefLabel & skos:definition duplicatas
- dcterms:identifier obrigatório e match com local name
- ifc cluster (propriedades obrigatórias para classes IFC)
- skos:altLabel Title Case
- DomainAttribute constraints (accessRights, identifier, definitions,
  prefLabels, mandatory properties)

Este validador NÃO modifica o grafo, apenas emite issues de validação.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Optional

from rdflib import Graph, URIRef, Literal as RDFLiteral, Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS


# Namespace EDO
EDO = Namespace("https://w3id.org/energy-domain/edo#")


@dataclass
class ValidationIssue:
    """Representa um issue de validação encontrado na ontologia."""
    code: str
    severity: Literal["INFO", "WARNING", "ERROR"]
    subject: URIRef
    predicate: Optional[URIRef] = None
    message: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Converte para dicionário serializável."""
        return {
            "code": self.code,
            "severity": self.severity,
            "subject": str(self.subject),
            "predicate": str(self.predicate) if self.predicate else None,
            "message": self.message,
            "extra": self.extra
        }


@dataclass
class ValidationReport:
    """Relatório de validação com lista de issues."""
    issues: list[ValidationIssue] = field(default_factory=list)
    total_classes_checked: int = 0
    total_issues: int = 0
    
    def add_issue(self, issue: ValidationIssue) -> None:
        """Adiciona um issue ao relatório."""
        self.issues.append(issue)
        self.total_issues = len(self.issues)
    
    def get_errors(self) -> list[ValidationIssue]:
        """Retorna apenas issues de severidade ERROR."""
        return [i for i in self.issues if i.severity == "ERROR"]
    
    def get_warnings(self) -> list[ValidationIssue]:
        """Retorna apenas issues de severidade WARNING."""
        return [i for i in self.issues if i.severity == "WARNING"]
    
    def has_errors(self) -> bool:
        """Verifica se há erros."""
        return any(i.severity == "ERROR" for i in self.issues)
    
    def to_dict(self) -> dict:
        """Converte para dicionário serializável."""
        return {
            "total_classes_checked": self.total_classes_checked,
            "total_issues": self.total_issues,
            "errors_count": len(self.get_errors()),
            "warnings_count": len(self.get_warnings()),
            "issues": [i.to_dict() for i in self.issues]
        }


class OntologyQualityValidator:
    """
    Validador de qualidade de ontologias.
    
    Implementa regras de validação sem modificar o grafo:
    - Duplicatas de prefLabel/definition
    - Identifier obrigatório e match com local name
    - ifc cluster constraints
    - altLabel Title Case
    """
    
    DEFAULT_RULES_PATH = Path(__file__).parent.parent.parent.parent.parent / "data" / "examples" / "rules.json"
    
    def __init__(self, rules_path: Optional[str] = None):
        """
        Inicializa o validador.
        
        Args:
            rules_path: Caminho para rules.json (opcional)
        """
        self.rules = self._load_rules(rules_path)
        self._title_case_exceptions_en = set()
        self._title_case_exceptions_pt = set()
        self._load_title_case_config()
    
    def _load_rules(self, rules_path: Optional[str] = None) -> dict:
        """Carrega regras do arquivo JSON."""
        path = Path(rules_path) if rules_path else self.DEFAULT_RULES_PATH
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("rules", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _load_title_case_config(self) -> None:
        """Carrega configurações de Title Case e regex das regras."""
        naming_syntax = self.rules.get("naming_syntax", {})
        preflabels = naming_syntax.get("skos_preflabels", {})
        
        english = preflabels.get("english", {})
        self._title_case_exceptions_en = set(english.get("exceptions", []))
        
        portuguese = preflabels.get("portuguese", {})
        self._title_case_exceptions_pt = set(portuguese.get("exceptions", []))
        
        # Compilar regex para validação de prefLabel
        regex_pattern = preflabels.get("regex")
        self._preflabel_regex = re.compile(regex_pattern) if regex_pattern else None
    
    def validate(self, graph: Graph) -> ValidationReport:
        """
        Executa todas as validações no grafo.
        
        Args:
            graph: Grafo RDF a validar
            
        Returns:
            ValidationReport com todos os issues encontrados
        """
        report = ValidationReport()
        
        # Encontrar todas as classes OWL
        classes = list(graph.subjects(RDF.type, OWL.Class))
        report.total_classes_checked = len(classes)
        
        # Identificar classes DomainAttribute para validação específica
        domain_attribute_classes = self._get_domain_attribute_subclasses(graph)
        
        for class_uri in classes:
            if not isinstance(class_uri, URIRef):
                continue
            
            # Validar identifier
            self._validate_identifier(graph, class_uri, report)
            
            # Validar prefLabel regex
            self._validate_preflabel_regex(graph, class_uri, report)
            
            # Validar prefLabel Title Case
            self._validate_preflabel_title_case(graph, class_uri, report)
            
            # Validar prefLabel duplicates
            self._validate_preflabel_duplicates(graph, class_uri, report)
            
            # Validar definition multiplicity
            self._validate_definition_multiplicity(graph, class_uri, report)
            
            # Validar altLabel Title Case
            self._validate_altlabel_title_case(graph, class_uri, report)
            
            # Validar ifc cluster
            self._validate_ifc_constraints(graph, class_uri, report)
            
            # Validar DomainAttribute constraints (se for subclasse de DomainAttribute)
            if class_uri in domain_attribute_classes:
                self._validate_domain_attribute_constraints(graph, class_uri, report)
        
        return report
    
    def _get_local_name(self, uri: URIRef) -> str:
        """Extrai o local name de uma URI."""
        uri_str = str(uri)
        if '#' in uri_str:
            return uri_str.rsplit('#', 1)[-1]
        elif '/' in uri_str:
            return uri_str.rsplit('/', 1)[-1]
        return uri_str
    
    def _validate_identifier(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """Valida dcterms:identifier para uma classe."""
        naming_syntax = self.rules.get("naming_syntax", {})
        id_rules = naming_syntax.get("dcterms_identifier", {})
        
        if not id_rules.get("must_exist_for_classes", True):
            return
        
        # Buscar identifier
        identifiers = list(graph.objects(class_uri, DCTERMS.identifier))
        
        if not identifiers:
            # CLASS_IDENTIFIER_MISSING
            severity = id_rules.get("severity_when_missing", "ERROR")
            report.add_issue(ValidationIssue(
                code="CLASS_IDENTIFIER_MISSING",
                severity=severity,
                subject=class_uri,
                predicate=DCTERMS.identifier,
                message=f"Classe '{self._get_local_name(class_uri)}' não possui dcterms:identifier",
                extra={"expected": self._get_local_name(class_uri)}
            ))
            return
        
        # Validar match com local name
        if id_rules.get("must_match_local_name", True):
            local_name = self._get_local_name(class_uri)
            identifier_value = str(identifiers[0])
            
            if identifier_value != local_name:
                severity = id_rules.get("severity_when_mismatch", "ERROR")
                report.add_issue(ValidationIssue(
                    code="CLASS_IDENTIFIER_MISMATCH",
                    severity=severity,
                    subject=class_uri,
                    predicate=DCTERMS.identifier,
                    message=f"dcterms:identifier '{identifier_value}' não corresponde ao local name '{local_name}'",
                    extra={
                        "identifier_value": identifier_value,
                        "expected": local_name
                    }
                ))
    
    def _identify_preflabel_cause(self, value: str, lang: str) -> str:
        """
        Identifica a causa específica de uma violação de formato de prefLabel.
        
        Args:
            value: O valor do prefLabel
            lang: O idioma do label
            
        Returns:
            Descrição da causa da violação
        """
        import re
        
        # Verificar se contém caracteres especiais inválidos
        # Permitidos: letras, números, espaços, hífens, apóstrofos, acentos, parênteses, barra
        if re.search(r'[^\w\s\-\'\u00C0-\u017F()/]', value):
            invalid_chars = re.findall(r'[^\w\s\-\'\u00C0-\u017F()/]', value)
            return f"contém caracteres inválidos: {invalid_chars}"
        
        # Verificar se tem espaços múltiplos
        if '  ' in value:
            return "contém espaços múltiplos consecutivos"
        
        # Verificar se começa com minúscula
        if value and value[0].islower():
            return "primeira letra deve ser maiúscula"
        
        # Verificar palavras individuais para capitalização incorreta
        words = value.split()
        for i, word in enumerate(words):
            # Pular palavras com hífen (tratadas separadamente)
            if '-' in word:
                continue
            # Primeira palavra deve começar com maiúscula
            if i == 0 and word and word[0].islower():
                return f"primeira palavra '{word}' deve começar com maiúscula"
            # Palavras do meio em minúsculo podem ser stopwords (ok) ou erros
            if i > 0 and word and word[0].isupper():
                # Se começa com maiúscula, está ok
                continue
        
        # Causa genérica se não identificada especificamente
        return "formato não corresponde ao padrão Title Case esperado"
    
    def _validate_preflabel_regex(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """
        Valida skos:prefLabel contra regex de formato.
        
        A regex padrão valida Title Case: primeira palavra capitalizada,
        palavras separadas por espaço, permite hífens.
        """
        if not self._preflabel_regex:
            return
        
        naming_syntax = self.rules.get("naming_syntax", {})
        preflabels_config = naming_syntax.get("skos_preflabels", {})
        
        for label in graph.objects(class_uri, SKOS.prefLabel):
            if isinstance(label, RDFLiteral):
                value = str(label)
                lang = label.language or "none"
                
                if not self._preflabel_regex.match(value):
                    # Identificar a causa específica da violação
                    cause = self._identify_preflabel_cause(value, lang)
                    report.add_issue(ValidationIssue(
                        code="PREFLABEL_FORMAT_INVALID",
                        severity="WARNING",
                        subject=class_uri,
                        predicate=SKOS.prefLabel,
                        message=f"skos:prefLabel '{value}'@{lang} não corresponde ao padrão esperado. Causa: {cause}",
                        extra={
                            "value": value,
                            "language": lang,
                            "expected_pattern": preflabels_config.get("regex_description", "Title Case"),
                            "regex": preflabels_config.get("regex", ""),
                            "cause": cause
                        }
                    ))
    
    def _validate_preflabel_title_case(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """
        Valida se skos:prefLabel segue Title Case corretamente.
        
        Regras:
        - Primeira palavra sempre capitalizada
        - Palavras significativas (não-stopwords) devem ser capitalizadas
        - Stopwords podem ser minúsculas (exceto primeira palavra)
        - Acrônimos devem ser UPPERCASE
        """
        naming_syntax = self.rules.get("naming_syntax", {})
        preflabels_config = naming_syntax.get("skos_preflabels", {})
        
        # Verificar se validação de Title Case está habilitada
        if not preflabels_config.get("validate_title_case", True):
            return
        
        # Carregar stopwords
        stopwords_config = naming_syntax.get("stopwords", {})
        
        # Carregar acrônimos registrados
        acronyms_config = naming_syntax.get("acronyms", {})
        registered_acronyms = set(acronyms_config.get("list", []))
        
        for label in graph.objects(class_uri, SKOS.prefLabel):
            if isinstance(label, RDFLiteral):
                value = str(label)
                lang = label.language or "none"
                
                # Obter stopwords para o idioma
                if lang.startswith("pt"):
                    stopwords = set(stopwords_config.get("pt_br", []))
                else:
                    stopwords = set(stopwords_config.get("en", []))
                
                # Verificar Title Case
                issues = self._check_title_case(value, stopwords, registered_acronyms)
                
                if issues:
                    report.add_issue(ValidationIssue(
                        code="PREFLABEL_FORMAT_INVALID",
                        severity="WARNING",
                        subject=class_uri,
                        predicate=SKOS.prefLabel,
                        message=f"skos:prefLabel '{value}'@{lang} não corresponde ao padrão esperado. Causa: {issues[0]}",
                        extra={
                            "value": value,
                            "language": lang,
                            "expected_pattern": "Title Case",
                            "issues": issues
                        }
                    ))
    
    def _check_title_case(self, value: str, stopwords: set, acronyms: set) -> list:
        """
        Verifica se um valor segue Title Case corretamente.
        
        Returns:
            Lista de problemas encontrados (vazia se estiver correto)
        """
        issues = []
        words = value.split()
        
        for i, word in enumerate(words):
            # Ignorar palavras vazias
            if not word:
                continue
            
            # Tratar palavras com parênteses - ex: "(CO2)"
            clean_word = word.strip("()")
            
            # Se é um acrônimo registrado, deve ser UPPERCASE
            if clean_word.upper() in acronyms:
                if clean_word != clean_word.upper():
                    issues.append(f"acrônimo '{clean_word}' deve ser maiúsculo: {clean_word.upper()}")
                continue
            
            # Tratar palavras com hífen - cada parte deve ser analisada
            if '-' in word:
                parts = word.split('-')
                for part in parts:
                    if part and part[0].islower() and part.lower() not in stopwords:
                        issues.append(f"palavra '{part}' em '{word}' deve começar com maiúscula")
                continue
            
            # Primeira palavra deve sempre ser capitalizada
            if i == 0:
                if clean_word and clean_word[0].islower():
                    issues.append(f"primeira palavra '{word}' deve começar com maiúscula")
                continue
            
            # Stopwords podem ser minúsculas
            if clean_word.lower() in stopwords:
                continue
            
            # Palavras não-stopwords devem começar com maiúscula
            if clean_word and clean_word[0].islower():
                issues.append(f"palavra '{word}' deve começar com maiúscula (não é stopword)")
        
        return issues
    
    def _validate_preflabel_duplicates(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """
        Valida duplicatas de skos:prefLabel.
        
        Nota: RDF é baseado em conjuntos, portanto triplas idênticas são armazenadas
        uma única vez. Esta validação detecta MÚLTIPLOS prefLabels DISTINTOS no mesmo idioma,
        o que viola a convenção SKOS de um prefLabel por idioma.
        """
        validation = self.rules.get("validation", {})
        skos_labels = validation.get("skos_labels", {})
        
        if not skos_labels.get("warn_duplicate_prefLabel", True):
            return
        
        # Coletar prefLabels agrupados por language
        preflabels_by_lang: dict[str, list[str]] = {}
        for label in graph.objects(class_uri, SKOS.prefLabel):
            if isinstance(label, RDFLiteral):
                lang = label.language or "none"
                value = str(label)
                if lang not in preflabels_by_lang:
                    preflabels_by_lang[lang] = []
                preflabels_by_lang[lang].append(value)
        
        # Verificar se há múltiplos prefLabels no mesmo idioma
        for lang, labels in preflabels_by_lang.items():
            if len(labels) > 1:
                # Múltiplos prefLabels distintos no mesmo idioma = warning
                report.add_issue(ValidationIssue(
                    code="MULTIPLE_PREFLABEL_SAME_LANG",
                    severity="WARNING",
                    subject=class_uri,
                    predicate=SKOS.prefLabel,
                    message=f"Classe tem {len(labels)} skos:prefLabel para idioma '{lang}': {labels}",
                    extra={"language": lang, "values": labels, "count": len(labels)}
                ))
    
    def _validate_definition_multiplicity(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """Valida multiplicidade de skos:definition."""
        validation = self.rules.get("validation", {})
        skos_defs = validation.get("skos_definitions", {})
        
        max_per_class = skos_defs.get("max_per_class", 1)
        warn_if_exceeds = skos_defs.get("warn_if_exceeds", True)
        
        if not warn_if_exceeds:
            return
        
        # Contar definitions por language
        definitions_by_lang: dict[str, int] = {}
        for definition in graph.objects(class_uri, SKOS.definition):
            if isinstance(definition, RDFLiteral):
                lang = definition.language or "none"
                definitions_by_lang[lang] = definitions_by_lang.get(lang, 0) + 1
        
        # Verificar se excede o máximo por idioma
        for lang, count in definitions_by_lang.items():
            if count > max_per_class:
                report.add_issue(ValidationIssue(
                    code="MULTIPLE_DEFINITION",
                    severity="WARNING",
                    subject=class_uri,
                    predicate=SKOS.definition,
                    message=f"Classe tem {count} skos:definition para idioma '{lang}' (máximo: {max_per_class})",
                    extra={"language": lang, "count": count, "max": max_per_class}
                ))
    
    def _validate_altlabel_title_case(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """Valida Title Case de skos:altLabel."""
        validation = self.rules.get("validation", {})
        altlabel_rules = validation.get("skos_altlabels", {})
        
        if not altlabel_rules.get("validate_title_case", True):
            return
        
        for altlabel in graph.objects(class_uri, SKOS.altLabel):
            if not isinstance(altlabel, RDFLiteral):
                continue
            
            value = str(altlabel)
            lang = altlabel.language or "en"
            
            # Validar Title Case
            if not self._is_valid_title_case(value, lang):
                report.add_issue(ValidationIssue(
                    code="ALTLABEL_TITLECASE_VIOLATION",
                    severity="WARNING",
                    subject=class_uri,
                    predicate=SKOS.altLabel,
                    message=f"skos:altLabel '{value}'@{lang} não segue Title Case",
                    extra={
                        "value": value,
                        "language": lang,
                        "expected": self._to_title_case(value, lang)
                    }
                ))
    
    def _is_valid_title_case(self, text: str, lang: str) -> bool:
        """Verifica se o texto segue Title Case para o idioma."""
        if not text:
            return True
        
        expected = self._to_title_case(text, lang)
        return text == expected
    
    def _to_title_case(self, text: str, lang: str) -> str:
        """Converte texto para Title Case conforme regras do idioma."""
        if not text:
            return text
        
        words = text.split()
        if not words:
            return text
        
        exceptions = self._title_case_exceptions_pt if lang.startswith("pt") else self._title_case_exceptions_en
        
        result = []
        for i, word in enumerate(words):
            # Primeira palavra sempre capitalizada
            if i == 0:
                result.append(word.capitalize())
            # Exceções em minúsculo (exceto primeira palavra)
            elif word.lower() in exceptions:
                result.append(word.lower())
            # Palavras com hífen
            elif '-' in word:
                parts = word.split('-')
                capitalized_parts = []
                for j, part in enumerate(parts):
                    if j == 0 or part.lower() not in exceptions:
                        capitalized_parts.append(part.capitalize())
                    else:
                        capitalized_parts.append(part.lower())
                result.append('-'.join(capitalized_parts))
            # Acrônimos (todas maiúsculas)
            elif word.isupper() and len(word) > 1:
                result.append(word)
            else:
                result.append(word.capitalize())
        
        return ' '.join(result)
    
    def _validate_ifc_constraints(self, graph: Graph, class_uri: URIRef, report: ValidationReport) -> None:
        """Valida constraints de classes IFC."""
        validation = self.rules.get("validation", {})
        ifc_constraints = validation.get("ifc_constraints", {})
        
        if not ifc_constraints:
            return
        
        # Detectar se é uma classe IFC de duas formas:
        # 1. Se herda de IfcInstanciableElement (ou base class configurada)
        # 2. Se tem alguma propriedade edo:ifc_*
        is_ifc_class = False
        
        # Método 1: Verificar se herda de IfcInstanciableElement
        require_base = ifc_constraints.get("require_ifc_base_class")
        if require_base:
            base_uri = self._resolve_prefixed_uri(require_base)
            if base_uri:
                subclass_of = list(graph.objects(class_uri, RDFS.subClassOf))
                if any(str(sc) == str(base_uri) for sc in subclass_of):
                    is_ifc_class = True
        
        # Método 2: Verificar se a classe tem alguma propriedade ifc_*
        if not is_ifc_class:
            for pred in graph.predicates(class_uri, None):
                pred_str = str(pred)
                # Verificar se o predicado contém "ifc" (case insensitive)
                if "ifc" in pred_str.lower() and "edo" in pred_str.lower():
                    is_ifc_class = True
                    break
        
        if not is_ifc_class:
            return
        
        # Validar propriedades obrigatórias - criar issue para CADA propriedade faltante
        required_props = ifc_constraints.get("required_properties", [])
        severity_missing_prop = ifc_constraints.get("severity_missing_property", "ERROR")
        missing_props = []
        
        for prop_prefixed in required_props:
            # Converter prefixo para URI
            prop_uri = self._resolve_prefixed_uri(prop_prefixed)
            
            if prop_uri and not list(graph.objects(class_uri, prop_uri)):
                missing_props.append(prop_prefixed)
                report.add_issue(ValidationIssue(
                    code="IFC_REQUIRED_PROPERTY_MISSING",
                    severity=severity_missing_prop,
                    subject=class_uri,
                    predicate=prop_uri,
                    message=f"Classe IFC sem propriedade obrigatória: {prop_prefixed}",
                    extra={"missing_property": prop_prefixed}
                ))
        
        # Validar base class (se ainda não foi validado acima)
        if require_base:
            base_uri = self._resolve_prefixed_uri(require_base)
            
            if base_uri:
                # Verificar se tem rdfs:subClassOf base_uri
                subclass_of = list(graph.objects(class_uri, RDFS.subClassOf))
                has_base = any(str(sc) == str(base_uri) for sc in subclass_of)
                
                if not has_base:
                    severity_base = ifc_constraints.get("severity_missing_base_class", "ERROR")
                    report.add_issue(ValidationIssue(
                        code="IFC_BASE_CLASS_MISSING",
                        severity=severity_base,
                        subject=class_uri,
                        predicate=RDFS.subClassOf,
                        message=f"Classe IFC não herda de {require_base}",
                        extra={"required_base_class": require_base}
                    ))
    
    def _resolve_prefixed_uri(self, prefixed: str) -> Optional[URIRef]:
        """Resolve uma URI prefixada para URIRef."""
        if ':' not in prefixed:
            return None
        
        prefix, local = prefixed.split(':', 1)
        
        # Namespaces conhecidos
        namespaces = {
            "edo": EDO,
            "rdf": RDF,
            "rdfs": RDFS,
            "owl": OWL,
            "skos": SKOS,
            "dcterms": DCTERMS
        }
        
        ns = namespaces.get(prefix.lower())
        if ns:
            return ns[local]
        
        return None
    
    # =========================================================================
    # DomainAttribute Constraints Validation
    # =========================================================================
    
    def _get_domain_attribute_subclasses(self, graph: Graph) -> set[URIRef]:
        """
        Seleciona todas as classes que são subclasses de edo:DomainAttribute.
        
        Inclui subclasses indiretas se configurado.
        """
        validation = self.rules.get("validation", {})
        da_constraints = validation.get("domain_attribute_constraints", {})
        
        if not da_constraints:
            return set()
        
        selector = da_constraints.get("class_selector", {})
        base_class_prefixed = selector.get("subClassOf", "edo:DomainAttribute")
        include_indirect = selector.get("include_indirect_subclasses", True)
        
        base_uri = self._resolve_prefixed_uri(base_class_prefixed)
        if not base_uri:
            return set()
        
        domain_attribute_classes: set[URIRef] = set()
        
        # Coletar todas as classes OWL
        all_classes = set(graph.subjects(RDF.type, OWL.Class))
        
        if include_indirect:
            # Fazer traversal transitivo para subclasses indiretas
            # Construir mapa de subclasses
            subclass_map: dict[URIRef, set[URIRef]] = {}
            for cls in all_classes:
                if isinstance(cls, URIRef):
                    superclasses = set(graph.objects(cls, RDFS.subClassOf))
                    subclass_map[cls] = {sc for sc in superclasses if isinstance(sc, URIRef)}
            
            # Para cada classe, verificar se DomainAttribute está na cadeia de ancestrais
            def has_ancestor(cls: URIRef, target: URIRef, visited: set[URIRef]) -> bool:
                if cls in visited:
                    return False
                visited.add(cls)
                
                superclasses = subclass_map.get(cls, set())
                if target in superclasses:
                    return True
                
                for sc in superclasses:
                    if has_ancestor(sc, target, visited):
                        return True
                return False
            
            for cls in all_classes:
                if isinstance(cls, URIRef):
                    if has_ancestor(cls, base_uri, set()):
                        domain_attribute_classes.add(cls)
        else:
            # Apenas subclasses diretas
            for cls in all_classes:
                if isinstance(cls, URIRef):
                    superclasses = set(graph.objects(cls, RDFS.subClassOf))
                    if base_uri in superclasses:
                        domain_attribute_classes.add(cls)
        
        return domain_attribute_classes
    
    def _validate_domain_attribute_constraints(
        self, graph: Graph, class_uri: URIRef, report: ValidationReport
    ) -> None:
        """
        Valida todas as constraints de DomainAttribute para uma classe.
        
        Emite warnings conforme especificação, NÃO modifica o grafo.
        """
        validation = self.rules.get("validation", {})
        da_constraints = validation.get("domain_attribute_constraints", {})
        
        if not da_constraints:
            return
        
        # 1. Validar dcterms:accessRights
        self._validate_da_access_rights(graph, class_uri, da_constraints, report)
        
        # 2. Validar dcterms:identifier (must match local name)
        self._validate_da_identifier(graph, class_uri, da_constraints, report)
        
        # 3. Validar skos:definition rules
        self._validate_da_definitions(graph, class_uri, da_constraints, report)
        
        # 4. Validar skos:prefLabel rules
        self._validate_da_preflabels(graph, class_uri, da_constraints, report)
        
        # 5. Validar mandatory properties
        self._validate_da_mandatory_properties(graph, class_uri, da_constraints, report)
    
    def _validate_da_access_rights(
        self, graph: Graph, class_uri: URIRef, config: dict, report: ValidationReport
    ) -> None:
        """Valida dcterms:accessRights para DomainAttribute."""
        access_rights_config = config.get("access_rights", {})
        
        if not access_rights_config.get("required", True):
            return
        
        predicate = self._resolve_prefixed_uri(
            access_rights_config.get("predicate", "dcterms:accessRights")
        )
        
        if not predicate:
            return
        
        access_rights_values = list(graph.objects(class_uri, predicate))
        
        if not access_rights_values:
            severity = access_rights_config.get("severity_missing", "WARNING")
            report.add_issue(ValidationIssue(
                code="DOMAINATTR_ACCESSRIGHTS_MISSING",
                severity=severity,
                subject=class_uri,
                predicate=predicate,
                message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui dcterms:accessRights",
                extra={}
            ))
    
    def _validate_da_identifier(
        self, graph: Graph, class_uri: URIRef, config: dict, report: ValidationReport
    ) -> None:
        """Valida dcterms:identifier para DomainAttribute (must match local name)."""
        id_config = config.get("identifier", {})
        
        if not id_config.get("required", True):
            return
        
        predicate = self._resolve_prefixed_uri(
            id_config.get("predicate", "dcterms:identifier")
        )
        
        if not predicate:
            return
        
        identifiers = list(graph.objects(class_uri, predicate))
        local_name = self._get_local_name(class_uri)
        
        if not identifiers:
            severity = id_config.get("severity_missing", "WARNING")
            report.add_issue(ValidationIssue(
                code="DOMAINATTR_IDENTIFIER_MISSING",
                severity=severity,
                subject=class_uri,
                predicate=predicate,
                message=f"DomainAttribute '{local_name}' não possui dcterms:identifier",
                extra={"expected": local_name}
            ))
            return
        
        # Verificar se identifier corresponde ao local name
        if id_config.get("must_match_local_name", True):
            identifier_values = [str(v) for v in identifiers]
            
            if local_name not in identifier_values:
                severity = id_config.get("severity_mismatch", "WARNING")
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_IDENTIFIER_MISMATCH",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"dcterms:identifier '{identifier_values[0]}' não corresponde ao local name '{local_name}'",
                    extra={
                        "identifier_value": identifier_values[0],
                        "expected": local_name
                    }
                ))
    
    def _validate_da_definitions(
        self, graph: Graph, class_uri: URIRef, config: dict, report: ValidationReport
    ) -> None:
        """Valida skos:definition para DomainAttribute."""
        def_config = config.get("definitions", {})
        
        predicate = self._resolve_prefixed_uri(
            def_config.get("predicate", "skos:definition")
        )
        
        if not predicate:
            return
        
        # Coletar definitions por idioma
        definitions_by_lang: dict[str, list[str]] = {}
        for definition in graph.objects(class_uri, predicate):
            if isinstance(definition, RDFLiteral):
                lang = definition.language or "none"
                value = str(definition)
                if lang not in definitions_by_lang:
                    definitions_by_lang[lang] = []
                definitions_by_lang[lang].append(value)
        
        # Verificar required languages
        if def_config.get("require_en", True):
            if "en" not in definitions_by_lang:
                severity = def_config.get("severity_missing_required_lang", "WARNING")
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_DEFINITION_MISSING_EN",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui skos:definition em inglês (@en)",
                    extra={"missing_language": "en"}
                ))
        
        if def_config.get("require_pt_br", True):
            if "pt-br" not in definitions_by_lang:
                severity = def_config.get("severity_missing_required_lang", "WARNING")
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_DEFINITION_MISSING_PT_BR",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui skos:definition em português (@pt-br)",
                    extra={"missing_language": "pt-br"}
                ))
        
        # Verificar multiplicidade por idioma
        if def_config.get("warn_if_more_than_one_per_lang", True):
            for lang, defs in definitions_by_lang.items():
                if len(defs) > 1:
                    severity = def_config.get("severity_too_many_per_lang", "WARNING")
                    report.add_issue(ValidationIssue(
                        code="DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG",
                        severity=severity,
                        subject=class_uri,
                        predicate=predicate,
                        message=f"DomainAttribute '{self._get_local_name(class_uri)}' possui {len(defs)} skos:definition para idioma '{lang}'",
                        extra={"language": lang, "count": len(defs), "values": defs}
                    ))
    
    def _validate_da_preflabels(
        self, graph: Graph, class_uri: URIRef, config: dict, report: ValidationReport
    ) -> None:
        """Valida skos:prefLabel para DomainAttribute."""
        pref_config = config.get("pref_labels", {})
        
        predicate = self._resolve_prefixed_uri(
            pref_config.get("predicate", "skos:prefLabel")
        )
        
        if not predicate:
            return
        
        # Coletar prefLabels por idioma
        preflabels_by_lang: dict[str, list[str]] = {}
        for label in graph.objects(class_uri, predicate):
            if isinstance(label, RDFLiteral):
                lang = label.language or "none"
                value = str(label)
                if lang not in preflabels_by_lang:
                    preflabels_by_lang[lang] = []
                preflabels_by_lang[lang].append(value)
        
        # Verificar required languages
        if pref_config.get("require_en", True):
            if "en" not in preflabels_by_lang:
                severity = pref_config.get("severity_missing_required_lang", "WARNING")
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_PREFLABEL_MISSING_EN",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui skos:prefLabel em inglês (@en)",
                    extra={"missing_language": "en"}
                ))
        
        if pref_config.get("require_pt_br", True):
            if "pt-br" not in preflabels_by_lang:
                severity = pref_config.get("severity_missing_required_lang", "WARNING")
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_PREFLABEL_MISSING_PT_BR",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui skos:prefLabel em português (@pt-br)",
                    extra={"missing_language": "pt-br"}
                ))
        
        # Verificar duplicatas por idioma
        if pref_config.get("warn_on_duplicate_per_lang", True):
            for lang, labels in preflabels_by_lang.items():
                if len(labels) > 1:
                    severity = pref_config.get("severity_duplicate", "WARNING")
                    report.add_issue(ValidationIssue(
                        code="DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG",
                        severity=severity,
                        subject=class_uri,
                        predicate=predicate,
                        message=f"DomainAttribute '{self._get_local_name(class_uri)}' possui {len(labels)} skos:prefLabel para idioma '{lang}'",
                        extra={"language": lang, "count": len(labels), "values": labels}
                    ))
    
    def _validate_da_mandatory_properties(
        self, graph: Graph, class_uri: URIRef, config: dict, report: ValidationReport
    ) -> None:
        """Valida propriedades obrigatórias de DomainAttribute."""
        mand_config = config.get("mandatory_properties", {})
        required_predicates = mand_config.get("required_predicates", [])
        severity = mand_config.get("severity_missing", "WARNING")
        
        for pred_prefixed in required_predicates:
            predicate = self._resolve_prefixed_uri(pred_prefixed)
            
            if not predicate:
                continue
            
            values = list(graph.objects(class_uri, predicate))
            
            if not values:
                report.add_issue(ValidationIssue(
                    code="DOMAINATTR_PROPERTY_MISSING",
                    severity=severity,
                    subject=class_uri,
                    predicate=predicate,
                    message=f"DomainAttribute '{self._get_local_name(class_uri)}' não possui propriedade obrigatória: {pred_prefixed}",
                    extra={"predicate": pred_prefixed}
                ))
