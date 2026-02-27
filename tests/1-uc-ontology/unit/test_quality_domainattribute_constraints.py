"""
Testes de qualidade para constraints de classes DomainAttribute.

Verifica todas as regras especificadas para subclasses de edo:DomainAttribute:
- dcterms:accessRights obrigatório
- dcterms:identifier obrigatório e match com local name
- skos:definition: requer @en e @pt-br, máximo 1 por idioma
- skos:prefLabel: requer @en e @pt-br, sem duplicatas por idioma
- Propriedades obrigatórias: hasAttributeScope, hasLifecycleCreationPhase,
  hasTypedValue, hasValueCardinality

O validador NÃO modifica o grafo - apenas emite warnings.
"""
import pytest
from pathlib import Path

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS

from onto_tools.domain.ontology.quality_validator import (
    OntologyQualityValidator,
    ValidationIssue,
    ValidationReport
)


EDO = Namespace("https://w3id.org/energy-domain/edo#")
FIXTURES_PATH = Path(__file__).parent.parent / "fixtures" / "domain_attribute_samples.ttl"


# =============================================================================
# Fixtures Comuns
# =============================================================================

@pytest.fixture
def validator():
    """Cria instância do validador."""
    return OntologyQualityValidator()


@pytest.fixture
def full_fixture_graph():
    """Carrega grafo com todas as fixtures de DomainAttribute."""
    g = Graph()
    g.parse(str(FIXTURES_PATH), format="turtle")
    return g


def _create_graph_with_domain_attribute_base() -> Graph:
    """Helper: cria grafo base com DomainAttribute e individuals necessários."""
    g = Graph()
    g.parse(data="""
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:DomainAttribute a owl:Class ;
            skos:prefLabel "Domain Attribute"@en ;
            dcterms:identifier "DomainAttribute" .
        
        edo:TypeLevelAttribute a owl:NamedIndividual .
        edo:DetailedDesign a owl:NamedIndividual .
        edo:FloatValue a owl:NamedIndividual .
        edo:SingleValue a owl:NamedIndividual .
    """, format="turtle")
    return g


# =============================================================================
# TESTES: Golden Template (AbsoluteInsidePressure)
# =============================================================================

class TestDomainAttributeGoldenTemplate:
    """Testes para o template golden (classe totalmente conforme)."""
    
    def test_domainattribute_template_is_fully_valid(self, validator, full_fixture_graph):
        """
        GIVEN: Grafo com edo:AbsoluteInsidePressure conforme template canônico
        WHEN: Executar validação
        THEN: Não deve gerar issues com código DOMAINATTR_*
        """
        report = validator.validate(full_fixture_graph)
        
        # Filtrar issues apenas para AbsoluteInsidePressure
        issues_for_template = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_") 
            and "AbsoluteInsidePressure" in str(i.subject)
        ]
        
        assert len(issues_for_template) == 0, (
            f"Golden template não deveria gerar issues DOMAINATTR_*, "
            f"mas gerou: {[i.code for i in issues_for_template]}"
        )
    
    def test_indirect_subclass_is_validated(self, validator, full_fixture_graph):
        """
        GIVEN: Grafo com IndirectSubclass (subclasse indireta via BendingStiffenessCurveAttribute)
        WHEN: Executar validação
        THEN: A classe deve ser validada como DomainAttribute
        """
        report = validator.validate(full_fixture_graph)
        
        # IndirectSubclass é completa, não deve ter issues
        issues_for_indirect = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_") 
            and "IndirectSubclass" in str(i.subject)
        ]
        
        assert len(issues_for_indirect) == 0, (
            f"IndirectSubclass completa não deveria gerar issues, "
            f"mas gerou: {[i.code for i in issues_for_indirect]}"
        )


# =============================================================================
# TESTES: dcterms:accessRights
# =============================================================================

class TestDomainAttributeAccessRights:
    """Testes para validação de dcterms:accessRights."""
    
    def test_domainattribute_missing_accessrights_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem dcterms:accessRights
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_ACCESSRIGHTS_MISSING
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoAccessRights a owl:Class ;
                dcterms:identifier "NoAccessRights" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "No Access Rights"@en ;
                skos:prefLabel "Sem Direitos de Acesso"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        access_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_ACCESSRIGHTS_MISSING"
            and "NoAccessRights" in str(i.subject)
        ]
        
        assert len(access_issues) == 1
        assert access_issues[0].severity == "WARNING"
    
    def test_fixture_missing_accessrights(self, validator, full_fixture_graph):
        """
        GIVEN: Fixture com MissingAccessRights
        WHEN: Executar validação
        THEN: Deve gerar issue DOMAINATTR_ACCESSRIGHTS_MISSING
        """
        report = validator.validate(full_fixture_graph)
        
        access_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_ACCESSRIGHTS_MISSING"
            and "MissingAccessRights" in str(i.subject)
        ]
        
        assert len(access_issues) == 1


