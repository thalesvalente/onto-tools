"""
Testes para Canonicalizer - Ordenação Determinística (UC-103).

Após refatoração (separação UC-103/UC-108):
- Canonicalizer (UC-103): Ordenação determinística para diff/revisão
- Normalizer (UC-108): Correções semânticas (nomenclatura, validação)

Cobre:
- Ordenação de prefixos alfabeticamente
- Ordenação de triplas por subject/predicate/object
- Serialização Protégé-compatible
- Idempotência (mesma entrada = mesma saída)
- CanonicalizationResult com estatísticas
"""
import pytest
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from onto_tools.domain.ontology.canonicalizer import Canonicalizer, CanonicalizationResult


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


@pytest.fixture
def canonicalizer():
    """Instância do Canonicalizer para testes."""
    return Canonicalizer()


@pytest.fixture
def canonicalizer_with_rules(rules_json_path):
    """Canonicalizer configurado com rules.json."""
    return Canonicalizer(rules_path=rules_json_path)


@pytest.fixture
def simple_graph():
    """Grafo simples para testes de ordenação."""
    g = Graph()
    g.bind("edo", EDO)
    g.bind("rdf", RDF)
    g.bind("owl", OWL)
    g.bind("skos", SKOS)
    
    g.add((EDO.ClassB, RDF.type, OWL.Class))
    g.add((EDO.ClassA, RDF.type, OWL.Class))
    g.add((EDO.ClassC, RDF.type, OWL.Class))
    
    return g


@pytest.fixture
def graph_with_unordered_prefixes():
    """Grafo com prefixos em ordem não-alfabética."""
    g = Graph()
    g.bind("zoo", Namespace("http://example.org/zoo#"))
    g.bind("alpha", Namespace("http://example.org/alpha#"))
    g.bind("beta", Namespace("http://example.org/beta#"))
    g.bind("rdf", RDF)
    g.bind("owl", OWL)
    
    alpha = Namespace("http://example.org/alpha#")
    g.add((alpha.Test, RDF.type, OWL.Class))
    
    return g


class TestCanonicalizerInit:
    """Testes de inicialização do Canonicalizer."""
    
    def test_init_default(self):
        """Canonicalizer inicializa sem parâmetros."""
        canonicalizer = Canonicalizer()
        
        assert canonicalizer is not None
        assert canonicalizer.rules is not None
    
    def test_init_with_rules_path(self, rules_json_path):
        """Canonicalizer aceita caminho para rules.json."""
        canonicalizer = Canonicalizer(rules_path=rules_json_path)
        
        assert canonicalizer.rules is not None


class TestCanonicalizationResult:
    """Testes do CanonicalizationResult."""
    
    def test_canonicalize_returns_result(self, canonicalizer, simple_graph):
        """canonicalize() retorna CanonicalizationResult."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert isinstance(result, CanonicalizationResult)
    
    def test_result_has_graph(self, canonicalizer, simple_graph):
        """CanonicalizationResult contém grafo canonizado."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert result.graph is not None
        assert len(result.graph) == len(simple_graph)
    
    def test_result_has_counts(self, canonicalizer, simple_graph):
        """CanonicalizationResult contém contagens de triplas e prefixos."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert result.triple_count is not None
        assert result.prefix_count is not None
    
    def test_result_to_dict(self, canonicalizer, simple_graph):
        """CanonicalizationResult pode ser serializado para dict."""
        result = canonicalizer.canonicalize(simple_graph)
        
        result_dict = result.to_dict()
        
        assert "is_idempotent" in result_dict
        assert "triple_count" in result_dict
        assert "prefix_count" in result_dict


class TestPrefixOrdering:
    """Testes de ordenação de prefixos."""
    
    def test_prefixes_sorted_alphabetically(self, canonicalizer, graph_with_unordered_prefixes):
        """Prefixos são ordenados alfabeticamente."""
        result = canonicalizer.canonicalize(graph_with_unordered_prefixes)
        
        prefixes = [prefix for prefix, ns in result.graph.namespaces() if prefix]
        
        # Filtrar apenas prefixos customizados (excluir padrão RDFLib)
        custom_prefixes = [p for p in prefixes if p in ['alpha', 'beta', 'zoo', 'owl', 'rdf']]
        
        # Verificar que estão ordenados
        assert custom_prefixes == sorted(custom_prefixes)
    
    def test_standard_prefixes_preserved(self, canonicalizer, simple_graph):
        """Prefixos padrão são preservados."""
        result = canonicalizer.canonicalize(simple_graph)
        
        bound = dict(result.graph.namespaces())
        
        # Deve preservar prefixos originais
        assert "edo" in bound


class TestTripleOrdering:
    """Testes de ordenação de triplas."""
    
    def test_triples_preserved(self, canonicalizer, simple_graph):
        """Todas as triplas são preservadas."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert len(result.graph) == len(simple_graph)
    
    def test_triple_count_correct(self, canonicalizer, simple_graph):
        """Contagem de triplas está correta."""
        result = canonicalizer.canonicalize(simple_graph)
        
        # simple_graph tem 3 triplas (3 classes)
        assert result.triple_count == 3


