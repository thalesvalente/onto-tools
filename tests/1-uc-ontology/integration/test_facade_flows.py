"""
Testes de integração para fluxos de fachada (Facade).

Cobre:
- Fluxos orquestrados pela camada application
- Integração entre adapters e domain
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


class TestFacadeFlows:
    """Testes de fluxos da fachada."""
    
    def test_load_normalize_save_flow(self, tmp_path, rules_json_path):
        """Fluxo completo: carregar -> normalizar -> salvar."""
        # Criar arquivo de entrada
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
        
        input_file = tmp_path / "input.ttl"
        g.serialize(destination=str(input_file), format="turtle")
        
        # Fluxo
        onto = OntologyGraph.load(str(input_file), RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        output_file = tmp_path / "output.ttl"
        normalized.save(str(output_file), RDFlibAdapter)
        
        # Verificar
        assert output_file.exists()
        reloaded, _ = RDFlibAdapter.load_ttl(str(output_file))
        assert len(reloaded) >= len(g)
    
    def test_query_flow(self, minimal_class_graph):
        """Fluxo de consulta SPARQL usando rdflib diretamente."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        SELECT ?class
        WHERE {
            ?class rdf:type owl:Class
        }
        """
        
        # Usar query direta no grafo (evita signal.alarm do SparqlAdapter)
        results = list(minimal_class_graph.query(query))
        
        assert len(results) > 0
    
    def test_diff_flow(self, minimal_class_graph):
        """Fluxo de comparação entre grafos."""
        onto1 = OntologyGraph(graph=minimal_class_graph)
        
        # Criar versão modificada
        g2 = Graph()
        for triple in minimal_class_graph:
            g2.add(triple)
        g2.add((EDO.NewClass, RDF.type, OWL.Class))
        
        onto2 = OntologyGraph(graph=g2)
        
        diff = onto1.diff(onto2)
        
        assert diff["added_count"] == 1
        assert diff["removed_count"] == 0
    
    def test_batch_apply_flow(self, minimal_class_graph):
        """Fluxo de aplicação de lote."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "facade-test",
            "onto_name": "test",
            "onto_version": "1.0",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:FacadeClass",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"
        assert result["batch_id"] == "facade-test"


class TestEdgeToEdgeFlows:
    """Testes de fluxo ponta-a-ponta."""
    
    def test_full_crud_cycle(self, tmp_path, rules_json_path):
        """Ciclo completo CRUD."""
        # CREATE
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        g.add((EDO.InitialClass, RDF.type, OWL.Class))
        g.add((EDO.InitialClass, DCTERMS.identifier, Literal("InitialClass")))
        
        input_file = tmp_path / "crud.ttl"
        g.serialize(destination=str(input_file), format="turtle")
        
        # READ
        onto = OntologyGraph.load(str(input_file), RDFlibAdapter)
        assert onto.metadata.triple_count >= 2
        
        # UPDATE (add)
        onto.add_triple("edo:NewClass", "rdf:type", "owl:Class")
        
        # UPDATE (remove)
        # (não remover nada por enquanto para manter o teste simples)
        
        # Normalize
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # SAVE (persist)
        output_file = tmp_path / "crud_output.ttl"
        normalized.save(str(output_file), RDFlibAdapter)
        
        # Verify
        assert output_file.exists()
        final, _ = RDFlibAdapter.load_ttl(str(output_file))
        
        # Deve ter a classe original + a nova
        class_count = len(list(final.subjects(RDF.type, OWL.Class)))
        assert class_count >= 2
