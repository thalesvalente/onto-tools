"""
Testes para RDFlibAdapter - Adapter para rdflib.

Cobre:
- Carregamento de arquivos TTL
- Salvamento de grafos
- Parsing de conteúdo Turtle
- Serialização para Turtle
- Validação de encoding
- Tratamento de erros
"""
import pytest
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


class TestRDFlibAdapterLoadTTL:
    """Testes de carregamento de TTL."""
    
    def test_load_valid_file(self, tmp_ttl_file):
        """Carrega arquivo TTL válido."""
        graph, metadata = RDFlibAdapter.load_ttl(tmp_ttl_file)
        
        assert graph is not None
        assert len(graph) > 0
    
    def test_load_returns_metadata(self, tmp_ttl_file):
        """Carregamento retorna metadados corretos."""
        graph, metadata = RDFlibAdapter.load_ttl(tmp_ttl_file)
        
        assert "hash" in metadata
        assert "triple_count" in metadata
        assert "source_path" in metadata
    
    def test_load_hash_is_sha256(self, tmp_ttl_file):
        """Hash é SHA256 (64 caracteres hex)."""
        graph, metadata = RDFlibAdapter.load_ttl(tmp_ttl_file)
        
        assert len(metadata["hash"]) == 64
        assert all(c in "0123456789abcdef" for c in metadata["hash"])
    
    def test_load_nonexistent_raises_filenotfound(self):
        """Arquivo inexistente levanta FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            RDFlibAdapter.load_ttl("/nao/existe/arquivo.ttl")
    
    def test_load_directory_raises_valueerror(self, tmp_path):
        """Diretório levanta ValueError."""
        with pytest.raises(ValueError, match="não é um arquivo"):
            RDFlibAdapter.load_ttl(str(tmp_path))
    
    def test_load_invalid_encoding_raises(self, tmp_path):
        """Arquivo com encoding inválido levanta ValueError."""
        bad_file = tmp_path / "bad.ttl"
        bad_file.write_bytes(b"\xff\xfe invalid utf-8")
        
        with pytest.raises(ValueError, match="UTF-8"):
            RDFlibAdapter.load_ttl(str(bad_file))
    
    def test_load_invalid_syntax_raises(self, tmp_path):
        """Arquivo com sintaxe inválida levanta ValueError."""
        bad_file = tmp_path / "bad.ttl"
        bad_file.write_text("this is not valid turtle @#$%", encoding="utf-8")
        
        with pytest.raises(ValueError, match="sintaxe"):
            RDFlibAdapter.load_ttl(str(bad_file))


class TestRDFlibAdapterSaveTTL:
    """Testes de salvamento de TTL."""
    
    def test_save_creates_file(self, tmp_path, minimal_class_graph):
        """Salvamento cria arquivo."""
        output = tmp_path / "output.ttl"
        
        RDFlibAdapter.save_ttl(minimal_class_graph, str(output))
        
        assert output.exists()
    
    def test_save_creates_parent_dirs(self, tmp_path, minimal_class_graph):
        """Salvamento cria diretórios pai."""
        output = tmp_path / "subdir" / "nested" / "output.ttl"
        
        RDFlibAdapter.save_ttl(minimal_class_graph, str(output))
        
        assert output.exists()
    
    def test_save_utf8_encoding(self, tmp_path, minimal_class_graph):
        """Arquivo salvo em UTF-8."""
        output = tmp_path / "output.ttl"
        
        RDFlibAdapter.save_ttl(minimal_class_graph, str(output))
        
        # Deve ser possível ler como UTF-8
        content = output.read_text(encoding="utf-8")
        assert len(content) > 0
    
    def test_save_preserves_triples(self, tmp_path, minimal_class_graph):
        """Salvamento preserva triplas."""
        output = tmp_path / "output.ttl"
        original_count = len(minimal_class_graph)
        
        RDFlibAdapter.save_ttl(minimal_class_graph, str(output))
        
        # Recarregar e verificar
        reloaded, _ = RDFlibAdapter.load_ttl(str(output))
        assert len(reloaded) == original_count


class TestRDFlibAdapterParseTurtle:
    """Testes de parsing de conteúdo Turtle."""
    
    def test_parse_valid_turtle(self):
        """Parseia Turtle válido."""
        content = """
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:TestClass a owl:Class .
        """
        
        graph = RDFlibAdapter.parse_turtle(content)
        
        assert len(graph) == 1
    
    def test_parse_with_prefixes(self):
        """Parsing extrai prefixos."""
        content = """
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix edo: <https://w3id.org/energy-domain/edo#> .
        
        edo:TestClass rdf:type owl:Class .
        """
        
        graph = RDFlibAdapter.parse_turtle(content)
        
        prefixes = dict(graph.namespaces())
        assert "edo" in prefixes
    
    def test_parse_invalid_raises(self):
        """Turtle inválido levanta ValueError."""
        content = "this is not valid turtle @#$%"
        
        with pytest.raises(ValueError, match="parsear"):
            RDFlibAdapter.parse_turtle(content)


class TestRDFlibAdapterSerializeTurtle:
    """Testes de serialização para Turtle."""
    
    def test_serialize_returns_string(self, minimal_class_graph):
        """Serialização retorna string."""
        result = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_serialize_contains_prefixes(self, minimal_class_graph):
        """Serialização contém declarações de prefixos."""
        result = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        
        assert "@prefix" in result
    
    def test_serialize_contains_triples(self, minimal_class_graph):
        """Serialização contém triplas."""
        result = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        
        assert "owl:Class" in result or "Class" in result
    
    def test_serialize_roundtrip(self, minimal_class_graph):
        """Roundtrip serialização -> parsing preserva triplas."""
        original_count = len(minimal_class_graph)
        
        serialized = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        reparsed = RDFlibAdapter.parse_turtle(serialized)
        
        assert len(reparsed) == original_count


class TestRDFlibAdapterProtegeStyle:
    """Testes de serialização estilo Protégé."""
    
    def test_serialization_uses_protege_style(self, minimal_class_graph):
        """Serialização usa estilo Protégé."""
        result = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        
        # Estilo Protégé tem características específicas
        assert "@prefix" in result
    
    def test_prefixes_sorted(self, minimal_class_graph):
        """Prefixos estão ordenados."""
        result = RDFlibAdapter.serialize_turtle(minimal_class_graph)
        
        # Extrair linhas de prefixo
        prefix_lines = [line for line in result.split("\n") if line.startswith("@prefix")]
        
        # Verificar que estão ordenados
        prefixes = [line.split()[1].rstrip(":") for line in prefix_lines]
        assert prefixes == sorted(prefixes)


class TestRDFlibAdapterFormatMap:
    """Testes do mapeamento de formatos."""
    
    def test_format_map_exists(self):
        """Mapa de formatos existe."""
        assert hasattr(RDFlibAdapter, "_format_map")
    
    def test_turtle_format_mapped(self):
        """Formato turtle está mapeado."""
        assert "turtle" in RDFlibAdapter._format_map
        assert "ttl" in RDFlibAdapter._format_map
    
    def test_rdf_xml_format_mapped(self):
        """Formato RDF/XML está mapeado."""
        assert "rdf" in RDFlibAdapter._format_map
        assert "owl" in RDFlibAdapter._format_map


class TestRDFlibAdapterEdgeCases:
    """Testes de casos extremos."""
    
    def test_empty_graph_serializes(self):
        """Grafo vazio serializa."""
        empty = Graph()
        
        result = RDFlibAdapter.serialize_turtle(empty)
        
        assert isinstance(result, str)
    
    def test_unicode_content_handled(self, tmp_path):
        """Conteúdo Unicode é tratado corretamente."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        g.add((EDO.Test, SKOS.prefLabel, Literal("Teste com acentuação: ção, ã, é", lang="pt-br")))
        
        output = tmp_path / "unicode.ttl"
        RDFlibAdapter.save_ttl(g, str(output))
        
        # Recarregar
        reloaded, _ = RDFlibAdapter.load_ttl(str(output))
        labels = list(reloaded.objects(EDO.Test, SKOS.prefLabel))
        
        assert len(labels) == 1
        assert "ção" in str(labels[0])
    
    def test_large_literals_handled(self, tmp_path):
        """Literais grandes são tratados."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("rdfs", RDFS)
        
        long_text = "A" * 10000
        g.add((EDO.Test, RDFS.comment, Literal(long_text)))
        
        output = tmp_path / "large.ttl"
        RDFlibAdapter.save_ttl(g, str(output))
        
        # Deve funcionar sem erro
        assert output.exists()