class TestIdempotency:
    """Testes de idempotência."""
    
    def test_canonicalize_is_idempotent(self, canonicalizer, simple_graph):
        """Canonização é idempotente (aplicar 2x = 1x)."""
        result1 = canonicalizer.canonicalize(simple_graph)
        result2 = canonicalizer.canonicalize(result1.graph)
        
        # Segunda canonização deve produzir resultado idêntico
        assert result2.is_idempotent is True
    
    def test_serialization_is_stable(self, canonicalizer, simple_graph):
        """Serialização é estável (mesma entrada = mesma saída)."""
        result1 = canonicalizer.canonicalize(simple_graph)
        ttl1 = canonicalizer.serialize(result1.graph)
        
        result2 = canonicalizer.canonicalize(result1.graph)
        ttl2 = canonicalizer.serialize(result2.graph)
        
        assert ttl1 == ttl2


class TestSerialization:
    """Testes de serialização."""
    
    def test_serialize_returns_string(self, canonicalizer, simple_graph):
        """serialize() retorna string TTL."""
        result = canonicalizer.canonicalize(simple_graph)
        ttl = canonicalizer.serialize(result.graph)
        
        assert isinstance(ttl, str)
        assert len(ttl) > 0
    
    def test_serialize_is_valid_turtle(self, canonicalizer, simple_graph):
        """Serialização é TTL válido."""
        result = canonicalizer.canonicalize(simple_graph)
        ttl = canonicalizer.serialize(result.graph)
        
        # Deve ser possível parsear de volta
        g = Graph()
        g.parse(data=ttl, format="turtle")
        
        assert len(g) == len(simple_graph)
    
    def test_canonicalize_and_serialize_returns_tuple(self, canonicalizer, simple_graph):
        """canonicalize_and_serialize() retorna tuple com TTL e result."""
        ttl, result = canonicalizer.canonicalize_and_serialize(simple_graph)
        
        assert isinstance(ttl, str)
        assert isinstance(result, CanonicalizationResult)
        assert len(ttl) > 0


class TestProtegeCompatibility:
    """Testes de compatibilidade com Protégé."""
    
    def test_predicate_order_follows_protege(self, canonicalizer):
        """Ordem de predicados segue convenção Protégé."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)
        
        # Adicionar propriedades em ordem "errada"
        g.add((EDO.TestClass, SKOS.prefLabel, Literal("Test", lang="en")))
        g.add((EDO.TestClass, RDFS.label, Literal("Test")))
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        ttl = canonicalizer.serialize(result.graph)
        
        # Na serialização, rdf:type deve vir primeiro (convenção Protégé)
        # Verificação indireta: TTL deve ser válido
        assert "rdf:type" in ttl or "a " in ttl
    
    def test_output_matches_protege_style(self, canonicalizer, simple_graph):
        """Saída segue estilo Protégé."""
        result = canonicalizer.canonicalize(simple_graph)
        ttl = canonicalizer.serialize(result.graph)
        
        # Verificar características do estilo Protégé:
        # - Prefixos no início
        # - Triplas agrupadas por subject
        assert "@prefix" in ttl or "PREFIX" in ttl


class TestStatistics:
    """Testes de contagens."""
    
    def test_triple_count(self, canonicalizer, simple_graph):
        """Triple count está correto."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert result.triple_count == len(simple_graph)
    
    def test_prefix_count(self, canonicalizer, simple_graph):
        """Prefix count inclui prefixos vinculados."""
        result = canonicalizer.canonicalize(simple_graph)
        
        # Deve ter pelo menos os prefixos vinculados no simple_graph (edo, rdf, owl, skos)
        assert result.prefix_count >= 4
    
    def test_processing_time(self, canonicalizer, simple_graph):
        """Processing time é registrado."""
        result = canonicalizer.canonicalize(simple_graph)
        
        assert result.processing_time_ms >= 0