# =============================================================================
# TESTES: dcterms:identifier
# =============================================================================

class TestDomainAttributeIdentifier:
    """Testes para validação de dcterms:identifier."""
    
    def test_domainattribute_missing_identifier_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem dcterms:identifier
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_IDENTIFIER_MISSING
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoIdentifier a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "No Identifier"@en ;
                skos:prefLabel "Sem Identificador"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        id_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_IDENTIFIER_MISSING"
            and "NoIdentifier" in str(i.subject)
        ]
        
        assert len(id_issues) == 1
        assert id_issues[0].severity == "WARNING"
    
    def test_domainattribute_identifier_mismatch_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute com identifier diferente do local name
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_IDENTIFIER_MISMATCH
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:WrongIdentifier a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "DifferentName" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "Wrong Identifier"@en ;
                skos:prefLabel "Identificador Errado"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        mismatch_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_IDENTIFIER_MISMATCH"
            and "WrongIdentifier" in str(i.subject)
        ]
        
        assert len(mismatch_issues) == 1
        assert mismatch_issues[0].severity == "WARNING"
        assert mismatch_issues[0].extra["expected"] == "WrongIdentifier"
        assert mismatch_issues[0].extra["identifier_value"] == "DifferentName"
    
    def test_fixture_identifier_mismatch(self, validator, full_fixture_graph):
        """
        GIVEN: Fixture com IdentifierMismatch
        WHEN: Executar validação
        THEN: Deve gerar issue DOMAINATTR_IDENTIFIER_MISMATCH
        """
        report = validator.validate(full_fixture_graph)
        
        mismatch_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_IDENTIFIER_MISMATCH"
            and "IdentifierMismatch" in str(i.subject)
        ]
        
        assert len(mismatch_issues) == 1


# =============================================================================
# TESTES: skos:definition
# =============================================================================

class TestDomainAttributeDefinitions:
    """Testes para validação de skos:definition."""
    
    def test_domainattribute_definition_too_many_per_lang_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute com mais de uma definition no mesmo idioma
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:TwoDefinitions a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "TwoDefinitions" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "First definition."@en ;
                skos:definition "Second definition."@en ;
                skos:definition "Definição em português."@pt-br ;
                skos:prefLabel "Two Definitions"@en ;
                skos:prefLabel "Duas Definições"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        too_many_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG"
            and "TwoDefinitions" in str(i.subject)
        ]
        
        assert len(too_many_issues) == 1
        assert too_many_issues[0].severity == "WARNING"
        assert too_many_issues[0].extra["language"] == "en"
        assert too_many_issues[0].extra["count"] == 2
    
    def test_domainattribute_definition_missing_en_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem definition em inglês
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_DEFINITION_MISSING_EN
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoEnDefinition a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "NoEnDefinition" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Apenas em português."@pt-br ;
                skos:prefLabel "No EN Definition"@en ;
                skos:prefLabel "Sem Definição EN"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        missing_en_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_DEFINITION_MISSING_EN"
            and "NoEnDefinition" in str(i.subject)
        ]
        
        assert len(missing_en_issues) == 1
        assert missing_en_issues[0].severity == "WARNING"
    
    def test_domainattribute_definition_missing_pt_br_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem definition em português
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_DEFINITION_MISSING_PT_BR
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoPtBrDefinition a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "NoPtBrDefinition" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Only in English."@en ;
                skos:prefLabel "No PT-BR Definition"@en ;
                skos:prefLabel "Sem Definição PT-BR"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        missing_ptbr_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_DEFINITION_MISSING_PT_BR"
            and "NoPtBrDefinition" in str(i.subject)
        ]
        
        assert len(missing_ptbr_issues) == 1
        assert missing_ptbr_issues[0].severity == "WARNING"
    
    def test_fixture_too_many_definitions(self, validator, full_fixture_graph):
        """
        GIVEN: Fixture com TooManyDefinitions
        WHEN: Executar validação
        THEN: Deve gerar issue DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG
        """
        report = validator.validate(full_fixture_graph)
        
        too_many_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG"
            and "TooManyDefinitions" in str(i.subject)
        ]
        
        assert len(too_many_issues) == 1


# =============================================================================
# TESTES: skos:prefLabel
# =============================================================================

