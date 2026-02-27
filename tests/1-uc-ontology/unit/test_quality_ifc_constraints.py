"""
Testes de qualidade para constraints de classes IFC

Verifica:
- Classe IFC sem propriedades obrigatórias gera ERROR
- Classe IFC sem base class gera ERROR
- Classe IFC completa não gera issues
- Validador NÃO modifica o grafo
"""
import pytest
from pathlib import Path

from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS

from onto_tools.domain.ontology.quality_validator import (
    OntologyQualityValidator,
    ValidationIssue,
    ValidationReport
)


EDO = Namespace("https://w3id.org/energy-domain/edo#")
FIXTURES_PATH = Path(__file__).parent.parent / "fixtures" / "ontology_quality_samples.ttl"


@pytest.fixture
def validator():
    """Cria instância do validador."""
    return OntologyQualityValidator()


@pytest.fixture
def sample_graph():
    """Carrega grafo de exemplo."""
    g = Graph()
    g.parse(str(FIXTURES_PATH), format="turtle")
    return g


@pytest.fixture
def incomplete_ifc_graph():
    """Grafo com classe IFC incompleta."""
    g = Graph()
    g.parse(data="""
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:IncompleteIfc a owl:Class ;
            skos:prefLabel "Incomplete IFC"@en ;
            dcterms:identifier "IncompleteIfc" ;
            edo:ifc_objectType "IfcPipe" .
    """, format="turtle")
    return g


@pytest.fixture
def complete_ifc_graph():
    """Grafo com classe IFC completa."""
    g = Graph()
    g.parse(data="""
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:IfcInstanciableElement a owl:Class .
        
        edo:CompleteIfc a owl:Class ;
            rdfs:subClassOf edo:IfcInstanciableElement ;
            skos:prefLabel "Complete IFC"@en ;
            dcterms:identifier "CompleteIfc" ;
            edo:ifc_equivalentClass "IfcPipeSegment" ;
            edo:ifc_objectType "IfcPipeSegment" ;
            edo:ifc_predefinedType "RIGIDSEGMENT" ;
            edo:hasDiscipline edo:Piping .
        
        edo:Piping a owl:NamedIndividual .
    """, format="turtle")
    return g


@pytest.fixture
def missing_base_class_graph():
    """Grafo com classe IFC sem base class."""
    g = Graph()
    g.parse(data="""
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix dcterms: <http://purl.org/dc/terms/> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:IfcNoBase a owl:Class ;
            skos:prefLabel "IFC No Base"@en ;
            dcterms:identifier "IfcNoBase" ;
            edo:ifc_equivalentClass "IfcWall" ;
            edo:ifc_objectType "IfcWall" ;
            edo:ifc_predefinedType "STANDARD" ;
            edo:hasDiscipline edo:Structural .
        
        edo:Structural a owl:NamedIndividual .
    """, format="turtle")
    return g


class TestIfcMissingProperties:
    """Testes para classes IFC sem propriedades obrigatórias."""
    
    def test_ifc_class_missing_required_properties_is_error(self, validator, incomplete_ifc_graph):
        """
        GIVEN: Classe com edo:ifc* property mas sem todas propriedades obrigatórias
        WHEN: Executar validação
        THEN: Deve gerar issues com code IFC_REQUIRED_PROPERTY_MISSING
        """
        report = validator.validate(incomplete_ifc_graph)
        
        missing_prop_issues = [i for i in report.issues if i.code == "IFC_REQUIRED_PROPERTY_MISSING"]
        
        assert len(missing_prop_issues) >= 1, "Deveria detectar propriedades IFC ausentes"
        assert all(i.severity == "ERROR" for i in missing_prop_issues)
    
    def test_ifc_class_missing_properties_lists_which(self, validator, incomplete_ifc_graph):
        """
        GIVEN: Classe IFC incompleta
        WHEN: Executar validação
        THEN: Deve listar quais propriedades estão faltando
        """
        report = validator.validate(incomplete_ifc_graph)
        
        missing_prop_issues = [i for i in report.issues if i.code == "IFC_REQUIRED_PROPERTY_MISSING"]
        
        missing_props = [i.extra.get("missing_property") for i in missing_prop_issues]
        
        # Deve faltar pelo menos ifc_equivalentClass e ifc_predefinedType
        assert any("ifc_equivalentClass" in p for p in missing_props if p)
    
    def test_incomplete_ifc_in_fixture(self, validator, sample_graph):
        """
        GIVEN: Fixture com IncompleteIfcClass
        WHEN: Executar validação
        THEN: Deve detectar propriedades IFC ausentes
        """
        report = validator.validate(sample_graph)
        
        incomplete_ifc_issues = [
            i for i in report.issues 
            if i.code == "IFC_REQUIRED_PROPERTY_MISSING" and "IncompleteIfcClass" in str(i.subject)
        ]
        
        assert len(incomplete_ifc_issues) >= 1