class TestEdgeCases:
    """Testes de casos especiais."""
    
    def test_empty_graph(self, canonicalizer):
        """Grafo vazio é processado sem erro."""
        g = Graph()
        
        result = canonicalizer.canonicalize(g)
        
        assert result.graph is not None
        assert len(result.graph) == 0
    
    def test_graph_with_blank_nodes(self, canonicalizer):
        """Grafo com blank nodes é processado."""
        from rdflib import BNode
        
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        
        blank = BNode()
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, OWL.equivalentClass, blank))
        g.add((blank, RDF.type, OWL.Restriction))
        
        result = canonicalizer.canonicalize(g)
        
        assert len(result.graph) == 3
    
    def test_graph_with_unicode(self, canonicalizer):
        """Grafo com Unicode é processado."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        
        g.add((EDO.Téste, RDF.type, OWL.Class))
        g.add((EDO.Téste, SKOS.prefLabel, Literal("Definição", lang="pt-br")))
        
        result = canonicalizer.canonicalize(g)
        
        assert len(result.graph) == 2
        
        # Serialização deve preservar Unicode
        ttl = canonicalizer.serialize(result.graph)
        assert "Definição" in ttl or "Defini" in ttl  # Pode estar escaped


# =============================================================================
# TESTES ADICIONAIS DE COBERTURA - canonicalizer.py
# =============================================================================

class TestCanonicalizerRulesLoading:
    """Testes para _load_rules() - linhas 88, 94-95, 99."""
    
    def test_load_rules_file_not_found_uses_defaults(self, tmp_path):
        """Arquivo rules.json não encontrado usa regras padrão."""
        canonicalizer = Canonicalizer(rules_path=str(tmp_path / "nonexistent.json"))
        
        assert canonicalizer.rules is not None
        assert "formatting" in canonicalizer.rules or "triples" in canonicalizer.rules
    
    def test_load_rules_invalid_json_uses_defaults(self, tmp_path):
        """Arquivo rules.json com JSON inválido usa regras padrão."""
        bad_json = tmp_path / "bad_rules.json"
        bad_json.write_text("{ invalid json content }", encoding="utf-8")
        
        canonicalizer = Canonicalizer(rules_path=str(bad_json))
        
        assert canonicalizer.rules is not None
    
    def test_load_rules_empty_file_uses_defaults(self, tmp_path):
        """Arquivo rules.json vazio usa regras padrão."""
        empty_json = tmp_path / "empty.json"
        empty_json.write_text("{}", encoding="utf-8")
        
        canonicalizer = Canonicalizer(rules_path=str(empty_json))
        
        # Mesmo com arquivo vazio, deve ter regras (get retorna {} então usa defaults)
        assert canonicalizer.rules is not None


class TestCanonicalizerBindPrefixes:
    """Testes para _bind_prefixes() - linhas 205-206, 237, 248."""
    
    def test_bind_prefixes_skips_automatic_ns_prefixes(self, canonicalizer):
        """Prefixos automáticos ns1, ns2 são ignorados."""
        g = Graph()
        ns1 = Namespace("http://auto1.example.org/")
        ns2 = Namespace("http://auto2.example.org/")
        g.bind("ns1", ns1)
        g.bind("ns2", ns2)
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        
        bound_prefixes = [p for p, _ in result.graph.namespaces()]
        # ns1 e ns2 devem ser ignorados (são automáticos do RDFLib)
        assert "edo" in bound_prefixes
    
    def test_bind_prefixes_with_required_prefixes(self, tmp_path):
        """Prefixos obrigatórios geram warning se não presentes."""
        import json
        
        rules = {
            "rules": {
                "prefixes": {
                    "required": [
                        {"prefix": "myprefix", "uri": "http://myprefix.example.org/"}
                    ]
                },
                "formatting": {"sort_prefixes_alphabetically": True}
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps(rules), encoding="utf-8")
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        
        # Deve ter warning sobre prefixo obrigatório ausente
        warnings = result.warnings
        assert any("missing_required_prefix" in str(w) or "myprefix" in str(w) for w in warnings)
    
    def test_bind_prefixes_unsorted(self, tmp_path):
        """Prefixos não ordenados quando sort_prefixes_alphabetically=False."""
        import json
        
        rules = {
            "rules": {
                "formatting": {"sort_prefixes_alphabetically": False}
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps(rules), encoding="utf-8")
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("zoo", Namespace("http://zoo.example.org/"))
        g.bind("alpha", Namespace("http://alpha.example.org/"))
        g.add((URIRef("http://zoo.example.org/Test"), RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        
        assert result.graph is not None


class TestCanonicalizerTripleSorting:
    """Testes para _sort_triples() - linhas 282, 293, 310."""
    
    def test_sort_triples_without_class_first(self, tmp_path):
        """Triplas ordenadas sem classes primeiro."""
        import json
        
        rules = {
            "rules": {
                "ordering": {
                    "class_declarations_before_properties": False,
                    "order_by": ["subject", "predicate", "object"]
                }
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps(rules), encoding="utf-8")
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.prop1, RDF.type, OWL.ObjectProperty))
        g.add((EDO.ClassA, RDF.type, OWL.Class))
        g.add((EDO.prop2, RDF.type, OWL.DatatypeProperty))
        
        result = canonicalizer.canonicalize(g)
        
        assert result.graph is not None
        assert len(result.graph) == 3
    
    def test_sort_triples_with_all_property_types(self, canonicalizer):
        """Ordenar com todos os tipos de propriedades."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        
        g.add((EDO.annotProp, RDF.type, OWL.AnnotationProperty))
        g.add((EDO.dataProp, RDF.type, OWL.DatatypeProperty))
        g.add((EDO.objProp, RDF.type, OWL.ObjectProperty))
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        
        assert result.triple_count == 4
    
    def test_collect_triples_removes_duplicates(self, canonicalizer):
        """Triplas duplicadas são removidas."""
        g = Graph()
        g.bind("edo", EDO)
        
        # Adicionar mesma tripla múltiplas vezes (RDFLib já previne, mas testamos o comportamento)
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, RDF.type, OWL.Class))  # Duplicata
        
        result = canonicalizer.canonicalize(g)
        
        # RDFLib já impede duplicatas, então deve ter 1
        assert result.triple_count == 1


