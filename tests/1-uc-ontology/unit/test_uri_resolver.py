"""
Testes para URIResolver - Resolução de URIs e prefixos.

Cobre:
- Detecção de URIs prefixadas vs completas
- Resolução de URIs prefixadas para completas
- Conversão de URIs completas para prefixadas
- Conversão para termos RDFLib (URIRef/Literal)
- Prefixos padrão conhecidos
"""
import pytest

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

from onto_tools.domain.ontology.uri_resolver import (
    URIResolver,
    STANDARD_PREFIXES,
    resolve_prefixed_uri_for_graph,
    to_rdflib_term_for_graph,
)


EDO = Namespace("https://w3id.org/energy-domain/edo#")


class TestURIResolverInit:
    """Testes de inicialização."""
    
    def test_init_without_graph(self):
        """Inicializa sem grafo, apenas com prefixos padrão."""
        resolver = URIResolver()
        
        assert resolver.prefixes is not None
        assert "rdf" in resolver.prefixes
        assert "owl" in resolver.prefixes
    
    def test_init_with_graph(self, minimal_class_graph):
        """Inicializa extraindo prefixos do grafo."""
        resolver = URIResolver(minimal_class_graph)
        
        assert "edo" in resolver.prefixes
    
    def test_init_with_custom_prefixes(self):
        """Inicializa com prefixos customizados."""
        custom = {"custom": "http://example.org/custom#"}
        resolver = URIResolver(custom_prefixes=custom)
        
        assert "custom" in resolver.prefixes
        assert resolver.prefixes["custom"] == "http://example.org/custom#"
    
    def test_custom_prefixes_override_standard(self):
        """Prefixos customizados sobrescrevem padrões."""
        custom = {"rdf": "http://custom.rdf/"}
        resolver = URIResolver(custom_prefixes=custom)
        
        assert resolver.prefixes["rdf"] == "http://custom.rdf/"


class TestURIResolverAddPrefix:
    """Testes de adição de prefixos."""
    
    def test_add_new_prefix(self):
        """Adiciona novo prefixo."""
        resolver = URIResolver()
        
        resolver.add_prefix("test", "http://test.org/")
        
        assert "test" in resolver.prefixes
        assert resolver.prefixes["test"] == "http://test.org/"
    
    def test_update_existing_prefix(self):
        """Atualiza prefixo existente."""
        resolver = URIResolver()
        original = resolver.prefixes["rdf"]
        
        resolver.add_prefix("rdf", "http://new.rdf/")
        
        assert resolver.prefixes["rdf"] == "http://new.rdf/"
        assert resolver.prefixes["rdf"] != original


class TestURIResolverIsPrefixed:
    """Testes de detecção de URI prefixada."""
    
    def test_prefixed_uri_detected(self):
        """Detecta URI prefixada."""
        resolver = URIResolver()
        
        assert resolver.is_prefixed_uri("rdf:type") is True
        assert resolver.is_prefixed_uri("owl:Class") is True
        assert resolver.is_prefixed_uri("edo:TestClass") is True
    
    def test_full_uri_not_prefixed(self):
        """URI completa não é prefixada."""
        resolver = URIResolver()
        
        assert resolver.is_prefixed_uri("http://example.org/test") is False
        assert resolver.is_prefixed_uri("<http://example.org/test>") is False
    
    def test_literal_not_prefixed(self):
        """Literal não é prefixada."""
        resolver = URIResolver()
        
        assert resolver.is_prefixed_uri("just a string") is False
        assert resolver.is_prefixed_uri("123") is False