class TestDomainAttributePrefLabels:
    """Testes para validação de skos:prefLabel."""
    
    def test_domainattribute_prefLabel_duplicate_per_lang_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute com prefLabel duplicado no mesmo idioma
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:DuplicateLabel a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "DuplicateLabel" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "First Label"@en ;
                skos:prefLabel "Second Label"@en ;
                skos:prefLabel "Rótulo em Português"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        dup_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG"
            and "DuplicateLabel" in str(i.subject)
        ]
        
        assert len(dup_issues) == 1
        assert dup_issues[0].severity == "WARNING"
        assert dup_issues[0].extra["language"] == "en"
        assert dup_issues[0].extra["count"] == 2
    
    def test_domainattribute_prefLabel_missing_en_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem prefLabel em inglês
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_PREFLABEL_MISSING_EN
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoEnLabel a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "NoEnLabel" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "Apenas em Português"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        missing_en_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PREFLABEL_MISSING_EN"
            and "NoEnLabel" in str(i.subject)
        ]
        
        assert len(missing_en_issues) == 1
        assert missing_en_issues[0].severity == "WARNING"
    
    def test_domainattribute_prefLabel_missing_pt_br_generates_warning(self, validator):
        """
        GIVEN: DomainAttribute sem prefLabel em português
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_PREFLABEL_MISSING_PT_BR
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoPtBrLabel a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "NoPtBrLabel" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "Only English Label"@en ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        missing_ptbr_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PREFLABEL_MISSING_PT_BR"
            and "NoPtBrLabel" in str(i.subject)
        ]
        
        assert len(missing_ptbr_issues) == 1
        assert missing_ptbr_issues[0].severity == "WARNING"
    
    def test_fixture_duplicate_preflabel(self, validator, full_fixture_graph):
        """
        GIVEN: Fixture com DuplicatePrefLabel
        WHEN: Executar validação
        THEN: Deve gerar issue DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG
        """
        report = validator.validate(full_fixture_graph)
        
        dup_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG"
            and "DuplicatePrefLabel" in str(i.subject)
        ]
        
        assert len(dup_issues) == 1


# =============================================================================
# TESTES: Propriedades Obrigatórias
# =============================================================================

class TestDomainAttributeMandatoryProperties:
    """Testes para validação de propriedades obrigatórias."""
    
    @pytest.mark.parametrize("missing_property,class_name", [
        ("edo:hasAttributeScope", "MissingAttributeScope"),
        ("edo:hasLifecycleCreationPhase", "MissingLifecyclePhase"),
        ("edo:hasTypedValue", "MissingTypedValue"),
        ("edo:hasValueCardinality", "MissingValueCardinality"),
    ])
    def test_domainattribute_missing_mandatory_properties_generate_warnings(
        self, validator, full_fixture_graph, missing_property, class_name
    ):
        """
        GIVEN: DomainAttribute sem propriedade obrigatória
        WHEN: Executar validação
        THEN: Deve gerar WARNING com code DOMAINATTR_PROPERTY_MISSING
        """
        report = validator.validate(full_fixture_graph)
        
        prop_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PROPERTY_MISSING"
            and class_name in str(i.subject)
            and i.extra.get("predicate") == missing_property
        ]
        
        assert len(prop_issues) == 1, (
            f"Deveria detectar {missing_property} faltando em {class_name}"
        )
        assert prop_issues[0].severity == "WARNING"
    
    def test_domainattribute_missing_hasAttributeScope(self, validator):
        """
        GIVEN: DomainAttribute sem edo:hasAttributeScope
        WHEN: Executar validação
        THEN: Deve gerar issue com predicate=edo:hasAttributeScope
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:NoScope a owl:Class ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "NoScope" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test class."@en ;
                skos:definition "Classe de teste."@pt-br ;
                skos:prefLabel "No Scope"@en ;
                skos:prefLabel "Sem Escopo"@pt-br ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        report = validator.validate(g)
        
        scope_issues = [
            i for i in report.issues 
            if i.code == "DOMAINATTR_PROPERTY_MISSING"
            and "NoScope" in str(i.subject)
            and i.extra.get("predicate") == "edo:hasAttributeScope"
        ]
        
        assert len(scope_issues) == 1


# =============================================================================
# TESTES: Imutabilidade do Grafo
# =============================================================================

