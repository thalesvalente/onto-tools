"""
Testes de validade e idempotência para o serializador estilo Protégé.

Verifica que:
- O TTL gerado é válido e pode ser parseado
- A serialização é idempotente (re-serializar produz mesmo resultado)
- O grafo semanticamente não muda após serialização
"""
import pytest
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, DCTERMS, XSD
from rdflib.compare import isomorphic

from onto_tools.adapters.rdf.protege_serializer import (
    ProtegeStyleTurtleSerializer,
    serialize_protege_style,
)


class TestTurtleValidity:
    """Testes para verificar que o TTL gerado é válido."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        graph.bind("xsd", XSD)
        return graph

    def test_serialized_ttl_can_be_parsed(self, edo_namespace):
        """
        Testa que o TTL gerado pode ser parseado de volta para um grafo.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.ParentClass))
        graph.add((edo.TestClass, DCTERMS.identifier, Literal("TestClass")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Classe de Teste", lang="pt-br")))
        graph.add((edo.TestClass, SKOS.definition, Literal("A test class.", lang="en")))

        # Serializar
        ttl_content = serialize_protege_style(graph)

        # Parsear de volta
        parsed_graph = Graph()
        try:
            parsed_graph.parse(data=ttl_content, format="turtle")
        except Exception as e:
            pytest.fail(f"Falha ao parsear TTL gerado: {e}\n\nConteúdo:\n{ttl_content}")

        # Deve ter o mesmo número de triplas
        assert len(parsed_graph) == len(graph), \
            f"Número de triplas diferente: original={len(graph)}, parsed={len(parsed_graph)}"

    def test_parsed_graph_is_isomorphic(self, edo_namespace):
        """
        Testa que o grafo parseado é isomórfico ao original.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.ParentClass))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test", lang="en")))

        # Serializar
        ttl_content = serialize_protege_style(graph)

        # Parsear de volta
        parsed_graph = Graph()
        parsed_graph.parse(data=ttl_content, format="turtle")

        # Grafos devem ser isomórficos (mesmas triplas, semanticamente)
        assert isomorphic(graph, parsed_graph), \
            "Grafo parseado não é isomórfico ao original"

    def test_complex_graph_remains_valid(self, edo_namespace):
        """
        Testa grafo complexo com múltiplos tipos de literais.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        # Vários tipos de literais
        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.label, Literal("Test")))  # Sem lang
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Teste", lang="pt-br")))
        graph.add((edo.TestClass, edo.hasCount, Literal(42, datatype=XSD.integer)))
        graph.add((edo.TestClass, edo.isActive, Literal(True, datatype=XSD.boolean)))
        graph.add((edo.TestClass, edo.ratio, Literal("3.14", datatype=XSD.decimal)))

        # Múltiplos sujeitos
        graph.add((edo.OtherClass, RDF.type, OWL.Class))
        graph.add((edo.OtherClass, RDFS.subClassOf, edo.TestClass))

        # Serializar
        ttl_content = serialize_protege_style(graph)

        # Parsear de volta
        parsed_graph = Graph()
        try:
            parsed_graph.parse(data=ttl_content, format="turtle")
        except Exception as e:
            pytest.fail(f"Falha ao parsear TTL complexo: {e}\n\nConteúdo:\n{ttl_content}")

        assert isomorphic(graph, parsed_graph), \
            "Grafo complexo não é isomórfico após round-trip"