class TestIfcMissingBaseClass:
    """Testes para classes IFC sem base class."""
    
    def test_ifc_class_missing_base_class_is_error(self, validator, missing_base_class_graph):
        """
        GIVEN: Classe com propriedades edo:ifc* mas sem rdfs:subClassOf edo:IfcInstanciableElement
        WHEN: Executar validação
        THEN: Deve gerar issue com code IFC_BASE_CLASS_MISSING
        """
        report = validator.validate(missing_base_class_graph)
        
        base_class_issues = [i for i in report.issues if i.code == "IFC_BASE_CLASS_MISSING"]
        
        assert len(base_class_issues) >= 1, "Deveria detectar base class IFC ausente"
        assert base_class_issues[0].severity == "ERROR"
    
    def test_missing_base_class_shows_required(self, validator, missing_base_class_graph):
        """
        GIVEN: Classe IFC sem base class
        WHEN: Executar validação
        THEN: Issue deve indicar qual base class é requerida
        """
        report = validator.validate(missing_base_class_graph)
        
        base_class_issues = [i for i in report.issues if i.code == "IFC_BASE_CLASS_MISSING"]
        
        assert len(base_class_issues) >= 1
        assert "IfcInstanciableElement" in base_class_issues[0].extra.get("required_base_class", "")


class TestCompleteIfcClass:
    """Testes para classes IFC completas."""
    
    def test_complete_ifc_class_no_issues(self, validator, complete_ifc_graph):
        """
        GIVEN: Classe IFC com todas propriedades obrigatórias e base class
        WHEN: Executar validação
        THEN: Não deve gerar issues de IFC
        """
        report = validator.validate(complete_ifc_graph)
        
        ifc_issues = [
            i for i in report.issues 
            if i.code in ("IFC_REQUIRED_PROPERTY_MISSING", "IFC_BASE_CLASS_MISSING")
            and "CompleteIfc" in str(i.subject)
        ]
        
        assert len(ifc_issues) == 0, "Classe IFC completa não deve gerar issues"
    
    def test_complete_ifc_in_fixture(self, validator, sample_graph):
        """
        GIVEN: Fixture com CompleteIfcClass
        WHEN: Executar validação
        THEN: CompleteIfcClass não deve gerar issues de IFC
        """
        report = validator.validate(sample_graph)
        
        complete_ifc_issues = [
            i for i in report.issues 
            if (i.code in ("IFC_REQUIRED_PROPERTY_MISSING", "IFC_BASE_CLASS_MISSING")
                and "CompleteIfcClass" in str(i.subject))
        ]
        
        assert len(complete_ifc_issues) == 0


class TestNonIfcClass:
    """Testes para classes que não são IFC."""
    
    def test_non_ifc_class_no_ifc_issues(self, validator):
        """
        GIVEN: Classe sem propriedades edo:ifc*
        WHEN: Executar validação
        THEN: Não deve gerar issues de IFC
        """
        g = Graph()
        g.parse(data="""
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
            @prefix dcterms: <http://purl.org/dc/terms/> .
            @prefix edo: <https://w3id.org/energy-domain/edo#> .
            
            edo:RegularClass a owl:Class ;
                skos:prefLabel "Regular Class"@en ;
                dcterms:identifier "RegularClass" ;
                edo:hasAttribute edo:SomeAttribute .
        """, format="turtle")
        
        report = validator.validate(g)
        
        ifc_issues = [
            i for i in report.issues 
            if i.code in ("IFC_REQUIRED_PROPERTY_MISSING", "IFC_BASE_CLASS_MISSING")
        ]
        
        assert len(ifc_issues) == 0, "Classe não-IFC não deve gerar issues de IFC"


class TestGraphNotModified:
    """Testes para garantir que o grafo não é modificado."""
    
    def test_validation_does_not_add_properties(self, validator, incomplete_ifc_graph):
        """
        GIVEN: Classe IFC incompleta
        WHEN: Executar validação
        THEN: O grafo NÃO deve ter propriedades adicionadas
        """
        triples_before = len(incomplete_ifc_graph)
        
        validator.validate(incomplete_ifc_graph)
        
        triples_after = len(incomplete_ifc_graph)
        
        assert triples_before == triples_after
    
    def test_validation_does_not_add_base_class(self, validator, missing_base_class_graph):
        """
        GIVEN: Classe IFC sem base class
        WHEN: Executar validação
        THEN: O grafo NÃO deve ter rdfs:subClassOf adicionado
        """
        subclasses_before = list(missing_base_class_graph.objects(
            EDO.IfcNoBase, RDFS.subClassOf
        ))
        
        validator.validate(missing_base_class_graph)
        
        subclasses_after = list(missing_base_class_graph.objects(
            EDO.IfcNoBase, RDFS.subClassOf
        ))
        
        assert subclasses_before == subclasses_after