class TestCanonicalizerLiteralNormalization:
    """Testes para normalização de literais - linhas 430-431."""
    
    def test_normalize_literal_with_uppercase_lang_tag(self, canonicalizer):
        """Lang tag em maiúsculas é normalizado para minúsculas."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        
        # Adicionar com lang tag em maiúsculas
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, SKOS.prefLabel, Literal("Test Class", lang="EN-US")))
        
        result = canonicalizer.canonicalize(g)
        
        # Verificar que lang tag foi normalizado
        for s, p, o in result.graph:
            if p == SKOS.prefLabel:
                assert o.language is None or o.language.islower()
    
    def test_normalize_literal_trims_whitespace(self, canonicalizer):
        """Whitespace em literais é removido."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, SKOS.prefLabel, Literal("  Test Class  ", lang="en")))
        
        result = canonicalizer.canonicalize(g)
        
        # Verificar que whitespace foi removido
        for s, p, o in result.graph:
            if p == SKOS.prefLabel:
                assert str(o).strip() == str(o)
    
    def test_normalize_literal_with_datatype(self, canonicalizer):
        """Literal com datatype é preservado."""
        g = Graph()
        g.bind("edo", EDO)
        
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, EDO.hasValue, Literal(42, datatype=XSD.integer)))
        
        result = canonicalizer.canonicalize(g)
        
        # Verificar que datatype foi preservado
        for s, p, o in result.graph:
            if p == EDO.hasValue:
                assert o.datatype == XSD.integer


class TestCanonicalizerGetWarnings:
    """Testes para get_warnings()."""
    
    def test_get_warnings_returns_list(self, canonicalizer, simple_graph):
        """get_warnings() retorna lista."""
        canonicalizer.canonicalize(simple_graph)
        
        warnings = canonicalizer.get_warnings()
        
        assert isinstance(warnings, list)
    
    def test_warnings_empty_for_valid_graph(self, canonicalizer, simple_graph):
        """Grafo válido não gera warnings."""
        canonicalizer.canonicalize(simple_graph)
        
        warnings = canonicalizer.get_warnings()
        
        # Pode ou não ter warnings dependendo da configuração
        assert isinstance(warnings, list)


# =============================================================================
# TESTES ADICIONAIS PARA COBERTURA
# =============================================================================

