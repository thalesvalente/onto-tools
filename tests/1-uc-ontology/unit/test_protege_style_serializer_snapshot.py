"""
Testes snapshot para o serializador estilo Protégé.

Compara o output do serializador com fixtures golden exportadas do Protégé.
"""
import pytest
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, DCTERMS

from onto_tools.adapters.rdf.protege_serializer import (
    ProtegeStyleTurtleSerializer,
    serialize_protege_style,
)


# Diretório das fixtures
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class TestProtegeStyleSerializerSnapshot:
    """Testes snapshot comparando output com fixtures golden."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_base_graph(self, edo: Namespace) -> Graph:
        """Cria grafo base com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        return graph

    def _normalize_ttl(self, content: str) -> str:
        """
        Normaliza TTL para comparação.
        
        Remove espaços em branco extras e normaliza line endings.
        """
        lines = content.strip().split("\n")
        normalized = []
        for line in lines:
            # Remover trailing whitespace mas preservar indentação
            normalized.append(line.rstrip())
        return "\n".join(normalized)

    def test_deadweightcollar_snapshot(self, edo_namespace):
        """
        Testa que DeadweightCollar é serializado exatamente como o golden.
        """
        edo = edo_namespace
        graph = self._create_base_graph(edo)

        # Adicionar triplas programaticamente
        graph.add((edo.DeadweightCollar, RDF.type, OWL.Class))
        graph.add((edo.DeadweightCollar, RDFS.subClassOf, edo.DomainElement))
        graph.add((edo.DeadweightCollar, RDFS.subClassOf, edo.IfcInstanciableElement))
        graph.add((edo.DeadweightCollar, DCTERMS.identifier, Literal("DeadweightCollar")))
        graph.add((edo.DeadweightCollar, SKOS.prefLabel, Literal("Deadweight Collar", lang="en")))
        graph.add((edo.DeadweightCollar, SKOS.prefLabel, Literal("Colar de Peso Morto", lang="pt-br")))
        graph.add((edo.DeadweightCollar, SKOS.definition, Literal(
            "A collar used to add weight to a structure or component.", lang="en"
        )))
        graph.add((edo.DeadweightCollar, SKOS.definition, Literal(
            "Um colar usado para adicionar peso a uma estrutura ou componente.", lang="pt-br"
        )))

        # Serializar
        result = serialize_protege_style(graph)
        
        # Carregar golden
        golden_path = FIXTURES_DIR / "protege_deadweightcollar.ttl"
        golden = golden_path.read_text(encoding="utf-8")

        # Comparar
        assert self._normalize_ttl(result) == self._normalize_ttl(golden), \
            f"Output não corresponde ao golden:\n---RESULTADO---\n{result}\n---GOLDEN---\n{golden}"

    def test_grooveheight_snapshot(self, edo_namespace):
        """
        Testa que GrooveHeight é serializado exatamente como o golden.
        """
        edo = edo_namespace
        graph = self._create_base_graph(edo)

        # Adicionar triplas programaticamente
        graph.add((edo.GrooveHeight, RDF.type, OWL.Class))
        graph.add((edo.GrooveHeight, RDFS.subClassOf, edo.DomainAttribute))
        graph.add((edo.GrooveHeight, DCTERMS.identifier, Literal("GrooveHeight")))
        graph.add((edo.GrooveHeight, SKOS.prefLabel, Literal("Groove Height", lang="en")))
        graph.add((edo.GrooveHeight, SKOS.prefLabel, Literal("Altura do Groove", lang="pt-br")))
        graph.add((edo.GrooveHeight, SKOS.definition, Literal(
            "The vertical dimension of a groove.", lang="en"
        )))
        graph.add((edo.GrooveHeight, SKOS.definition, Literal(
            "A dimensão vertical de um groove.", lang="pt-br"
        )))

        # Serializar
        result = serialize_protege_style(graph)
        
        # Carregar golden
        golden_path = FIXTURES_DIR / "protege_grooveheight.ttl"
        golden = golden_path.read_text(encoding="utf-8")

        # Comparar
        assert self._normalize_ttl(result) == self._normalize_ttl(golden), \
            f"Output não corresponde ao golden:\n---RESULTADO---\n{result}\n---GOLDEN---\n{golden}"

    def test_groovepoint_snapshot(self, edo_namespace):
        """
        Testa que GroovePoint é serializado exatamente como o golden.
        """
        edo = edo_namespace
        graph = self._create_base_graph(edo)

        # Adicionar triplas programaticamente
        graph.add((edo.GroovePoint, RDF.type, OWL.Class))
        graph.add((edo.GroovePoint, RDFS.subClassOf, edo.DomainElement))
        graph.add((edo.GroovePoint, DCTERMS.identifier, Literal("GroovePoint")))
        graph.add((edo.GroovePoint, SKOS.prefLabel, Literal("Groove Point", lang="en")))
        graph.add((edo.GroovePoint, SKOS.prefLabel, Literal("Ponto do Groove", lang="pt-br")))
        graph.add((edo.GroovePoint, SKOS.definition, Literal(
            "A reference point on a groove structure.", lang="en"
        )))
        graph.add((edo.GroovePoint, SKOS.definition, Literal(
            "Um ponto de referência em uma estrutura de groove.", lang="pt-br"
        )))
        # hasAttribute com múltiplos objetos
        graph.add((edo.GroovePoint, edo.hasAttribute, edo.GrooveHeight))
        graph.add((edo.GroovePoint, edo.hasAttribute, edo.GrooveMinimumSupportArea))
        graph.add((edo.GroovePoint, edo.hasAttribute, edo.GrooveWidth))

        # Serializar
        result = serialize_protege_style(graph)
        
        # Carregar golden
        golden_path = FIXTURES_DIR / "protege_groovepoint.ttl"
        golden = golden_path.read_text(encoding="utf-8")

        # Comparar
        assert self._normalize_ttl(result) == self._normalize_ttl(golden), \
            f"Output não corresponde ao golden:\n---RESULTADO---\n{result}\n---GOLDEN---\n{golden}"