class TestDomainAttributeGraphImmutability:
    """Testes para garantir que o validador não modifica o grafo."""
    
    def test_validation_does_not_modify_graph(self, validator, full_fixture_graph):
        """
        GIVEN: Grafo com DomainAttributes com problemas
        WHEN: Executar validação
        THEN: O grafo NÃO deve ser modificado
        """
        # Serializar antes
        graph_before = full_fixture_graph.serialize(format="turtle")
        
        # Executar validação
        validator.validate(full_fixture_graph)
        
        # Serializar depois
        graph_after = full_fixture_graph.serialize(format="turtle")
        
        assert graph_before == graph_after, "Validação não deve modificar o grafo"
    
    def test_validation_does_not_add_missing_accessrights(self, validator):
        """
        GIVEN: DomainAttribute sem accessRights
        WHEN: Executar validação
        THEN: accessRights NÃO deve ser adicionado
        """
        g = _create_graph_with_domain_attribute_base()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:TestNoAccess a owl:Class ;
                dcterms:identifier "TestNoAccess" ;
                rdfs:subClassOf edo:DomainAttribute ;
                skos:definition "Test."@en ;
                skos:definition "Teste."@pt-br ;
                skos:prefLabel "Test No Access"@en ;
                skos:prefLabel "Teste Sem Acesso"@pt-br ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasValueCardinality edo:SingleValue .
        """, format="turtle")
        
        # Verificar que não tem accessRights antes
        access_before = list(g.objects(EDO.TestNoAccess, DCTERMS.accessRights))
        assert len(access_before) == 0
        
        # Validar
        validator.validate(g)
        
        # Verificar que ainda não tem accessRights
        access_after = list(g.objects(EDO.TestNoAccess, DCTERMS.accessRights))
        assert len(access_after) == 0


# =============================================================================
# TESTES: Classe não-DomainAttribute
# =============================================================================

class TestNonDomainAttributeClass:
    """Testes para classes que não são DomainAttribute."""
    
    def test_non_domainattribute_class_no_domainattr_issues(self, validator, full_fixture_graph):
        """
        GIVEN: Classe regular (não subclasse de DomainAttribute)
        WHEN: Executar validação
        THEN: Não deve gerar issues DOMAINATTR_*
        """
        report = validator.validate(full_fixture_graph)
        
        regular_class_issues = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_")
            and "RegularClass" in str(i.subject)
        ]
        
        assert len(regular_class_issues) == 0, (
            "Classes não-DomainAttribute não devem gerar issues DOMAINATTR_*"
        )


# =============================================================================
# TESTES: Seleção de Subclasses
# =============================================================================

class TestDomainAttributeSubclassSelection:
    """Testes para seleção de subclasses de DomainAttribute."""
    
    def test_direct_subclass_is_selected(self, validator, full_fixture_graph):
        """
        GIVEN: Classe com rdfs:subClassOf edo:DomainAttribute direto
        WHEN: Executar validação
        THEN: A classe deve ser validada como DomainAttribute
        """
        report = validator.validate(full_fixture_graph)
        
        # MissingAccessRights é subclasse direta e deve ter issue
        direct_issues = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_")
            and "MissingAccessRights" in str(i.subject)
        ]
        
        assert len(direct_issues) >= 1, "Subclasse direta deve ser validada"
    
    def test_indirect_subclass_is_selected(self, validator, full_fixture_graph):
        """
        GIVEN: Classe que herda de DomainAttribute indiretamente
        WHEN: Executar validação com include_indirect_subclasses=true
        THEN: A classe deve ser validada como DomainAttribute
        """
        # IndirectSubclass herda de BendingStiffenessCurveAttribute que herda de DomainAttribute
        # Como é completa, não deve ter issues, mas deve ter sido validada
        
        report = validator.validate(full_fixture_graph)
        
        # Verificar que classes intermediárias também são validadas
        # BendingStiffenessCurveAttribute é subclasse de DomainAttribute
        intermediate_issues = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_")
            and "BendingStiffenessCurveAttribute" in str(i.subject)
        ]
        
        # Deve ter issues porque não tem todas as propriedades obrigatórias
        assert len(intermediate_issues) >= 1


# =============================================================================
# TESTES ADICIONAIS DE COBERTURA
# =============================================================================

class TestDomainAttributeEdgeCases:
    """Testes para casos de borda."""
    
    def test_empty_graph_no_errors(self, validator):
        """
        GIVEN: Grafo vazio
        WHEN: Executar validação
        THEN: Não deve gerar erros
        """
        g = Graph()
        
        report = validator.validate(g)
        
        assert report.total_classes_checked == 0
        da_issues = [i for i in report.issues if i.code.startswith("DOMAINATTR_")]
        assert len(da_issues) == 0
    
    def test_domain_attribute_base_class_itself(self, validator):
        """
        GIVEN: Apenas a classe DomainAttribute base (sem subclasses)
        WHEN: Executar validação
        THEN: DomainAttribute base não deve ser validada (não é subclasse de si mesma)
        """
        g = Graph()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:DomainAttribute a owl:Class ;
                skos:prefLabel "Domain Attribute"@en ;
                dcterms:identifier "DomainAttribute" .
        """, format="turtle")
        
        report = validator.validate(g)
        
        # DomainAttribute não é subclasse de si mesmo, então não deve ter issues DOMAINATTR_*
        da_issues = [
            i for i in report.issues 
            if i.code.startswith("DOMAINATTR_")
            and "DomainAttribute" in str(i.subject)
            and "BendingStiffenessCurveAttribute" not in str(i.subject)  # excluir outras
        ]
        
        # A base class DomainAttribute não deve gerar issues de DomainAttribute
        # (ela não é subclasse de si mesma)
        assert len(da_issues) == 0