class TestIdempotence:
    """Testes de idempotência da serialização."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        return graph

    def test_serialize_parse_serialize_is_identical(self, edo_namespace):
        """
        Testa que serializar → parsear → serializar produz output idêntico.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.ParentClass))
        graph.add((edo.TestClass, DCTERMS.identifier, Literal("TestClass")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Classe de Teste", lang="pt-br")))

        # Primeira serialização
        ttl1 = serialize_protege_style(graph)

        # Parsear
        graph2 = Graph()
        graph2.parse(data=ttl1, format="turtle")
        
        # Re-bind prefixos (pode ser necessário para consistência)
        graph2.bind("edo", edo)
        graph2.bind("owl", OWL)
        graph2.bind("rdf", RDF)
        graph2.bind("rdfs", RDFS)
        graph2.bind("skos", SKOS)
        graph2.bind("dcterms", DCTERMS)

        # Segunda serialização
        ttl2 = serialize_protege_style(graph2)

        assert ttl1 == ttl2, \
            f"Serialização não é idempotente:\n---PRIMEIRA---\n{ttl1}\n---SEGUNDA---\n{ttl2}"

    def test_multiple_serializations_identical(self, edo_namespace):
        """
        Testa que múltiplas serializações do mesmo grafo são idênticas.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Teste", lang="pt-br")))

        # Serializar várias vezes
        results = [serialize_protege_style(graph) for _ in range(10)]

        # Todas devem ser idênticas
        first = results[0]
        for i, result in enumerate(results[1:], start=2):
            assert result == first, \
                f"Serialização {i} difere da primeira"


class TestSemanticPreservation:
    """Testes para garantir que a semântica é preservada."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        return graph

    def test_no_triple_loss_or_addition(self, edo_namespace):
        """
        Testa que nenhuma tripla é perdida ou adicionada.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        # Adicionar triplas conhecidas
        expected_triples = [
            (edo.TestClass, RDF.type, OWL.Class),
            (edo.TestClass, RDFS.subClassOf, edo.ParentClass),
            (edo.TestClass, DCTERMS.identifier, Literal("TestClass")),
            (edo.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")),
        ]
        
        for triple in expected_triples:
            graph.add(triple)

        # Serializar e parsear
        ttl = serialize_protege_style(graph)
        parsed = Graph()
        parsed.parse(data=ttl, format="turtle")

        # Verificar que todas as triplas originais existem
        for triple in expected_triples:
            assert triple in parsed, \
                f"Tripla perdida: {triple}"

        # Verificar que não há triplas extras
        assert len(parsed) == len(expected_triples), \
            f"Número de triplas diferente: esperado={len(expected_triples)}, atual={len(parsed)}"

    def test_literal_types_preserved(self, edo_namespace):
        """
        Testa que tipos de literais são preservados.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)
        graph.bind("xsd", XSD)

        # Diferentes tipos de literais
        graph.add((edo.Test, edo.intValue, Literal(42, datatype=XSD.integer)))
        graph.add((edo.Test, edo.boolValue, Literal(True, datatype=XSD.boolean)))
        graph.add((edo.Test, edo.stringValue, Literal("hello")))
        graph.add((edo.Test, edo.langValue, Literal("world", lang="en")))

        ttl = serialize_protege_style(graph)
        parsed = Graph()
        parsed.parse(data=ttl, format="turtle")

        # Verificar tipos
        for s, p, o in parsed:
            if p == edo.intValue:
                assert o.datatype == XSD.integer, f"Integer type perdido: {o}"
            elif p == edo.boolValue:
                assert o.datatype == XSD.boolean, f"Boolean type perdido: {o}"
            elif p == edo.langValue:
                assert o.language == "en", f"Language tag perdido: {o}"

    def test_uris_not_converted_to_literals(self, edo_namespace):
        """
        Testa que URIs não são convertidas para literais.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.ParentClass))

        ttl = serialize_protege_style(graph)
        parsed = Graph()
        parsed.parse(data=ttl, format="turtle")

        # Verificar que objetos URI ainda são URI
        for s, p, o in parsed:
            if p == RDF.type:
                assert isinstance(o, URIRef), \
                    f"rdf:type object deve ser URIRef, não {type(o)}"
            if p == RDFS.subClassOf:
                assert isinstance(o, URIRef), \
                    f"rdfs:subClassOf object deve ser URIRef, não {type(o)}"