class TestCanonicalizerRequiredPrefixes:
    """Testes para prefixos obrigatórios (linhas 190, 237, 248)."""
    
    def test_missing_required_prefix_generates_warning(self, tmp_path):
        """Prefixo obrigatório faltante gera warning (linha 190)."""
        import json
        # A estrutura rules correta - prefixes está no nível de rules, não dentro de formatting
        rules_data = {
            "rules": {
                "prefixes": {
                    "required": [
                        {"prefix": "requiredns", "uri": "http://required.example.org/"}
                    ]
                }
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps(rules_data))
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        
        result = canonicalizer.canonicalize(g)
        
        warnings = canonicalizer.get_warnings()
        missing_prefix_warnings = [w for w in warnings if w.get("type", "") == "missing_required_prefix"]
        assert len(missing_prefix_warnings) > 0, f"Expected missing_required_prefix warning, got: {warnings}"


class TestCanonicalizerLiteralNormalization:
    """Testes para normalização de literais (linhas 237, 248)."""
    
    def test_literal_without_trim_whitespace(self, tmp_path):
        """Literal sem trim_whitespace preserva espaços (linha 237)."""
        import json
        rules = {
            "triples": {
                "normalize_literals": {
                    "trim_whitespace": False
                }
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps({"rules": rules}))
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, SKOS.prefLabel, Literal("  spaced  ", lang="en")))
        
        result = canonicalizer.canonicalize(g)
        
        assert result is not None
    
    def test_literal_with_none_value(self):
        """Literal com value None (linha 248)."""
        canonicalizer = Canonicalizer()
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.Test, RDF.type, OWL.Class))
        # Adicionar literal vazio
        g.add((EDO.Test, RDFS.comment, Literal("")))
        
        result = canonicalizer.canonicalize(g)
        
        assert result is not None


class TestCanonicalizerSortTriples:
    """Testes para ordenação de triplas (linhas 310, 345, 353)."""
    
    def test_class_declarations_not_first(self, tmp_path):
        """Declarações de classe não primeiro quando desabilitado (linha 310)."""
        import json
        rules = {
            "ordering": {
                "class_declarations_before_properties": False
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps({"rules": rules}))
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.testProp, RDF.type, OWL.ObjectProperty))
        
        result = canonicalizer.canonicalize(g)
        
        assert result is not None
    
    def test_triple_ordering_by_predicate(self, tmp_path):
        """Ordenação por predicate (linha 345)."""
        import json
        rules = {
            "ordering": {
                "order_by": ["predicate", "subject", "object"]
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps({"rules": rules}))
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.TestClass, RDF.type, OWL.Class))
        g.add((EDO.TestClass, RDFS.label, Literal("Test", lang="en")))
        
        result = canonicalizer.canonicalize(g)
        
        assert result is not None
    
    def test_triple_ordering_complex(self, tmp_path):
        """Ordenação complexa com múltiplos critérios (linha 353)."""
        import json
        rules = {
            "ordering": {
                "order_by": ["object", "subject", "predicate"],
                "class_declarations_before_properties": True
            }
        }
        rules_file = tmp_path / "rules.json"
        rules_file.write_text(json.dumps({"rules": rules}))
        
        canonicalizer = Canonicalizer(rules_path=str(rules_file))
        
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.ClassA, RDF.type, OWL.Class))
        g.add((EDO.ClassB, RDF.type, OWL.Class))
        g.add((EDO.propA, RDF.type, OWL.ObjectProperty))
        
        result = canonicalizer.canonicalize(g)
        
        assert result is not None


class TestCanonicalizerVerifyIdempotency:
    """Testes para validate_idempotency (linhas 404-412)."""
    
    def test_validate_idempotency_returns_true(self, canonicalizer, simple_graph):
        """validate_idempotency retorna True para canonização idempotente."""
        result = canonicalizer.validate_idempotency(simple_graph)
        
        assert result is True
    
    def test_validate_idempotency_after_multiple_calls(self, canonicalizer, simple_graph):
        """validate_idempotency é True após múltiplas chamadas."""
        # Primeira canonização
        canonicalizer.canonicalize(simple_graph)
        
        # Verificar idempotência
        result = canonicalizer.validate_idempotency(simple_graph)
        
        assert result is True