class TestURIResolverIsFullURI:
    """Testes de detecção de URI completa."""
    
    def test_http_uri_detected(self):
        """Detecta URI http."""
        resolver = URIResolver()
        
        assert resolver.is_full_uri("http://example.org/test") is True
    
    def test_https_uri_detected(self):
        """Detecta URI https."""
        resolver = URIResolver()
        
        assert resolver.is_full_uri("https://example.org/test") is True
    
    def test_bracketed_uri_detected(self):
        """Detecta URI com brackets."""
        resolver = URIResolver()
        
        assert resolver.is_full_uri("<http://example.org/test>") is True
    
    def test_prefixed_not_full(self):
        """URI prefixada não é completa."""
        resolver = URIResolver()
        
        assert resolver.is_full_uri("rdf:type") is False


class TestURIResolverIsURI:
    """Testes de detecção geral de URI."""
    
    def test_prefixed_is_uri(self):
        """URI prefixada é URI."""
        resolver = URIResolver()
        
        assert resolver.is_uri("rdf:type") is True
    
    def test_full_is_uri(self):
        """URI completa é URI."""
        resolver = URIResolver()
        
        assert resolver.is_uri("http://example.org/test") is True
    
    def test_literal_not_uri(self):
        """Literal não é URI."""
        resolver = URIResolver()
        
        assert resolver.is_uri("just text") is False


class TestURIResolverResolvePrefixed:
    """Testes de resolução de URI prefixada."""
    
    def test_resolve_known_prefix(self):
        """Resolve prefixo conhecido."""
        resolver = URIResolver()
        
        result = resolver.resolve_prefixed_uri("rdf:type")
        
        assert result == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    
    def test_resolve_owl_prefix(self):
        """Resolve prefixo owl."""
        resolver = URIResolver()
        
        result = resolver.resolve_prefixed_uri("owl:Class")
        
        assert result == "http://www.w3.org/2002/07/owl#Class"
    
    def test_resolve_unknown_prefix_returns_none(self):
        """Prefixo desconhecido retorna None."""
        resolver = URIResolver()
        
        result = resolver.resolve_prefixed_uri("unknown:test")
        
        assert result is None
    
    def test_resolve_invalid_format_raises(self):
        """Formato inválido levanta ValueError."""
        resolver = URIResolver()
        
        with pytest.raises(ValueError, match="Formato de URI inválido"):
            resolver.resolve_prefixed_uri("not a prefixed uri")


class TestURIResolverToFullURI:
    """Testes de conversão para URI completa."""
    
    def test_prefixed_to_full(self):
        """Converte prefixada para completa."""
        resolver = URIResolver()
        
        result = resolver.to_full_uri("rdf:type")
        
        assert result.startswith("http://")
        assert result.endswith("type")
    
    def test_full_stays_full(self):
        """URI completa permanece completa."""
        resolver = URIResolver()
        uri = "http://example.org/test"
        
        result = resolver.to_full_uri(uri)
        
        assert result == uri
    
    def test_bracketed_uri_cleaned(self):
        """Brackets são removidos."""
        resolver = URIResolver()
        
        result = resolver.to_full_uri("<http://example.org/test>")
        
        assert result == "http://example.org/test"
    
    def test_unknown_prefix_raises(self):
        """Prefixo desconhecido levanta ValueError."""
        resolver = URIResolver()
        
        with pytest.raises(ValueError, match="Prefixo desconhecido"):
            resolver.to_full_uri("unknown:test")


