"""NamingValidator — Validação sintática de convenções de nomenclatura OWL (UC-108 - extensão)"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING
from datetime import datetime
import yaml

if TYPE_CHECKING:
    from rdflib import Graph

from rdflib import OWL, RDF, RDFS, SKOS, Namespace

# Namespace dcterms
DCTERMS = Namespace("http://purl.org/dc/terms/")


def _get_default_rules_path() -> str:
    """
    Retorna o caminho padrão para rules.json.
    
    A partir de src/onto_tools/domain/ontology/naming_validator.py,
    sobe até a raiz e vai para data/examples/rules.json
    """
    project_root = Path(__file__).parent.parent.parent.parent.parent
    return str(project_root / "data" / "examples" / "rules.json")


class NamingValidator:
    """UC-108 (extensão): Validar sintaxe de nomenclatura conforme convenções OWL"""
    
    def __init__(self, rules_path: str = None):
        """
        Args:
            rules_path: Caminho para rules.json (default: data/examples/rules.json)
        """
        self.rules_path = rules_path or _get_default_rules_path()
        self.rules = self._load_rules()
    
    def _load_rules(self) -> dict:
        """Carrega regras de naming_syntax do rules.json"""
        rules_file = Path(self.rules_path)
        
        if not rules_file.exists():
            print(f"Aviso: rules.json não encontrado em {self.rules_path}, usando regras padrão")
            return self._default_rules()
        
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            return rules_data.get("rules", {}).get("naming_syntax", {})
        except Exception as e:
            print(f"Erro ao carregar rules.json: {e}")
            return self._default_rules()
    
    def _default_rules(self) -> dict:
        """Regras padrão caso rules.json não exista"""
        return {
            "owl_classes": {
                "pattern": "PascalCase",
                "regex": "^[A-Z][a-zA-Z0-9]*$",
                "must_match_identifier": True
            },
            "owl_properties": {
                "pattern": "lowerCamelCase",
                "regex": "^[a-z][a-zA-Z0-9]*$"
            },
            "skos_preflabels": {
                "required_languages": ["en", "pt-br"],
                "language_tags_lowercase": True,
                "no_underscores": True,
                "no_trailing_periods": True
            },
            "dcterms_identifier": {
                "must_exist_for_classes": True,
                "must_match_local_name": True,
                "pattern": "PascalCase",
                "regex": "^[A-Z][a-zA-Z0-9]*$"
            }
        }
    
    def validate_naming_syntax(self, graph: Graph) -> tuple[bool, dict]:
        """
        Valida convenções sintáticas de nomenclatura.
        
        Args:
            graph: Grafo RDF a validar
        
        Returns:
            tuple[bool, dict]: (is_valid, validation_report)
                - is_valid: True se não há erros
                - validation_report: {"errors": [...], "warnings": [...], "suggestions": [...], "summary": {...}}
        """
        errors = []
        warnings = []
        suggestions = []
        
        # Validar classes OWL
        class_errors, class_warnings = self._validate_class_names(graph)
        errors.extend(class_errors)
        warnings.extend(class_warnings)
        
        # Validar propriedades OWL
        prop_errors, prop_warnings = self._validate_property_names(graph)
        errors.extend(prop_errors)
        warnings.extend(prop_warnings)
        
        # Validar skos:prefLabel
        label_errors, label_warnings, label_suggestions = self._validate_preflabels(graph)
        errors.extend(label_errors)
        warnings.extend(label_warnings)
        suggestions.extend(label_suggestions)
        
        # Validar dcterms:identifier
        id_errors = self._validate_identifiers(graph)
        errors.extend(id_errors)
        
        # Construir relatório
        report = self._build_validation_report(errors, warnings, suggestions, graph)
        
        is_valid = len(errors) == 0
        return is_valid, report
    
    def _validate_class_names(self, graph: Graph) -> tuple[list, list]:
        """Valida nomes de classes OWL"""
        errors = []
        warnings = []
        
        class_rules = self.rules.get("owl_classes", {})
        pattern = class_rules.get("regex", "^[A-Z][a-zA-Z0-9]*$")
        must_match_id = class_rules.get("must_match_identifier", True)
        
        for class_uri in graph.subjects(RDF.type, OWL.Class):
            # Extrair nome local
            local_name = self._get_local_name(str(class_uri))
            if not local_name:
                continue
            
            # Validar padrão PascalCase
            if not re.match(pattern, local_name):
                errors.append({
                    "subject": str(class_uri),
                    "issue": f"Class name '{local_name}' violates PascalCase pattern",
                    "expected": self._suggest_pascalcase(local_name),
                    "severity": "error",
                    "rule": "owl_classes.pattern"
                })
            
            # Validar dcterms:identifier match
            if must_match_id:
                identifier = graph.value(class_uri, DCTERMS.identifier)
                if identifier and str(identifier) != local_name:
                    errors.append({
                        "subject": str(class_uri),
                        "issue": f"dcterms:identifier '{identifier}' does not match class name '{local_name}'",
                        "expected": local_name,
                        "severity": "error",
                        "rule": "dcterms_identifier.must_match_local_name"
                    })
        
        return errors, warnings
    
    def _validate_property_names(self, graph: Graph) -> tuple[list, list]:
        """Valida nomes de propriedades OWL"""
        errors = []
        warnings = []
        
        prop_rules = self.rules.get("owl_properties", {})
        pattern = prop_rules.get("regex", "^[a-z][a-zA-Z0-9]*$")
        exclude_from_validation = set(prop_rules.get("exclude_from_validation", []))
        
        # Validar ObjectProperty, DatatypeProperty, AnnotationProperty
        property_types = [OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty]
        
        for prop_type in property_types:
            for prop_uri in graph.subjects(RDF.type, prop_type):
                local_name = self._get_local_name(str(prop_uri))
                if not local_name:
                    continue
                
                # Pular propriedades na lista de exclusão
                if local_name in exclude_from_validation:
                    continue
                
                # Validar padrão lowerCamelCase
                if not re.match(pattern, local_name):
                    errors.append({
                        "subject": str(prop_uri),
                        "issue": f"Property name '{local_name}' violates lowerCamelCase pattern",
                        "expected": self._suggest_camelcase(local_name),
                        "severity": "error",
                        "rule": "owl_properties.pattern"
                    })
        
        return errors, warnings
    
    def _load_prepositions(self, lang: str) -> set:
        """Carrega as preposições das regras de naming_syntax."""
        label_rules = self.rules.get("skos_preflabels", {})
        
        # Mapear idioma para configuração
        if lang.startswith("pt"):
            lang_config = label_rules.get("portuguese", {})
        else:
            lang_config = label_rules.get("english", {})
        
        # Retornar exceções (preposições, artigos, etc.)
        return set(lang_config.get("exceptions", []))

    def _correct_preflabel(self, label: str, lang: str = "pt-br") -> str:
        """
        Corrige o skos:prefLabel para atender às regras de capitalização por idioma.
        
        Regras:
        - Acrônimos registrados devem estar em UPPERCASE
        - Preposições/stopwords em minúsculo (exceto primeira palavra)
        - Outras palavras capitalizadas (primeira letra maiúscula)
        """
        prepositions = self._load_prepositions(lang)
        words = label.split()
        corrected_words = []

        for i, word in enumerate(words):
            # Verificar se é acrônimo registrado - deve ficar UPPERCASE
            if self._is_acronym(word):
                corrected_words.append(word.upper())
            elif word.lower() in prepositions and i != 0:
                corrected_words.append(word.lower())
            else:
                corrected_words.append(word.capitalize())

        return " ".join(corrected_words)

    def _validate_preflabels(self, graph: Graph) -> tuple[list, list, list]:
        """Valida skos:prefLabel e aplica correções."""
        errors = []
        warnings = []
        suggestions = []

        label_rules = self.rules.get("skos_preflabels", {})
        required_langs = label_rules.get("required_languages", ["en", "pt-br"])

        # Iterar sobre classes OWL
        for class_uri in graph.subjects(RDF.type, OWL.Class):
            local_name = self._get_local_name(str(class_uri))

            # Coletar todos prefLabels
            pref_labels = list(graph.objects(class_uri, SKOS.prefLabel))

            if not pref_labels:
                warnings.append({
                    "subject": str(class_uri),
                    "issue": f"Class '{local_name}' has no skos:prefLabel",
                    "expected": "At least one prefLabel in en and pt-br",
                    "severity": "warning",
                    "rule": "skos_preflabels.required_languages"
                })
                continue
            else:
                # Tem prefLabels - validar idiomas
                pass
            
            # Verificar idiomas obrigatórios
            found_langs = set()
            for label in pref_labels:
                if hasattr(label, 'language') and label.language:
                    lang = label.language
                    found_langs.add(lang)
                    
                    # Validar language tag lowercase
                    if label_rules.get("language_tags_lowercase", True) and lang != lang.lower():
                        errors.append({
                            "subject": str(class_uri),
                            "issue": f"Language tag '{lang}' should be lowercase",
                            "expected": lang.lower(),
                            "severity": "error",
                            "rule": "skos_preflabels.language_tags_lowercase"
                        })
                    
                    # Validar underscores
                    label_text = str(label)
                    if label_rules.get("no_underscores", True) and '_' in label_text:
                        warnings.append({
                            "subject": str(class_uri),
                            "issue": f"prefLabel '{label_text}'@{lang} contains underscores",
                            "expected": label_text.replace('_', ' '),
                            "severity": "warning",
                            "rule": "skos_preflabels.no_underscores"
                        })
                    
                    # Validar trailing period
                    if label_rules.get("no_trailing_periods", True) and label_text.endswith('.'):
                        warnings.append({
                            "subject": str(class_uri),
                            "issue": f"prefLabel '{label_text}'@{lang} has trailing period",
                            "expected": label_text.rstrip('.'),
                            "severity": "warning",
                            "rule": "skos_preflabels.no_trailing_periods"
                        })
                    
                    # Validar Title Case (se habilitado)
                    if label_rules.get("validate_title_case", False):
                        if lang == "en":
                            is_valid_case, expected_case = self._validate_title_case_en(label_text)
                            if not is_valid_case:
                                warnings.append({
                                    "subject": str(class_uri),
                                    "issue": f"prefLabel '{label_text}'@{lang} violates English Title Case (APA)",
                                    "expected": expected_case,
                                    "severity": "warning",
                                    "rule": "skos_preflabels.english.pattern"
                                })
                            else:
                                # Label EN válido - sem ação necessária
                                pass
                        elif lang == "pt-br":
                            is_valid_case, expected_case = self._validate_title_case_pt(label_text)
                            if not is_valid_case:
                                warnings.append({
                                    "subject": str(class_uri),
                                    "issue": f"prefLabel '{label_text}'@{lang} violates Portuguese Title Case",
                                    "expected": expected_case,
                                    "severity": "warning",
                                    "rule": "skos_preflabels.portuguese.pattern"
                                })
                            else:
                                # Label PT válido - sem ação necessária
                                pass
                        else:
                            # Idioma não suportado para Title Case validation
                            pass
            
            # Verificar idiomas faltantes
            missing_langs = set(required_langs) - found_langs
            if missing_langs:
                errors.append({
                    "subject": str(class_uri),
                    "issue": f"Class '{local_name}' missing prefLabel for languages: {', '.join(missing_langs)}",
                    "expected": f"Add prefLabel for: {', '.join(missing_langs)}",
                    "severity": "error",
                    "rule": "skos_preflabels.required_languages"
                })
        
        return errors, warnings, suggestions
    
    def _validate_identifiers(self, graph: Graph) -> list:
        """Valida dcterms:identifier - deve seguir Title Case (PascalCase) como classes OWL"""
        errors = []
        
        id_rules = self.rules.get("dcterms_identifier", {})
        must_exist = id_rules.get("must_exist_for_classes", True)
        must_match = id_rules.get("must_match_local_name", True)
        
        # Obter regex de classes (Title Case / PascalCase) do rules.json
        # Se dcterms_identifier tiver seu próprio regex, usar esse; senão, usar o de owl_classes
        identifier_regex = id_rules.get("regex") or self.rules.get("owl_classes", {}).get("regex", r"^[A-Z][a-zA-Z0-9]*$")
        
        for class_uri in graph.subjects(RDF.type, OWL.Class):
            local_name = self._get_local_name(str(class_uri))
            if not local_name:
                continue
            
            identifier = graph.value(class_uri, DCTERMS.identifier)
            
            # Validar existência
            if must_exist and not identifier:
                errors.append({
                    "subject": str(class_uri),
                    "issue": f"Class '{local_name}' missing dcterms:identifier",
                    "expected": f'Add: dcterms:identifier "{local_name}"',
                    "severity": "error",
                    "rule": "dcterms_identifier.must_exist_for_classes"
                })
            
            # Validar match com nome local
            if must_match and identifier and str(identifier) != local_name:
                errors.append({
                    "subject": str(class_uri),
                    "issue": f"dcterms:identifier '{identifier}' does not match class name '{local_name}'",
                    "expected": local_name,
                    "severity": "error",
                    "rule": "dcterms_identifier.must_match_local_name"
                })
            
            # NOVA VALIDAÇÃO: Verificar se identifier segue Title Case (igual a classes OWL)
            if identifier:
                identifier_str = str(identifier)
                if not re.match(identifier_regex, identifier_str):
                    # Sugerir correção em Title Case
                    suggested = self._suggest_pascalcase(identifier_str)
                    # Só reportar se a sugestão for diferente do valor atual
                    if suggested != identifier_str:
                        errors.append({
                            "subject": str(class_uri),
                            "issue": f"dcterms:identifier '{identifier_str}' violates Title Case pattern (must be PascalCase like OWL classes)",
                            "expected": suggested,
                            "severity": "error",
                            "rule": "dcterms_identifier.pattern"
                        })
        
        return errors
    
    def _get_local_name(self, uri: str) -> str | None:
        """Extrai nome local de uma URI"""
        if '#' in uri:
            return uri.split('#')[-1]
        elif '/' in uri:
            return uri.split('/')[-1]
        return None
    
    def _suggest_pascalcase(self, name: str) -> str:
        """Sugere PascalCase para um nome"""
        # Se tem underscores ou hífens, tratar como separadores de palavras
        if '_' in name or '-' in name:
            # Primeiro, separar por underscore/hífens
            parts = name.replace('-', '_').split('_')
            result_parts = []
            
            for part in parts:
                # Para cada parte, se já está em PascalCase/camelCase, manter estrutura
                if part and not ' ' in part:
                    # Detectar transições maiúscula/minúscula
                    words = []
                    current_word = []
                    for i, char in enumerate(part):
                        if char.isupper() and i > 0 and part[i-1].islower():
                            if current_word:
                                words.append(''.join(current_word))
                            current_word = [char]
                        else:
                            current_word.append(char)
                    if current_word:
                        words.append(''.join(current_word))
                    
                    # Capitalizar cada palavra detectada
                    if words:
                        result_parts.extend([w.capitalize() for w in words])
                    else:
                        result_parts.append(part.capitalize())
                else:
                    result_parts.append(part.capitalize())
            
            return ''.join(result_parts)
        
        # Se já está em camelCase ou PascalCase, capitalizar primeira letra
        if name and not ' ' in name:
            # Detectar transições de minúscula para maiúscula (camelCase)
            words = []
            current_word = []
            for i, char in enumerate(name):
                if char.isupper() and i > 0 and name[i-1].islower():
                    # Transição de minúscula para maiúscula - nova palavra
                    if current_word:
                        words.append(''.join(current_word))
                    current_word = [char]
                else:
                    current_word.append(char)
            if current_word:
                words.append(''.join(current_word))
            
            # Capitalizar cada palavra
            return ''.join(word.capitalize() for word in words)
        
        # Remove underscores, hífens e espaços
        cleaned = name.replace('_', ' ').replace('-', ' ')
        # Capitaliza cada palavra
        words = cleaned.split()
        return ''.join(word.capitalize() for word in words)
    
    def _suggest_camelcase(self, name: str) -> str:
        """Sugere lowerCamelCase para um nome"""
        pascal = self._suggest_pascalcase(name)
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return name
    
    def _is_acronym(self, word: str) -> bool:
        """
        Detecta se palavra é acrônimo registrado ou padrão (3+ letras UPPERCASE).
        
        Verifica:
        1. Se word.upper() está na lista de acrônimos registrados no rules.json
        2. OU se é uma palavra de 3+ letras todas em maiúsculas (fallback)
        
        Args:
            word: Palavra a verificar
        
        Returns:
            True se for acrônimo registrado ou padrão
        
        Examples:
            >>> validator._is_acronym("PLET")  # Registrado
            True
            >>> validator._is_acronym("Plet")  # Registrado (case-insensitive)
            True
            >>> validator._is_acronym("HCR")   # Registrado
            True
            >>> validator._is_acronym("Hcr")   # Registrado (case-insensitive)
            True
            >>> validator._is_acronym("NATO")  # Não registrado, mas 3+ UPPERCASE
            True
            >>> validator._is_acronym("Bomba")
            False
        """
        # Carregar lista de acrônimos registrados
        acronyms_config = self.rules.get("acronyms", {})
        registered_acronyms = set(a.upper() for a in acronyms_config.get("list", []))
        
        # Verificar se está na lista de acrônimos registrados (case-insensitive)
        if word.upper() in registered_acronyms:
            return True
        
        # Fallback: 3+ letras todas maiúsculas
        return len(word) >= 3 and word.isupper() and word.isalpha()
    
    def _is_first_word(self, index: int) -> bool:
        """
        Verifica se é a primeira palavra do título.
        
        Args:
            index: Índice da palavra na lista
        
        Returns:
            True se index == 0
        """
        return index == 0
    
    def _handle_apostrophe_pt(self, word: str) -> str:
        """
        Trata apóstrofos em português: d'água → d'Água.
        
        Args:
            word: Palavra potencialmente contendo apóstrofo
        
        Returns:
            Palavra corretamente capitalizada
        
        Examples:
            >>> validator._handle_apostrophe_pt("d'água")
            "d'Água"
            >>> validator._handle_apostrophe_pt("l'état")
            "l'État"
        """
        apostrophe_prefixes = self.rules.get("skos_preflabels", {}).get(
            "portuguese", {}
        ).get("apostrophe_rules", {}).get("preserve_lowercase_prefix", ["d'", "l'"])
        
        for prefix in apostrophe_prefixes:
            if word.lower().startswith(prefix):
                # d'água → d' + Água
                return prefix + word[len(prefix):].capitalize()
        
        return word
    
    def _handle_hyphen_en(self, word: str) -> str:
        """
        Trata hífens em inglês: pull-in → Pull-In, 0-ring → O-Ring.
        
        Args:
            word: Palavra com hífen
        
        Returns:
            Composto corretamente capitalizado
        
        Examples:
            >>> validator._handle_hyphen_en("pull-in")
            "Pull-In"
            >>> validator._handle_hyphen_en("0-ring")
            "O-Ring"
            >>> validator._handle_hyphen_en("coaxial-cable")
            "Coaxial-Cable"
        """
        corrections = self.rules.get("skos_preflabels", {}).get(
            "english", {}
        ).get("technical_corrections", {})
        
        # Verificar correções exatas
        if word.lower() in corrections:
            return corrections[word.lower()]
        
        # Padrão: capitalizar ambas partes
        parts = word.split('-')
        return '-'.join(part.capitalize() for part in parts)
    
    def _handle_hyphen_pt(self, word: str, is_second_exception: bool) -> str:
        """
        Trata hífens em português: Bomba-Relógio (ambos caps) vs Parte-de (segundo é exceção).
        
        Args:
            word: Palavra com hífen
            is_second_exception: Se segunda parte está na lista de exceções
        
        Returns:
            Composto corretamente capitalizado
        
        Examples:
            >>> validator._handle_hyphen_pt("bomba-relógio", False)
            "Bomba-Relógio"
            >>> validator._handle_hyphen_pt("parte-de", True)
            "Parte-de"
        """
        parts = word.split('-')
        if len(parts) == 2:
            first = parts[0].capitalize()
            second = parts[1].lower() if is_second_exception else parts[1].capitalize()
            return f"{first}-{second}"
        
        # Múltiplos hífens: capitalizar todos
        return '-'.join(part.capitalize() for part in parts)
    
    def _validate_title_case_en(self, text: str) -> tuple[bool, str]:
        """
        Valida Title Case inglês (APA Style).
        
        Regras:
        - Primeira palavra sempre capitalizada
        - Palavras ≥4 letras sempre capitalizadas
        - Stopwords (≤3 letras) em minúsculo quando não primeira palavra
        - Acrônimos registrados devem estar em UPPERCASE
        - Hífens técnicos: ambas partes capitalizadas
        - 'Y' e 'T' entre aspas devem ser maiúsculos
        
        Args:
            text: Texto prefLabel a validar
        
        Returns:
            tuple[bool, str]: (is_valid, expected_format)
        
        Examples:
            >>> validator._validate_title_case_en("Bending Moment vs Shear Force")
            (True, "Bending Moment vs Shear Force")
            >>> validator._validate_title_case_en("bending moment VS shear force")
            (False, "Bending Moment vs Shear Force")
            >>> validator._validate_title_case_en("Plet")
            (False, "PLET")
            >>> validator._validate_title_case_en("Hcr Hose")
            (False, "HCR Hose")
        """
        en_rules = self.rules.get("skos_preflabels", {}).get("english", {})
        # Usar stopwords centralizadas, fallback para exceptions legadas
        stopwords = self.rules.get("stopwords", {}).get("en", []) or en_rules.get("exceptions", [])
        min_length = en_rules.get("min_capitalize_length", 4)
        
        words = text.split()
        expected_words = []
        
        for i, word in enumerate(words):
            # Verificar se é acrônimo registrado - deve estar em UPPERCASE
            if self._is_acronym(word):
                expected_words.append(word.upper())
                continue
            
            # Tratar hífens
            if '-' in word:
                expected = self._handle_hyphen_en(word)
                expected_words.append(expected)
                continue
            
            # Primeira palavra sempre capitalizada
            if self._is_first_word(i):
                expected_words.append(word.capitalize())
                continue
            
            # Palavras ≥4 letras capitalizadas
            if len(word) >= min_length:
                expected_words.append(word.capitalize())
                continue
            else:
                # Palavra curta (<4 letras) - verificar stopwords
                pass
            
            # Stopwords em minúsculo
            if word.lower() in stopwords:
                expected_words.append(word.lower())
            else:
                # Palavras curtas não-exceções ainda capitalizadas
                # (palavras < min_length que não estão na lista de exceções)
                expected_words.append(word.capitalize())
        
        expected = ' '.join(expected_words)
        return text == expected, expected
    
    def _validate_title_case_pt(self, text: str) -> tuple[bool, str]:
        """
        Valida Title Case português (baseado em gramática).
        
        Regras:
        - Primeira palavra sempre capitalizada
        - Stopwords (artigos/preposições) em minúsculo quando não primeira palavra
        - Palavras de conteúdo capitalizadas
        - Acrônimos registrados devem estar em UPPERCASE
        - Apóstrofos: d'Água (preposição lowercase + substantivo caps)
        - Hífens: ambos capitalizados exceto se segundo é stopword
        - 'Y' e 'T' entre aspas devem ser maiúsculos
        
        Args:
            text: Texto prefLabel a validar
        
        Returns:
            tuple[bool, str]: (is_valid, expected_format)
        
        Examples:
            >>> validator._validate_title_case_pt("Conjunto de Colares de Anodo")
            (True, "Conjunto de Colares de Anodo")
            >>> validator._validate_title_case_pt("d'água")
            (False, "d'Água")
            >>> validator._validate_title_case_pt("Plem")
            (False, "PLEM")
        """
        pt_rules = self.rules.get("skos_preflabels", {}).get("portuguese", {})
        # Usar stopwords centralizadas, fallback para exceptions legadas
        stopwords = self.rules.get("stopwords", {}).get("pt_br", []) or pt_rules.get("exceptions", [])
        
        words = text.split()
        expected_words = []
        
        for i, word in enumerate(words):
            # Verificar se é acrônimo registrado - deve estar em UPPERCASE
            if self._is_acronym(word):
                expected_words.append(word.upper())
                continue
            
            # Tratar apóstrofos (d'água → d'Água)
            if "'" in word:
                expected = self._handle_apostrophe_pt(word)
                expected_words.append(expected)
                continue
            
            # Tratar hífens
            if '-' in word:
                # Verificar se segunda parte é stopword
                parts = word.split('-')
                is_second_stopword = len(parts) == 2 and parts[1].lower() in stopwords
                expected = self._handle_hyphen_pt(word, is_second_stopword)
                expected_words.append(expected)
                continue
            
            # Primeira palavra sempre capitalizada
            if self._is_first_word(i):
                expected_words.append(word.capitalize())
                continue
            else:
                # Não é primeira palavra - aplicar outras regras
                pass
            
            # Stopwords em minúsculo
            if word.lower() in stopwords:
                expected_words.append(word.lower())
            else:
                # Palavras de conteúdo capitalizadas
                expected_words.append(word.capitalize())
        
        expected = ' '.join(expected_words)
        return text == expected, expected
    
    def _build_validation_report(self, errors: list, warnings: list, suggestions: list, graph: Graph) -> dict:
        """Constrói relatório de validação padronizado"""
        return {
            "validation_type": "naming_syntax",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_errors": len(errors),
                "total_warnings": len(warnings),
                "total_suggestions": len(suggestions),
                "is_valid": len(errors) == 0,
                "total_classes_checked": len(list(graph.subjects(RDF.type, OWL.Class))),
                "total_properties_checked": len(list(graph.subjects(RDF.type, OWL.ObjectProperty))) + 
                                           len(list(graph.subjects(RDF.type, OWL.DatatypeProperty))) +
                                           len(list(graph.subjects(RDF.type, OWL.AnnotationProperty)))
            },
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "rules_file": self.rules_path
        }