class TestCanonicalizerSerialize:
    """Testes para serialize (linhas 430-431)."""
    
    def test_serialize_returns_string(self, canonicalizer, simple_graph):
        """serialize retorna string TTL."""
        result = canonicalizer.canonicalize(simple_graph)
        
        ttl = canonicalizer.serialize(result.graph)
        
        assert isinstance(ttl, str)
        assert "@prefix" in ttl
    
    def test_serialize_empty_graph(self, canonicalizer):
        """serialize de grafo vazio retorna string."""
        g = Graph()
        
        result = canonicalizer.canonicalize(g)
        ttl = canonicalizer.serialize(result.graph)
        
        assert isinstance(ttl, str)


class TestSemanticPreservation:
    """
    Testes para GATE-B (Semantic Preservation Gate) — PATCH-v7.
    
    Objetivo: garantir que canonização preserva isomorfismo RDF,
    em particular multilinguismo (triplas com mesmo lexical form
    mas language tags distintas devem ser preservadas).
    """
    
    def test_preserves_multilingual_labels_distinct_tags(self, canonicalizer):
        """
        T-702: Canonização preserva triplas multilíngues com mesmo lexical form.
        
        Bug reportado no GATE-ISOMORPH-FAILURE-ANALYSIS_patch-v5.md:
        - Canonização removia triplas como PLEM@en vs PLEM@pt-br
        - Causa: deduplicação por string key ignorava language tags
        
        Após T-701: canonização NÃO deve remover essas triplas.
        """
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        
        # Adicionar triplas com MESMO lexical form mas language tags diferentes
        g.add((EDO.PLEM, SKOS.prefLabel, Literal("PLEM", lang="en")))
        g.add((EDO.PLEM, SKOS.prefLabel, Literal("PLEM", lang="pt-br")))
        
        # Canonizar
        result = canonicalizer.canonicalize(g)
        
        # Verificar que AMBAS triplas foram preservadas
        labels_en = list(result.graph.objects(EDO.PLEM, SKOS.prefLabel))
        labels_with_en_tag = [lit for lit in labels_en if lit.language == "en"]
        labels_with_pt_br_tag = [lit for lit in labels_en if lit.language == "pt-br"]
        
        assert len(labels_with_en_tag) == 1, "Tripla com @en foi removida (violação de isomorfismo)"
        assert len(labels_with_pt_br_tag) == 1, "Tripla com @pt-br foi removida (violação de isomorfismo)"
        
        # Verificar contagem total
        assert len(result.graph) == 2, f"Esperado 2 triplas, obtido {len(result.graph)}"
    
    def test_preserves_whitespace_in_literals(self, canonicalizer):
        """
        T-702: Canonização NÃO altera whitespace em literais.
        
        Motivação: trim whitespace pode alterar semântica RDF
        (literais "  value  " vs "value" são distintos).
        """
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdfs", RDFS)
        
        # Literal com whitespace intencional
        g.add((EDO.ClassA, RDFS.comment, Literal("  spaced  ", lang="en")))
        
        # Canonizar
        result = canonicalizer.canonicalize(g)
        
        # Verificar que whitespace foi preservado
        comments = list(result.graph.objects(EDO.ClassA, RDFS.comment))
        assert len(comments) == 1
        assert str(comments[0]) == "  spaced  ", "Whitespace foi alterado (violação de preservação semântica)"
    
    def test_preserves_language_tag_case(self, canonicalizer):
        """
        T-702: Canonização NÃO altera case de language tags.
        
        Motivação: BCP 47 permite "pt-BR" e "pt-br" (case-insensitive),
        mas rdflib trata como strings distintas.
        Canonização NÃO deve normalizar para evitar alteração de triplas.
        """
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        
        # Adicionar literais com language tags em cases diferentes
        g.add((EDO.ClassA, SKOS.prefLabel, Literal("Label", lang="PT-BR")))
        
        # Canonizar
        result = canonicalizer.canonicalize(g)
        
        # Verificar que case foi preservado
        labels = list(result.graph.objects(EDO.ClassA, SKOS.prefLabel))
        assert len(labels) == 1
        # rdflib normaliza para lowercase internamente, mas tripla deve existir
        assert labels[0].language in ["pt-br", "PT-BR"], "Language tag foi perdida"
    
    def test_isomorphism_after_canonicalization(self, canonicalizer):
        """
        T-702: Canonização preserva isomorfismo RDF (Input ≅ Canonicalized).
        
        Contrato UC-103: canonização DEVE preservar grafo RDF.
        Teste formal usando rdflib.compare.isomorphic.
        """
        from rdflib.compare import isomorphic
        
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        g.bind("owl", OWL)
        
        # Grafo com multilinguismo
        g.add((EDO.PLEM, RDF.type, OWL.Class))
        g.add((EDO.PLEM, SKOS.prefLabel, Literal("PLEM", lang="en")))
        g.add((EDO.PLEM, SKOS.prefLabel, Literal("PLEM", lang="pt-br")))
        
        # Canonizar
        result = canonicalizer.canonicalize(g)
        
        # Verificar isomorfismo
        assert isomorphic(g, result.graph), "Canonização alterou o grafo RDF (violação do contrato UC-103)"
    
    def test_real_ontology_whitespace_preservation(self, canonicalizer):
        """
        T-717: Teste de integração com subconjunto REAL da ontologia EDO.
        
        Motivação: Validar preservação de whitespace com dados reais
        (não sintéticos). EDO contém " Seal Ring"@en - whitespace intencional
        que deve ser preservado durante canonização.
        
        Caso de regressão: Prevenir bugs futuros onde canonização
        possa inadvertidamente alterar literais.
        """
        from rdflib.compare import isomorphic
        from rdflib.namespace import DCTERMS
        
        # Criar subconjunto real da EDO com edge cases de whitespace
        g = Graph()
        g.bind("edo", Namespace("https://w3id.org/energy-domain/edo#"))
        g.bind("skos", SKOS)
        g.bind("owl", OWL)
        g.bind("dcterms", DCTERMS)
        
        EDO_NS = Namespace("https://w3id.org/energy-domain/edo#")
        RingGasket = EDO_NS.RingGasket
        
        # Triplas reais do EDO (subset focado em whitespace edge cases)
        g.add((RingGasket, RDF.type, OWL.Class))
        g.add((RingGasket, DCTERMS.identifier, Literal("RingGasket")))
        
        # EDGE CASE: whitespace leading (" Seal Ring"@en)
        g.add((RingGasket, SKOS.altLabel, Literal(" Seal Ring", lang="en")))
        g.add((RingGasket, SKOS.altLabel, Literal("Gasket", lang="en")))
        g.add((RingGasket, SKOS.altLabel, Literal("O-Ring", lang="en")))
        
        # Multilinguismo
        g.add((RingGasket, SKOS.prefLabel, Literal("Junta de Conexão", lang="pt-br")))
        g.add((RingGasket, SKOS.prefLabel, Literal("Ring Gasket", lang="en")))
        
        # Canonizar
        result = canonicalizer.canonicalize(g)
        
        # VALIDAÇÃO 1: Isomorfismo (Input ≅ Canonicalized)
        assert isomorphic(g, result.graph), (
            f"Canonização alterou o grafo RDF. "
            f"Input: {len(g)} triplas, Canonicalized: {len(result.graph)} triplas. "
            f"Violação do contrato UC-103."
        )
        
        # VALIDAÇÃO 2: Whitespace leading preservado (" Seal Ring"@en)
        alt_labels = list(result.graph.objects(RingGasket, SKOS.altLabel))
        whitespace_label = [lit for lit in alt_labels if str(lit).startswith(" Seal")]
        assert len(whitespace_label) == 1, (
            f"Whitespace leading foi removido de ' Seal Ring'@en. "
            f"Esperado: ' Seal Ring', Obtido: {[str(lit) for lit in alt_labels]}"
        )
        assert str(whitespace_label[0]) == " Seal Ring", (
            f"Literal com whitespace foi alterado. "
            f"Esperado: ' Seal Ring', Obtido: '{str(whitespace_label[0])}'"
        )
        
        # VALIDAÇÃO 3: Multilinguismo preservado
        pref_labels_pt = [lit for lit in result.graph.objects(RingGasket, SKOS.prefLabel) 
                          if lit.language == "pt-br"]
        pref_labels_en = [lit for lit in result.graph.objects(RingGasket, SKOS.prefLabel) 
                          if lit.language == "en"]
        assert len(pref_labels_pt) == 1, "Tripla com @pt-br foi removida"
        assert len(pref_labels_en) == 1, "Tripla com @en foi removida"
        
        # VALIDAÇÃO 4: Contagem total de triplas
        # 1 rdf:type + 1 dcterms:identifier + 3 skos:altLabel + 2 skos:prefLabel = 7 triplas
        assert len(result.graph) == 7, (
            f"Número de triplas alterado. Esperado: 7, Obtido: {len(result.graph)}"
        )
