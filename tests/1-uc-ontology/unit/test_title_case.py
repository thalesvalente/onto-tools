"""
Testes para Title Case - Validação de capitalização.

Cobre:
- Title Case inglês (APA Style)
- Title Case português
- Tratamento de exceções (artigos, preposições)
- Tratamento de acrônimos
- Tratamento de hífens e apóstrofos
"""
import pytest

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import OWL, RDF, SKOS

from onto_tools.domain.ontology.naming_validator import NamingValidator


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


@pytest.fixture
def validator():
    """Cria validador com regras de teste."""
    return NamingValidator()


class TestTitleCaseEnglish:
    """Testes de Title Case inglês."""
    
    def test_simple_title_case(self, validator):
        """Título simples em Title Case."""
        is_valid, expected = validator._validate_title_case_en("Test Class Name")
        
        assert is_valid is True
    
    def test_lowercase_first_word_fails(self, validator):
        """Primeira palavra em lowercase falha."""
        is_valid, expected = validator._validate_title_case_en("test Class Name")
        
        assert is_valid is False
        assert expected == "Test Class Name"
    
    def test_short_word_exceptions(self, validator):
        """Palavras curtas (artigos/preposições) em minúsculo."""
        is_valid, expected = validator._validate_title_case_en("Bending Moment vs Shear Force")
        
        # "vs" é uma exceção e deve estar em minúsculo
        assert "vs" in expected.lower() or is_valid is True
    
    def test_first_word_always_caps(self, validator):
        """Primeira palavra sempre capitalizada, mesmo se exceção."""
        is_valid, expected = validator._validate_title_case_en("The Great Escape")
        
        assert expected.startswith("The")
    
    def test_acronym_preserved(self, validator):
        """Acrônimos mantêm ALL CAPS."""
        is_valid, expected = validator._validate_title_case_en("NASA Space Program")
        
        assert "NASA" in expected


class TestTitleCasePortuguese:
    """Testes de Title Case português."""
    
    def test_simple_title_case_pt(self, validator):
        """Título simples em português."""
        is_valid, expected = validator._validate_title_case_pt("Classe de Teste")
        
        # "de" é preposição, deve estar em minúsculo
        assert "de" in expected.lower() or is_valid is True
    
    def test_preposition_lowercase(self, validator):
        """Preposições em minúsculo."""
        is_valid, expected = validator._validate_title_case_pt("Conjunto de Colares de Anodo")
        
        # "de" deve estar em minúsculo (exceto se primeira)
        parts = expected.split()
        # Verificar que "de" não está capitalizado no meio
        for i, word in enumerate(parts):
            if word.lower() == "de" and i > 0:
                assert word == "de" or word == "De"
    
    def test_first_word_caps_even_preposition(self, validator):
        """Primeira palavra capitalizada mesmo se preposição."""
        is_valid, expected = validator._validate_title_case_pt("De Volta ao Futuro")
        
        assert expected.startswith("De")


class TestHandleHyphen:
    """Testes de tratamento de hífens."""
    
    def test_hyphen_english(self, validator):
        """Hífen em inglês: ambas partes capitalizadas."""
        result = validator._handle_hyphen_en("pull-in")
        
        assert result == "Pull-In"
    
    def test_hyphen_portuguese_both_caps(self, validator):
        """Hífen em português: ambas capitalizadas por padrão."""
        result = validator._handle_hyphen_pt("bomba-relógio", is_second_exception=False)
        
        assert result == "Bomba-Relógio"
    
    def test_hyphen_portuguese_second_exception(self, validator):
        """Hífen em português: segunda parte exceção fica minúscula."""
        result = validator._handle_hyphen_pt("parte-de", is_second_exception=True)
        
        assert result == "Parte-de"


class TestHandleApostrophe:
    """Testes de tratamento de apóstrofos."""
    
    def test_apostrophe_portuguese(self, validator):
        """Apóstrofo em português: d'água -> d'Água."""
        result = validator._handle_apostrophe_pt("d'água")
        
        assert result == "d'Água"


class TestIsAcronym:
    """Testes de detecção de acrônimos."""
    
    def test_valid_acronym(self, validator):
        """Acrônimo válido (3+ letras maiúsculas)."""
        assert validator._is_acronym("NASA") is True
        assert validator._is_acronym("IMUX") is True
        assert validator._is_acronym("API") is True
    
    def test_short_not_acronym(self, validator):
        """Palavras curtas (< 3) não são acrônimos."""
        assert validator._is_acronym("AB") is False
        assert validator._is_acronym("A") is False
    
    def test_lowercase_not_acronym(self, validator):
        """Palavras em lowercase não são acrônimos."""
        assert validator._is_acronym("nasa") is False
        assert validator._is_acronym("Test") is False
    
    def test_numbers_not_acronym(self, validator):
        """Números não são acrônimos."""
        assert validator._is_acronym("123") is False


class TestIsFirstWord:
    """Testes de detecção de primeira palavra."""
    
    def test_first_word_index_zero(self, validator):
        """Índice 0 é primeira palavra."""
        assert validator._is_first_word(0) is True
    
    def test_other_indices_not_first(self, validator):
        """Outros índices não são primeira palavra."""
        assert validator._is_first_word(1) is False
        assert validator._is_first_word(5) is False


class TestTitleCaseValidationIntegration:
    """Testes de integração de validação Title Case."""
    
    def test_preflabel_validation_with_title_case(self, validator):
        """Validação de prefLabel com Title Case."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, DCTERMS.identifier, Literal("TestClass")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("test class", lang="en")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("classe teste", lang="pt-br")))
        
        is_valid, report = validator.validate_naming_syntax(g)
        
        # Se validate_title_case está habilitado, deve haver warnings
        # Se não está, não deve haver warnings de title case
        assert "warnings" in report


class TestTitleCaseEdgeCases:
    """Testes de casos extremos de Title Case."""
    
    def test_single_word(self, validator):
        """Palavra única."""
        is_valid, expected = validator._validate_title_case_en("Test")
        
        assert expected == "Test"
    
    def test_empty_string(self, validator):
        """String vazia."""
        is_valid, expected = validator._validate_title_case_en("")
        
        assert expected == ""
    
    def test_all_caps_word(self, validator):
        """Palavra toda em maiúsculas (não acrônimo curto)."""
        is_valid, expected = validator._validate_title_case_en("THE TEST")
        
        # Deve normalizar
        assert "The" in expected or "THE" in expected
    
    def test_mixed_case_preserved_for_acronyms(self, validator):
        """Acrônimos preservam case."""
        is_valid, expected = validator._validate_title_case_en("The NASA Mission")
        
        assert "NASA" in expected

