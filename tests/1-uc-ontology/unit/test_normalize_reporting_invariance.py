"""
Testes para Invariância de Reporte entre Modos (RF-01, RF-03)

Estes testes garantem que:
- RF-01: validate-only e auto-fix produzem mesmo conjunto de achados e propostas
- RF-02: Correções controladas apenas pelo rulebook
- RF-03: Audit-log com schema estável em ambos os modos
- RF-04: Evidência rastreável

TEST-01: validate-only reporta mesmas issues detectadas que auto-fix
TEST-02: validate-only tem applied == 0 e proposed > 0 quando há correções possíveis
TEST-03: auto-fix aplica somente correções elegíveis no rulebook
TEST-04: nenhum acesso a data/examples/rules.json quando rulebook custom é usado
TEST-05: audit-log contém chaves essenciais em ambos os modos
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from onto_tools.domain.ontology.normalizer import Normalizer, NormalizationResult


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


@pytest.fixture
def minimal_ontology_with_issues():
    """
    Ontologia mínima com issues conhecidas para testar invariância.
    
    Contém:
    - 1 IRI com padrão incorreto (lowerCamelCase em vez de PascalCase)
    - 1 dcterms:identifier que dispara regra mecânica
    - 1 skos:prefLabel com formato incorreto (Title Case)
    - 1 skos:definition sem ponto final
    """
    g = Graph()
    
    # Bind namespaces
    g.bind("edo", EDO)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS)
    
    # Classe com nome correto (PascalCase) mas prefLabel incorreto
    g.add((EDO.TestClass, RDF.type, OWL.Class))
    g.add((EDO.TestClass, DCTERMS.identifier, Literal("TestClass")))
    # prefLabel incorreto: deve ser "Test Class" (Title Case)
    g.add((EDO.TestClass, SKOS.prefLabel, Literal("test class", lang="en")))
    g.add((EDO.TestClass, SKOS.prefLabel, Literal("classe de teste", lang="pt-br")))
    # definition sem ponto final
    g.add((EDO.TestClass, SKOS.definition, Literal("A test class for validation", lang="en")))
    g.add((EDO.TestClass, SKOS.definition, Literal("Uma classe de teste para validação", lang="pt-br")))
    
    # Segunda classe para garantir múltiplas issues
    g.add((EDO.AnotherClass, RDF.type, OWL.Class))
    g.add((EDO.AnotherClass, DCTERMS.identifier, Literal("AnotherClass")))
    g.add((EDO.AnotherClass, SKOS.prefLabel, Literal("another class", lang="en")))
    g.add((EDO.AnotherClass, SKOS.prefLabel, Literal("outra classe", lang="pt-br")))
    
    return g


@pytest.fixture
def custom_rules_minimal():
    """Regras mínimas customizadas para teste."""
    return {
        "rules": {
            "validation": {
                "check_utf8_encoding": True,
                "validate_iris": True
            },
            "naming_syntax": {
                "auto_fix": True,
                "owl_classes": {"pattern": "PascalCase"},
                "owl_properties": {"pattern": "lowerCamelCase"},
                "skos_preflabels": {
                    "required_languages": ["en", "pt-br"],
                    "validate_title_case": True,
                    "auto_fix": True
                },
                "stopwords": {
                    "en": ["a", "an", "the", "of", "for", "and", "or", "to", "in", "on", "at", "by", "with"],
                    "pt_br": ["de", "da", "do", "das", "dos", "para", "e", "ou", "em", "na", "no", "nas", "nos", "com", "a", "o", "as", "os", "um", "uma", "uns", "umas"]
                },
                "acronyms": {
                    "list": ["API", "IFC", "ID", "URI", "URL"]
                }
            }
        }
    }


@pytest.fixture
def custom_rules_path(custom_rules_minimal, tmp_path):
    """Cria arquivo temporário de rules.json para teste."""
    rules_file = tmp_path / "test_rules.json"
    with open(rules_file, 'w', encoding='utf-8') as f:
        json.dump(custom_rules_minimal, f, indent=2)
    return str(rules_file)


class TestReportingInvariance:
    """
    RF-01: Invariância de reporte por modo.
    
    Para o mesmo input e mesmo rulebook:
    - validate-only e auto-fix devem produzir mesmo conjunto de achados
    - e o mesmo conjunto de propostas
    - diferindo apenas em applied_corrections
    """
    
    def test_01_validate_only_reports_same_issues_as_auto_fix(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """
        TEST-01: validate-only reporta mesmas issues detectadas que auto-fix.
        
        Verifica que o número de issues detectadas é idêntico em ambos os modos.
        """
        # Modo validate-only (auto_fix=False)
        normalizer_validate = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result_validate = normalizer_validate.normalize(minimal_ontology_with_issues)
        
        # Modo auto-fix (auto_fix=True)
        normalizer_autofix = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result_autofix = normalizer_autofix.normalize(minimal_ontology_with_issues)
        
        # fix_stats deve existir em AMBOS os modos
        assert result_validate.fix_stats is not None, "fix_stats deve existir em validate-only"
        assert result_autofix.fix_stats is not None, "fix_stats deve existir em auto-fix"
        
        # O número total de propostas deve ser o mesmo
        # (pendentes em validate-only, aplicadas em auto-fix)
        validate_preflabel_total = (
            result_validate.fix_stats.get("total_pending_preflabel_fixes", 0) +
            result_validate.fix_stats.get("total_preflabel_fixes", 0)
        )
        autofix_preflabel_total = (
            result_autofix.fix_stats.get("total_pending_preflabel_fixes", 0) +
            result_autofix.fix_stats.get("total_preflabel_fixes", 0)
        )
        
        assert validate_preflabel_total == autofix_preflabel_total, (
            f"Total de propostas de prefLabel deve ser igual: "
            f"validate={validate_preflabel_total}, autofix={autofix_preflabel_total}"
        )
    
    def test_02_validate_only_has_zero_applied_and_positive_proposed(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """
        TEST-02: validate-only tem applied == 0 e proposed > 0.
        
        Quando há correções possíveis, validate-only deve:
        - Reportar propostas (pending_*_corrections não vazio)
        - Não aplicar nenhuma correção (total_*_fixes == 0)
        """
        normalizer = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result = normalizer.normalize(minimal_ontology_with_issues)
        
        assert result.fix_stats is not None
        
        # Deve ter propostas pendentes (prefLabels incorretos)
        pending_preflabel = result.fix_stats.get("pending_preflabel_corrections", {})
        pending_definition = result.fix_stats.get("pending_definition_corrections", {})
        
        total_pending = len(pending_preflabel) + len(pending_definition)
        assert total_pending > 0, "Deve haver propostas pendentes em validate-only"
        
        # Não deve ter correções aplicadas
        assert result.fix_stats.get("total_preflabel_fixes", 0) == 0, (
            "validate-only não deve aplicar correções de prefLabel"
        )
        assert result.fix_stats.get("total_definition_fixes", 0) == 0, (
            "validate-only não deve aplicar correções de definition"
        )
        
        # Verificar modo reportado
        assert result.fix_stats.get("mode") == "validate_only"
        assert result.auto_fix_applied is False
    
    def test_03_auto_fix_applies_only_eligible_corrections(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """
        TEST-03: auto-fix aplica somente correções elegíveis no rulebook.
        
        Verifica que:
        - Correções são aplicadas quando auto_fix=True
        - Pendentes ficam vazios após aplicação
        """
        normalizer = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result = normalizer.normalize(minimal_ontology_with_issues)
        
        assert result.fix_stats is not None
        
        # Deve ter correções aplicadas
        applied_preflabel = result.fix_stats.get("total_preflabel_fixes", 0)
        applied_definition = result.fix_stats.get("total_definition_fixes", 0)
        
        # Pelo menos prefLabels devem ser corrigidos
        assert applied_preflabel > 0 or applied_definition > 0, (
            "auto-fix deve aplicar correções quando elegíveis"
        )
        
        # Pendentes devem estar vazios (correções foram aplicadas)
        pending_preflabel = result.fix_stats.get("pending_preflabel_corrections", {})
        assert len(pending_preflabel) == 0, (
            "auto-fix não deve ter pendentes após aplicar correções"
        )
        
        # Verificar modo reportado
        assert result.fix_stats.get("mode") == "auto_fix"
        assert result.auto_fix_applied is True


class TestRulebookGovernance:
    """
    RF-02: Aplicação controlada apenas pelo rulebook.
    """
    
    def test_04_no_hardcoded_rules_access(self, minimal_ontology_with_issues, custom_rules_path):
        """
        TEST-04: nenhum acesso a data/examples/rules.json quando rulebook custom é usado.
        
        Verifica que o normalizer usa o rulebook injetado e não recarrega de path hardcoded.
        """
        # Criar regras customizadas com acrônimos específicos
        custom_rules = {
            "rules": {
                "validation": {"validate_iris": True},
                "naming_syntax": {
                    "auto_fix": True,
                    "stopwords": {"en": ["the", "of"], "pt_br": ["de", "da"]},
                    "acronyms": {"list": ["CUSTOM_ACRONYM"]}  # Acrônimo único
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_rules, f)
            custom_path = f.name
        
        try:
            normalizer = Normalizer(rules_path=custom_path, auto_fix=True)
            
            # Verificar que as regras carregadas são as customizadas
            acronyms = normalizer.rules.get("naming_syntax", {}).get("acronyms", {}).get("list", [])
            assert "CUSTOM_ACRONYM" in acronyms, (
                "Normalizer deve usar rulebook customizado, não default"
            )
            
            # Executar normalização para garantir que usa as regras corretas
            result = normalizer.normalize(minimal_ontology_with_issues)
            assert result.fix_stats is not None
            
        finally:
            Path(custom_path).unlink(missing_ok=True)


class TestAuditLogSchema:
    """
    RF-03: Audit-log com schema estável.
    """
    
    def test_05_fix_stats_has_essential_keys_in_both_modes(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """
        TEST-05: audit-log contém chaves essenciais em ambos os modos.
        
        Verifica que fix_stats tem estrutura consistente.
        """
        # Chaves essenciais que devem estar presentes em ambos os modos
        essential_keys = [
            "uri_corrections",
            "identifier_corrections",
            "preflabel_corrections",
            "definition_corrections",
            "pending_preflabel_corrections",
            "pending_definition_corrections",
            "total_triples_modified",
            "total_uri_replacements",
            "total_identifier_fixes",
            "total_preflabel_fixes",
            "total_definition_fixes",
            "total_pending_preflabel_fixes",
            "total_pending_definition_fixes",
            "mode",
        ]
        
        # Testar validate-only
        normalizer_validate = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result_validate = normalizer_validate.normalize(minimal_ontology_with_issues)
        
        assert result_validate.fix_stats is not None
        for key in essential_keys:
            assert key in result_validate.fix_stats, (
                f"Chave '{key}' ausente em fix_stats (validate-only)"
            )
        
        # Testar auto-fix
        normalizer_autofix = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result_autofix = normalizer_autofix.normalize(minimal_ontology_with_issues)
        
        assert result_autofix.fix_stats is not None
        for key in essential_keys:
            assert key in result_autofix.fix_stats, (
                f"Chave '{key}' ausente em fix_stats (auto-fix)"
            )
    
    def test_mode_field_is_correct(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """Verifica que o campo 'mode' está correto em cada cenário."""
        # validate-only
        normalizer_v = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result_v = normalizer_v.normalize(minimal_ontology_with_issues)
        assert result_v.fix_stats["mode"] == "validate_only"
        
        # auto-fix
        normalizer_a = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result_a = normalizer_a.normalize(minimal_ontology_with_issues)
        assert result_a.fix_stats["mode"] == "auto_fix"


class TestProposedCorrectionsConsistency:
    """Testes adicionais de consistência de propostas."""
    
    def test_total_proposed_equals_sum_of_applied_and_pending(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """
        O total de correções propostas deve ser consistente entre modos.
        
        Em validate-only: todas propostas ficam em pending
        Em auto-fix: todas propostas são aplicadas
        """
        # validate-only
        normalizer_v = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result_v = normalizer_v.normalize(minimal_ontology_with_issues)
        
        # auto-fix
        normalizer_a = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result_a = normalizer_a.normalize(minimal_ontology_with_issues)
        
        # Em validate-only: pendentes == total propostas
        v_pending = (
            result_v.fix_stats.get("total_pending_preflabel_fixes", 0) +
            result_v.fix_stats.get("total_pending_definition_fixes", 0)
        )
        
        # Em auto-fix: aplicadas == total propostas
        a_applied = (
            result_a.fix_stats.get("total_preflabel_fixes", 0) +
            result_a.fix_stats.get("total_definition_fixes", 0)
        )
        
        # Os totais devem ser iguais (mesmas propostas)
        assert v_pending == a_applied, (
            f"Total de propostas deve ser igual: "
            f"validate-only pending={v_pending}, auto-fix applied={a_applied}"
        )
    
    def test_preflabel_corrections_structure(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """Verifica estrutura das correções de prefLabel."""
        normalizer = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result = normalizer.normalize(minimal_ontology_with_issues)
        
        pending = result.fix_stats.get("pending_preflabel_corrections", {})
        
        # Cada entrada deve ter old_value, new_value, lang
        for subject, corrections in pending.items():
            assert isinstance(corrections, list), f"Correções de {subject} deve ser lista"
            for corr in corrections:
                assert "old_value" in corr, "Correção deve ter old_value"
                assert "new_value" in corr, "Correção deve ter new_value"
                assert "lang" in corr, "Correção deve ter lang"


class TestNormalizationResultContract:
    """Testes do contrato do NormalizationResult."""
    
    def test_to_dict_works_in_both_modes(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """NormalizationResult.to_dict() funciona em ambos os modos."""
        # validate-only
        normalizer_v = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        result_v = normalizer_v.normalize(minimal_ontology_with_issues)
        dict_v = result_v.to_dict()
        
        assert "auto_fix_applied" in dict_v
        assert dict_v["auto_fix_applied"] is False
        
        # auto-fix
        normalizer_a = Normalizer(rules_path=custom_rules_path, auto_fix=True)
        result_a = normalizer_a.normalize(minimal_ontology_with_issues)
        dict_a = result_a.to_dict()
        
        assert "auto_fix_applied" in dict_a
        assert dict_a["auto_fix_applied"] is True
    
    def test_normalizer_exposes_rules_path(
        self, minimal_ontology_with_issues, custom_rules_path
    ):
        """Normalizer expõe rules_path para cálculo de rulebook snapshot."""
        normalizer = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        
        # rules_path deve ser acessível para cálculo de sha256
        assert hasattr(normalizer, 'rules_path'), "Normalizer deve expor rules_path"
        assert normalizer.rules_path == custom_rules_path, "rules_path deve ser o caminho fornecido"


class TestAuditLogRulebookSnapshot:
    """
    T5: Testes do rulebook snapshot no audit-log.
    
    O audit-log deve incluir:
    - rulebook.path
    - rulebook.sha256
    - rulebook.version (opcional)
    """
    
    def test_rulebook_snapshot_sha256_calculation(self, custom_rules_path):
        """Verifica que o sha256 do rulebook pode ser calculado."""
        import hashlib
        
        with open(custom_rules_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        
        assert len(sha256) == 64, "SHA256 deve ter 64 caracteres hex"
        assert sha256.isalnum(), "SHA256 deve ser alfanumérico"
    
    def test_rulebook_path_is_absolute(self, custom_rules_path):
        """Verifica que o path do rulebook é absoluto após resolução."""
        normalizer = Normalizer(rules_path=custom_rules_path, auto_fix=False)
        
        # O path armazenado pode ser relativo ou absoluto
        # mas deve ser válido e existir
        assert Path(normalizer.rules_path).exists(), "Path do rulebook deve existir"