class TestSerializerDeterminism:
    """Testes para garantir que a serialização é determinística."""

    @pytest.fixture
    def sample_graph(self):
        """Cria grafo de exemplo para testes."""
        edo = Namespace("https://w3id.org/energy-domain/edo#")
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        
        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.label, Literal("Test", lang="en")))
        
        return graph

    def test_multiple_serializations_identical(self, sample_graph):
        """
        Testa que múltiplas serializações produzem output idêntico.
        """
        results = [serialize_protege_style(sample_graph) for _ in range(5)]
        
        assert all(r == results[0] for r in results), \
            "Serializações não são idênticas"

    def test_different_triple_order_same_output(self):
        """
        Testa que triplas adicionadas em ordem diferente produzem mesmo output.
        """
        edo = Namespace("https://w3id.org/energy-domain/edo#")
        
        # Grafo 1 - triplas em uma ordem
        graph1 = Graph()
        graph1.bind("edo", edo)
        graph1.bind("owl", OWL)
        graph1.bind("rdf", RDF)
        graph1.add((edo.ClassB, RDF.type, OWL.Class))
        graph1.add((edo.ClassA, RDF.type, OWL.Class))
        graph1.add((edo.ClassC, RDF.type, OWL.Class))
        
        # Grafo 2 - mesmas triplas em ordem diferente
        graph2 = Graph()
        graph2.bind("edo", edo)
        graph2.bind("owl", OWL)
        graph2.bind("rdf", RDF)
        graph2.add((edo.ClassA, RDF.type, OWL.Class))
        graph2.add((edo.ClassC, RDF.type, OWL.Class))
        graph2.add((edo.ClassB, RDF.type, OWL.Class))
        
        result1 = serialize_protege_style(graph1)
        result2 = serialize_protege_style(graph2)
        
        assert result1 == result2, \
            f"Outputs diferem:\n---G1---\n{result1}\n---G2---\n{result2}"
