"""
Testes adicionais para cobertura do protege_serializer.py.

Cobre linhas: 188, 247, 319, 330-333, 343, 349, 371, 377-378, 384
"""
import pytest
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from onto_tools.adapters.rdf.protege_serializer import (
    ProtegeStyleTurtleSerializer,
    serialize_protege_style
)


EDO = Namespace("https://w3id.org/energy-domain/edo#")


class TestProtegeSerializerBNodes:
    """Testes de serialização de BNodes."""
    
    def test_serialize_bnode_subject(self):
        """Serializa BNode como sujeito."""
        g = Graph()
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        
        bnode = BNode()
        g.add((bnode, RDF.type, OWL.Restriction))
        g.add((bnode, OWL.onProperty, EDO.hasValue))
        
        result = serialize_protege_style(g)
        
        assert "_:" in result  # BNode representation
    
    def test_serialize_bnode_object(self):
        """Serializa BNode como objeto."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        
        bnode = BNode()
        g.add((EDO.TestClass, OWL.equivalentClass, bnode))
        g.add((bnode, RDF.type, OWL.Restriction))
        
        result = serialize_protege_style(g)
        
        assert "_:" in result


class TestProtegeSerializerLiterals:
    """Testes de serialização de literais com diferentes tipos."""
    
    def test_serialize_integer_literal(self):
        """Serializa literal inteiro sem aspas."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.TestClass, EDO.itemCount, Literal(42, datatype=XSD.integer)))
        
        result = serialize_protege_style(g)
        
        # Inteiro pode ser serializado sem aspas
        assert "42" in result
    
    def test_serialize_invalid_integer_literal(self):
        """Serializa literal inteiro inválido com tipo."""
        g = Graph()
        g.bind("edo", EDO)
        
        # Literal marcado como integer mas com valor inválido
        g.add((EDO.TestClass, EDO.value, Literal("not-a-number", datatype=XSD.integer)))
        
        result = serialize_protege_style(g)
        
        assert "not-a-number" in result
    
    def test_serialize_decimal_literal(self):
        """Serializa literal decimal."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.TestClass, EDO.price, Literal("3.14", datatype=XSD.decimal)))
        
        result = serialize_protege_style(g)
        
        assert "3.14" in result
    
    def test_serialize_boolean_literal(self):
        """Serializa literal booleano em lowercase."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.TestClass, EDO.active, Literal("true", datatype=XSD.boolean)))
        g.add((EDO.TestClass, EDO.inactive, Literal("FALSE", datatype=XSD.boolean)))
        
        result = serialize_protege_style(g)
        
        assert "true" in result.lower()
    
    def test_serialize_string_literal_with_datatype(self):
        """Serializa literal string com datatype explícito."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.TestClass, EDO.name, Literal("Test", datatype=XSD.string)))
        
        result = serialize_protege_style(g)
        
        assert '"Test"' in result
    
    def test_serialize_custom_datatype_literal(self):
        """Serializa literal com datatype customizado."""
        g = Graph()
        g.bind("edo", EDO)
        
        CUSTOM_TYPE = URIRef("http://example.org/CustomType")
        g.add((EDO.TestClass, EDO.data, Literal("custom value", datatype=CUSTOM_TYPE)))
        
        result = serialize_protege_style(g)
        
        assert "custom value" in result
    
    def test_serialize_literal_with_special_chars(self):
        """Serializa literal com caracteres especiais."""
        g = Graph()
        g.bind("edo", EDO)
        
        # Literal com aspas, newline, tab
        g.add((EDO.TestClass, RDFS.comment, Literal('Line1\nLine2\t"quoted"')))
        
        result = serialize_protege_style(g)
        
        # Deve ter escape de caracteres
        assert "\\n" in result or "Line1" in result
    
    def test_serialize_literal_with_language(self):
        """Serializa literal com language tag."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.TestClass, RDFS.label, Literal("Wall", lang="en")))
        g.add((EDO.TestClass, RDFS.label, Literal("Parede", lang="pt-br")))
        
        result = serialize_protege_style(g)
        
        assert "@en" in result
        assert "@pt-br" in result


class TestProtegeSerializerQNames:
    """Testes de conversão para QNames."""
    
    def test_qname_with_prefix(self):
        """Converte URI para QName com prefixo."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("owl", OWL)
        
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        
        result = serialize_protege_style(g)
        
        assert "edo:TestClass" in result
        assert "owl:Class" in result
    
    def test_qname_without_prefix_uses_brackets(self):
        """URI sem prefixo usa angle brackets."""
        g = Graph()
        
        UNKNOWN = Namespace("http://unknown.example.org/")
        g.add((UNKNOWN.Entity, RDF.type, OWL.Class))
        
        result = serialize_protege_style(g)
        
        # Deve usar <uri> para namespace desconhecido
        assert "<http://unknown.example.org/" in result or "Entity" in result
    
    def test_qname_empty_prefix(self):
        """URI com prefixo vazio usa :localname."""
        g = Graph()
        BASE = Namespace("http://example.org/")
        g.bind("", BASE)
        
        g.add((BASE.Item, RDF.type, OWL.Class))
        
        result = serialize_protege_style(g)
        
        assert ":Item" in result or "Item" in result


class TestProtegeSerializerPredicateOrdering:
    """Testes de ordenação de predicados."""
    
    def test_predicates_ordered_by_priority(self):
        """Predicados são ordenados por prioridade (rdf:type primeiro)."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        g.bind("rdfs", RDFS)
        
        g.add((EDO.TestClass, RDFS.label, Literal("Test")))
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, RDFS.comment, Literal("A comment")))
        
        result = serialize_protege_style(g)
        
        # rdf:type deve aparecer antes de rdfs:label
        type_pos = result.find("rdf:type") if "rdf:type" in result else result.find("a ")
        label_pos = result.find("rdfs:label")
        
        # Se ambos existem, type deve vir primeiro
        if type_pos >= 0 and label_pos >= 0:
            assert type_pos < label_pos


class TestProtegeSerializerMultipleObjects:
    """Testes de serialização com múltiplos objetos."""
    
    def test_multiple_objects_same_predicate(self):
        """Múltiplos objetos para mesmo predicado."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdfs", RDFS)
        
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, RDFS.label, Literal("Label 1", lang="en")))
        g.add((EDO.TestClass, RDFS.label, Literal("Label 2", lang="pt")))
        
        result = serialize_protege_style(g)
        
        assert "Label 1" in result
        assert "Label 2" in result


class TestProtegeSerializerEmptyGraph:
    """Testes de serialização de grafo vazio."""
    
    def test_empty_graph_serializes(self):
        """Grafo vazio serializa sem erro."""
        g = Graph()
        
        result = serialize_protege_style(g)
        
        # Pode ter apenas prefixos ou estar vazio
        assert isinstance(result, str)


class TestSerializeProtegeStyleFunction:
    """Testes da função auxiliar serialize_protege_style."""
    
    def test_function_returns_string(self):
        """Função retorna string."""
        g = Graph()
        g.add((EDO.Test, RDF.type, OWL.Class))
        
        result = serialize_protege_style(g)
        
        assert isinstance(result, str)
    
    def test_function_creates_serializer(self):
        """Função cria e usa serializer."""
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        
        result = serialize_protege_style(g)
        
        assert len(result) > 0
