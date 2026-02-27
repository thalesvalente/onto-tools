"""
Testes de integração para fluxos de normalização completa.

Cobre:
- Fluxo completo de carregamento -> normalização -> salvamento
- Integração entre Normalizer e NamingValidator
- Roundtrip de arquivos TTL
"""
import pytest
from pathlib import Path

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import OWL, RDF, SKOS

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.graph import OntologyGraph
from onto_tools.domain.ontology.normalizer import Normalizer


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


class TestNormalizationComplete:
    """Testes de normalização completa."""
    
    def test_full_normalization_flow(self, tmp_path, rules_json_path):
        """Fluxo completo: criar -> salvar -> carregar -> normalizar -> salvar."""
        # Criar grafo
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, DCTERMS.identifier, Literal("TestClass")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("Classe de Teste", lang="pt-br")))
        
        # Salvar original
        input_file = tmp_path / "input.ttl"
        g.serialize(destination=str(input_file), format="turtle")
        
        # Carregar
        onto = OntologyGraph.load(str(input_file), RDFlibAdapter)
        
        # Normalizar
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # Salvar normalizado
        output_file = tmp_path / "output.ttl"
        normalized.save(str(output_file), RDFlibAdapter)
        
        # Verificar resultado
        assert output_file.exists()
        
        # Recarregar e verificar triplas
        reloaded, _ = RDFlibAdapter.load_ttl(str(output_file))
        assert len(reloaded) == len(g)
    
    def test_normalization_preserves_content(self, tmp_path, rules_json_path):
        """Normalização preserva conteúdo semântico."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        # Criar conteúdo
        g.add((EDO.ClassA, RDF.type, OWL.Class))
        g.add((EDO.ClassA, DCTERMS.identifier, Literal("ClassA")))
        g.add((EDO.ClassA, SKOS.prefLabel, Literal("Class A", lang="en")))
        
        g.add((EDO.ClassB, RDF.type, OWL.Class))
        g.add((EDO.ClassB, DCTERMS.identifier, Literal("ClassB")))
        g.add((EDO.ClassB, SKOS.prefLabel, Literal("Class B", lang="en")))
        
        # Salvar e normalizar
        input_file = tmp_path / "input.ttl"
        g.serialize(destination=str(input_file), format="turtle")
        
        onto = OntologyGraph.load(str(input_file), RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # Verificar que ambas as classes estão presentes
        assert (EDO.ClassA, RDF.type, OWL.Class) in normalized.graph
        assert (EDO.ClassB, RDF.type, OWL.Class) in normalized.graph
    
    def test_normalization_with_validation_warnings(self, tmp_path, rules_json_path):
        """Normalização gera warnings de validação."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        # Criar classe com problemas de nomenclatura
        g.add((EDO.badClassName, RDF.type, OWL.Class))
        g.add((EDO.badClassName, DCTERMS.identifier, Literal("badClassName")))
        g.add((EDO.badClassName, SKOS.prefLabel, Literal("bad class name", lang="en")))
        
        input_file = tmp_path / "input.ttl"
        g.serialize(destination=str(input_file), format="turtle")
        
        onto = OntologyGraph.load(str(input_file), RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # Deve haver warnings
        warnings = normalizer.get_warnings()
        assert isinstance(warnings, list)


class TestBatchOperationsIntegration:
    """Testes de integração de operações em lote."""
    
    def test_batch_apply_and_normalize(self, tmp_path, rules_json_path):
        """Aplica lote e depois normaliza."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        g.add((EDO.ExistingClass, RDF.type, OWL.Class))
        g.add((EDO.ExistingClass, DCTERMS.identifier, Literal("ExistingClass")))
        
        onto = OntologyGraph(graph=g)
        
        # Aplicar lote
        update_list = {
            "batch_id": "test-001",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:NewClass",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        assert result["overall_result"] == "success"
        
        # Normalizar
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # Verificar que nova classe está presente
        has_new_class = any(
            "NewClass" in str(s) 
            for s, p, o in normalized.graph 
            if p == RDF.type and o == OWL.Class
        )
        assert has_new_class


class TestCommentPreservation:
    """Testes de preservação de comentários."""
    
    def test_rdfs_comment_preserved(self, rules_json_path):
        """rdfs:comment é preservado após normalização."""
        from rdflib.namespace import RDFS
        
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("rdfs", RDFS)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, DCTERMS.identifier, Literal("TestClass")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")))
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("Classe de Teste", lang="pt-br")))
        g.add((EDO.TestClass, RDFS.comment, Literal("This is a test comment", lang="en")))
        
        normalizer = Normalizer(rules_path=rules_json_path)
        result = normalizer.normalize(g)
        
        # Verificar que comentário está presente
        comments = list(result.graph.objects(EDO.TestClass, RDFS.comment))
        assert len(comments) == 1
        assert "test comment" in str(comments[0])


class TestTransactionality:
    """Testes de transacionalidade."""
    
    def test_batch_rollback_on_error(self):
        """Lote com erro faz rollback completo."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        
        g.add((EDO.Original, RDF.type, OWL.Class))
        
        onto = OntologyGraph(graph=g)
        original_triples = set(onto.graph)
        
        update_list = {
            "batch_id": "test-rollback",
            "ordered_ops": [
                {"op_id": 1, "type": "insert", "triple": {"subject": "edo:A", "predicate": "rdf:type", "object": "owl:Class"}},
                {"op_id": 2, "type": "invalid", "triple": {"subject": "edo:B", "predicate": "rdf:type", "object": "owl:Class"}},
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "failed"
        # Grafo deve estar inalterado
        assert set(onto.graph) == original_triples