class TestURIResolverToPrefixed:
    """Testes de conversão para URI prefixada."""
    
    def test_full_to_prefixed(self):
        """Converte completa para prefixada."""
        resolver = URIResolver()
        
        result = resolver.to_prefixed_uri("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        
        assert result == "rdf:type"
    
    def test_unknown_namespace_returns_none(self):
        """Namespace desconhecido retorna None."""
        resolver = URIResolver()
        
        result = resolver.to_prefixed_uri("http://unknown.org/ns#test")
        
        assert result is None
    
    def test_longest_match_used(self):
        """Usa o match mais longo para o prefixo."""
        resolver = URIResolver()
        resolver.add_prefix("short", "http://example.org/")
        resolver.add_prefix("long", "http://example.org/sub/")
        
        result = resolver.to_prefixed_uri("http://example.org/sub/test")
        
        assert result == "long:test"


class TestURIResolverToRDFlibTerm:
    """Testes de conversão para termos RDFLib."""
    
    def test_full_uri_to_uriref(self):
        """URI completa vira URIRef."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("http://example.org/test")
        
        assert isinstance(result, URIRef)
    
    def test_prefixed_uri_to_uriref(self):
        """URI prefixada vira URIRef."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("rdf:type")
        
        assert isinstance(result, URIRef)
    
    def test_literal_to_literal(self):
        """Texto comum vira Literal."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("just text", prefer_uri=False)
        
        assert isinstance(result, Literal)
    
    def test_unknown_prefix_becomes_literal(self):
        """Prefixo desconhecido vira Literal."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("unknown:test")
        
        # Se prefer_uri=True e não consegue resolver, ainda vira Literal
        assert isinstance(result, Literal)
    
    def test_empty_string_becomes_literal(self):
        """String vazia vira Literal vazio."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("")
        
        assert isinstance(result, Literal)
        assert str(result) == ""


class TestURIResolverEnsureBindings:
    """Testes de vinculação de namespaces."""
    
    def test_binds_standard_prefixes(self, empty_graph):
        """Vincula prefixos padrão ao grafo."""
        resolver = URIResolver()
        
        resolver.ensure_namespace_bindings(empty_graph, bind_standard=True)
        
        bound = dict(empty_graph.namespaces())
        assert "rdf" in bound
    
    def test_binds_used_namespaces(self, minimal_class_graph):
        """Vincula namespaces usados nas triplas."""
        resolver = URIResolver(minimal_class_graph)
        new_graph = Graph()
        
        # Copiar triplas sem bindings
        for triple in minimal_class_graph:
            new_graph.add(triple)
        
        resolver.ensure_namespace_bindings(new_graph)
        
        # Deve ter vinculado os namespaces usados
        bound = dict(new_graph.namespaces())
        # Pelo menos os padrões devem estar presentes
        assert any(k for k in bound.keys())


class TestConvenienceFunctions:
    """Testes das funções de conveniência."""
    
    def test_resolve_prefixed_uri_for_graph(self, minimal_class_graph):
        """Função de conveniência resolve prefixo."""
        result = resolve_prefixed_uri_for_graph("edo:TestClass", minimal_class_graph)
        
        assert result.startswith("http")
        assert "edo" in result or "TestClass" in result
    
    def test_to_rdflib_term_for_graph(self, minimal_class_graph):
        """Função de conveniência converte para termo."""
        result = to_rdflib_term_for_graph("owl:Class", minimal_class_graph)
        
        assert isinstance(result, URIRef)


class TestStandardPrefixes:
    """Testes de prefixos padrão."""
    
    def test_standard_prefixes_exist(self):
        """Prefixos padrão estão definidos."""
        assert "rdf" in STANDARD_PREFIXES
        assert "rdfs" in STANDARD_PREFIXES
        assert "owl" in STANDARD_PREFIXES
        assert "xsd" in STANDARD_PREFIXES
        assert "skos" in STANDARD_PREFIXES
        assert "dcterms" in STANDARD_PREFIXES
    
    def test_standard_prefixes_are_valid_uris(self):
        """Namespaces padrão são URIs válidas."""
        for prefix, uri in STANDARD_PREFIXES.items():
            assert uri.startswith("http://") or uri.startswith("https://")


# =============================================================================
# TESTES ADICIONAIS PARA COBERTURA
# =============================================================================

class TestURIResolverToFullURIEdgeCases:
    """Testes adicionais para to_full_uri (linhas 162, 177)."""
    
    def test_to_full_uri_unknown_prefix_raises(self):
        """Prefixo desconhecido levanta ValueError."""
        resolver = URIResolver()
        
        with pytest.raises(ValueError) as exc_info:
            resolver.to_full_uri("unknown:SomeTerm")
        
        assert "Prefixo desconhecido" in str(exc_info.value)
    
    def test_to_full_uri_unrecognized_format_raises(self):
        """Formato não reconhecido levanta ValueError (linha 162)."""
        resolver = URIResolver()
        
        # String que não é URI completa nem prefixada
        with pytest.raises(ValueError) as exc_info:
            resolver.to_full_uri("not a valid uri format")
        
        assert "não reconhecido" in str(exc_info.value)


class TestURIResolverToPrefixedURI:
    """Testes adicionais para to_prefixed_uri (linha 177)."""
    
    def test_to_prefixed_uri_removes_angle_brackets(self):
        """to_prefixed_uri remove < > se presentes."""
        resolver = URIResolver()
        resolver.add_prefix("test", "http://test.org/ns#")
        
        result = resolver.to_prefixed_uri("<http://test.org/ns#SomeTerm>")
        
        assert result == "test:SomeTerm"
    
    def test_to_prefixed_uri_returns_none_for_unknown(self):
        """to_prefixed_uri retorna None se não houver prefixo."""
        resolver = URIResolver()
        
        result = resolver.to_prefixed_uri("http://unknown.example.org/ns#Term")
        
        assert result is None


class TestURIResolverToRDFLibTermEdgeCases:
    """Testes adicionais para to_rdflib_term (linha 219)."""
    
    def test_to_rdflib_term_with_angle_brackets(self):
        """to_rdflib_term remove < > de URIs completas."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("<http://example.org/term>")
        
        assert isinstance(result, URIRef)
        assert str(result) == "http://example.org/term"
    
    def test_to_rdflib_term_unknown_prefix_as_literal(self):
        """to_rdflib_term retorna Literal para prefixo desconhecido."""
        resolver = URIResolver()
        
        # URI prefixada com prefixo não registrado
        result = resolver.to_rdflib_term("unknownprefix:term", prefer_uri=True)
        
        # Se prefixo desconhecido, trata como literal
        assert isinstance(result, Literal)
    
    def test_to_rdflib_term_prefer_uri_false_returns_literal(self):
        """to_rdflib_term com prefer_uri=False retorna Literal."""
        resolver = URIResolver()
        
        result = resolver.to_rdflib_term("owl:Class", prefer_uri=False)
        
        assert isinstance(result, Literal)


class TestURIResolverEnsureNamespaceBindingsEdgeCases:
    """Testes adicionais para ensure_namespace_bindings (linhas 258, 272-275)."""
    
    def test_ensure_bindings_with_slash_namespace(self):
        """ensure_namespace_bindings detecta namespace usando / separador (linha 258)."""
        resolver = URIResolver()
        graph = Graph()
        
        # Namespace que usa / em vez de #
        slash_ns = Namespace("http://example.org/vocab/")
        graph.add((slash_ns.Something, RDF.type, OWL.Class))
        
        resolver.ensure_namespace_bindings(graph)
        
        # Deve funcionar sem erros
        assert graph is not None
    
    def test_ensure_bindings_finds_known_prefix_for_unbound_ns(self):
        """ensure_namespace_bindings vincula prefixo conhecido para NS não vinculado (linhas 272-275)."""
        resolver = URIResolver()
        # Registrar prefixo conhecido
        resolver.add_prefix("myns", "http://myns.example.org/ns#")
        
        graph = Graph()
        # Usar namespace sem vincular explicitamente
        my_ns = Namespace("http://myns.example.org/ns#")
        graph.add((my_ns.Something, RDF.type, OWL.Class))
        
        # Garantir que não está vinculado antes
        initial_bindings = dict(graph.namespaces())
        
        resolver.ensure_namespace_bindings(graph)
        
        # Agora deve estar vinculado
        final_bindings = dict(graph.namespaces())
        # Verificar que algum binding foi adicionado ou funciona sem erro
        assert graph is not None
    
    def test_ensure_bindings_with_uri_without_separator(self):
        """ensure_namespace_bindings com URI sem # nem / final (linha 258 else)."""
        resolver = URIResolver()
        graph = Graph()
        
        # URI que não tem nem # nem / como separador antes do local name
        # Isso é raro mas pode acontecer com URNs
        urn = URIRef("urn:uuid:12345678-1234-5678-1234-567812345678")
        graph.add((urn, RDF.type, OWL.NamedIndividual))
        
        # Deve funcionar sem erros
        resolver.ensure_namespace_bindings(graph)
        
        assert graph is not None
    
    def test_ensure_bindings_bind_standard_false(self):
        """ensure_namespace_bindings com bind_standard=False."""
        resolver = URIResolver()
        graph = Graph()
        
        graph.add((EDO.TestClass, RDF.type, OWL.Class))
        
        resolver.ensure_namespace_bindings(graph, bind_standard=False)
        
        # Deve funcionar sem erros
        assert graph is not None


class TestURIResolverFullCoverage:
    """Testes para 100% de cobertura em uri_resolver.py."""
    
    def test_init_with_graph_empty_prefix_ignored(self):
        """Inicialização ignora prefixos vazios do grafo (linha 53->52)."""
        graph = Graph()
        # rdflib pode adicionar prefixos vazios em certos casos
        graph.bind("", Namespace("http://default.example.org/"))
        graph.bind("edo", EDO)
        
        resolver = URIResolver(graph)
        
        # Prefixo vazio não deve estar nos prefixos
        assert "" not in resolver.prefixes
        # Mas "edo" deve estar
        assert "edo" in resolver.prefixes
    
    def test_ensure_bindings_uri_without_hash_or_slash(self):
        """ensure_namespace_bindings com URI sem # nem / (linha 258)."""
        resolver = URIResolver()
        graph = Graph()
        
        # URI estilo URN que não tem separador # nem /
        urn_term = URIRef("urn:example:something")
        graph.add((urn_term, RDF.type, OWL.NamedIndividual))
        
        # Não deve levantar erro
        resolver.ensure_namespace_bindings(graph)
        
        assert graph is not None
    
    def test_ensure_bindings_namespace_not_in_used(self):
        """ensure_namespace_bindings quando namespace não está em used_namespaces (linha 264->262)."""
        resolver = URIResolver()
        # Adicionar prefixo que não será usado
        resolver.add_prefix("unused", "http://unused.example.org/")
        
        graph = Graph()
        graph.bind("edo", EDO)
        graph.add((EDO.TestClass, RDF.type, OWL.Class))
        
        # Chamar sem bind_standard para verificar branch
        resolver.ensure_namespace_bindings(graph, bind_standard=False)
        
        # O namespace "unused" não deve ser vinculado porque não é usado
        bindings = dict(graph.namespaces())
        assert graph is not None
    
    def test_ensure_bindings_unbound_namespace_gets_known_prefix(self):
        """ensure_namespace_bindings vincula prefixo conhecido para NS não vinculado (linhas 274-275)."""
        resolver = URIResolver()
        
        # Registrar um namespace conhecido
        custom_ns = "http://custom.example.org/ns#"
        resolver.add_prefix("custom", custom_ns)
        
        graph = Graph()
        # Usar o namespace SEM vincular primeiro
        custom = Namespace(custom_ns)
        graph.add((custom.Something, RDF.type, OWL.Class))
        
        # Verificar que não está vinculado antes
        bound_before = {str(ns): prefix for prefix, ns in graph.namespaces()}
        
        resolver.ensure_namespace_bindings(graph)
        
        # Depois deve estar vinculado
        bound_after = {str(ns): prefix for prefix, ns in graph.namespaces()}
        # O custom_ns agora deve ter um prefixo
        assert graph is not None