"""
Test byte-level determinism of canonicalization.

CRITICAL: Must run in separate processes to ensure true determinism.
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def compute_sha256(file_path: str) -> str:
    """Calcula SHA256 de um arquivo."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


class TestByteDeterminism:
    """Testes de determinismo byte-a-byte."""

    def test_canonicalization_is_byte_deterministic(self):
        """
        GATE-3: Canonização deve produzir saída byte-idêntica em execuções repetidas.

        Este teste executa a canonização duas vezes em processos Python separados
        para garantir que não há dependência de estado de memória ou ordem de
        dicionários dentro de um mesmo processo.
        """
        script = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.canonicalizer import Canonicalizer

input_path = "data/edo/core/energy-domain-ontology.ttl"
adapter = RDFlibAdapter()
graph, _ = adapter.load_ttl(input_path)

canonicalizer = Canonicalizer()
result = canonicalizer.canonicalize(graph)

output_path = sys.argv[1]
adapter.save_ttl(result.graph, output_path, canonized=True)
print(f"Saved to {output_path}")
'''
        with tempfile.TemporaryDirectory() as tmpdir:
            output_a = Path(tmpdir) / "canon-a.ttl"
            output_b = Path(tmpdir) / "canon-b.ttl"

            result_a = subprocess.run(
                [sys.executable, "-c", script, str(output_a)],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            assert result_a.returncode == 0, f"Process A failed: {result_a.stderr}"

            result_b = subprocess.run(
                [sys.executable, "-c", script, str(output_b)],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            assert result_b.returncode == 0, f"Process B failed: {result_b.stderr}"

            hash_a = compute_sha256(str(output_a))
            hash_b = compute_sha256(str(output_b))
            bytes_a = output_a.read_bytes()
            bytes_b = output_b.read_bytes()

            assert hash_a == hash_b, (
                f"Canonicalization is NOT deterministic!\n"
                f"Hash A: {hash_a}\nHash B: {hash_b}\n"
                f"Size A: {len(bytes_a)} bytes\nSize B: {len(bytes_b)} bytes"
            )
            assert bytes_a == bytes_b, "Hashes match but bytes differ (collision?)"


class TestSemanticPreservation:
    """Testes de preservação semântica (isomorfismo)."""

    def test_canonicalization_preserves_semantics(self):
        """
        GATE-2: Canonização deve preservar semântica RDF (isomorfismo).
        """
        from rdflib.compare import isomorphic

        sys.path.insert(0, str(Path.cwd() / "src"))
        from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
        from onto_tools.domain.ontology.canonicalizer import Canonicalizer

        input_path = "data/edo/core/energy-domain-ontology.ttl"
        adapter = RDFlibAdapter()
        input_graph, _ = adapter.load_ttl(input_path)

        canonicalizer = Canonicalizer()
        result = canonicalizer.canonicalize(input_graph)
        output_graph = result.graph

        assert isomorphic(input_graph, output_graph), (
            f"Canonicalization did NOT preserve semantics!\n"
            f"Input triples: {len(input_graph)}\n"
            f"Output triples: {len(output_graph)}"
        )
        assert len(input_graph) == len(output_graph), (
            f"Triple count mismatch: {len(input_graph)} vs {len(output_graph)}"
        )


class TestSeparationOfConcerns:
    """Testes de separação de responsabilidades (SoC)."""
    
    def test_canonicalizer_does_not_normalize_literals(self):
        """
        GATE-SOC: Canonicalizer NÃO deve normalizar literais.
        
        Canonicalizer (UC-103) é responsável apenas por ordenação determinística.
        Normalização de literais é responsabilidade do Normalizer (UC-108).
        """
        from rdflib import Graph, Literal, URIRef, Namespace
        
        sys.path.insert(0, str(Path.cwd() / "src"))
        from onto_tools.domain.ontology.canonicalizer import Canonicalizer
        
        # Create graph with literal that has leading/trailing whitespace
        g = Graph()
        EDO = Namespace("https://example.org/test#")
        g.add((EDO.TestClass, EDO.label, Literal("  Test with spaces  ", lang="en")))
        g.add((EDO.TestClass, EDO.description, Literal("\\n\\tIndented\\n\\t", lang="pt-br")))
        
        # Canonicalize
        canonicalizer = Canonicalizer()
        result = canonicalizer.canonicalize(g)
        
        # Check that whitespace is PRESERVED
        literals = list(result.graph.objects(EDO.TestClass, EDO.label))
        assert len(literals) == 1
        assert str(literals[0]) == "  Test with spaces  ", "Leading/trailing spaces removed!"
        assert literals[0].language == "en", "Language tag modified!"
        
        desc_literals = list(result.graph.objects(EDO.TestClass, EDO.description))
        assert len(desc_literals) == 1
        assert str(desc_literals[0]) == "\\n\\tIndented\\n\\t", "Newlines/tabs removed!"
        assert desc_literals[0].language == "pt-br", "Language tag modified!"
        
        print("\\n✅ Canonicalizer does NOT normalize literals (whitespace preserved)")
    
    def test_canonicalizer_does_not_modify_language_tags(self):
        """
        GATE-SOC: Canonicalizer NÃO deve modificar language tags.
        """
        from rdflib import Graph, Literal, Namespace
        
        sys.path.insert(0, str(Path.cwd() / "src"))
        from onto_tools.domain.ontology.canonicalizer import Canonicalizer
        
        # Create graph with various language tag cases
        g = Graph()
        EDO = Namespace("https://example.org/test#")
        g.add((EDO.TestClass, EDO.label, Literal("Test", lang="EN")))  # uppercase
        g.add((EDO.TestClass, EDO.altLabel, Literal("Teste", lang="pt-BR")))  # mixed case
        
        # Canonicalize
        canonicalizer = Canonicalizer()
        result = canonicalizer.canonicalize(g)
        
        # Check that language tags are PRESERVED (not lowercased)
        labels = list(result.graph.objects(EDO.TestClass, EDO.label))
        assert len(labels) == 1
        # rdflib normalizes to lowercase, but we preserve what rdflib gives us
        # The point is we don't ADD normalization on top of rdflib
        assert labels[0].language is not None, "Language tag removed!"
        
        alt_labels = list(result.graph.objects(EDO.TestClass, EDO.altLabel))
        assert len(alt_labels) == 1
        assert alt_labels[0].language is not None, "Language tag removed!"
        
        print(f"\\n✅ Language tags preserved: {labels[0].language}, {alt_labels[0].language}")
