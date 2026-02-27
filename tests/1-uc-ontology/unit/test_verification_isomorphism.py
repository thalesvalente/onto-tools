"""
Unit tests for verification.isomorphism module.

Tests RDF graph isomorphism comparison functionality.
"""
from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace, URIRef

from onto_tools.application.verification.isomorphism import (
    compare_isomorphism,
    compare_graphs,
    IsomorphismReport
)


EX = Namespace("http://example.org/")


class TestCompareIsomorphism:
    """Tests for compare_isomorphism function."""
    
    @pytest.fixture
    def simple_ttl_content(self) -> str:
        """Simple TTL content for testing."""
        return """
@prefix ex: <http://example.org/> .

ex:Subject1 ex:predicate1 ex:Object1 .
ex:Subject1 ex:predicate2 "Literal value" .
"""
    
    @pytest.fixture
    def equivalent_ttl_content(self) -> str:
        """Equivalent TTL with different ordering."""
        return """
@prefix ex: <http://example.org/> .

ex:Subject1 ex:predicate2 "Literal value" .
ex:Subject1 ex:predicate1 ex:Object1 .
"""
    
    @pytest.fixture
    def different_ttl_content(self) -> str:
        """Different TTL content."""
        return """
@prefix ex: <http://example.org/> .

ex:Subject1 ex:predicate1 ex:Object1 .
ex:Subject1 ex:predicate2 "Different value" .
"""
    
    def test_identical_files_are_isomorphic(self, tmp_path: Path, simple_ttl_content: str):
        """Test that identical files are isomorphic."""
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(simple_ttl_content)
        file_b.write_text(simple_ttl_content)
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is True
        assert report.graph_a_triple_count == 2
        assert report.graph_b_triple_count == 2
        assert report.error is None
    
    def test_equivalent_graphs_are_isomorphic(
        self, tmp_path: Path, simple_ttl_content: str, equivalent_ttl_content: str
    ):
        """Test that semantically equivalent graphs are isomorphic."""
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(simple_ttl_content)
        file_b.write_text(equivalent_ttl_content)
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is True
        assert report.graph_a_triple_count == 2
        assert report.graph_b_triple_count == 2
    
    def test_different_graphs_not_isomorphic(
        self, tmp_path: Path, simple_ttl_content: str, different_ttl_content: str
    ):
        """Test that different graphs are not isomorphic."""
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(simple_ttl_content)
        file_b.write_text(different_ttl_content)
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is False
        assert report.triples_only_in_a > 0 or report.triples_only_in_b > 0
    
    def test_empty_graphs_are_isomorphic(self, tmp_path: Path):
        """Test that empty graphs are isomorphic."""
        empty_ttl = "@prefix ex: <http://example.org/> .\n"
        
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(empty_ttl)
        file_b.write_text(empty_ttl)
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is True
        assert report.graph_a_triple_count == 0
        assert report.graph_b_triple_count == 0
    
    def test_missing_file_returns_error(self, tmp_path: Path, simple_ttl_content: str):
        """Test that missing file returns error report."""
        file_a = tmp_path / "exists.ttl"
        file_b = tmp_path / "missing.ttl"
        
        file_a.write_text(simple_ttl_content)
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is False
        assert report.error is not None
        # Error message varies by platform - just ensure there's an error
    
    def test_invalid_ttl_returns_error(self, tmp_path: Path, simple_ttl_content: str):
        """Test that invalid TTL returns error report."""
        file_a = tmp_path / "valid.ttl"
        file_b = tmp_path / "invalid.ttl"
        
        file_a.write_text(simple_ttl_content)
        file_b.write_text("This is not valid TTL { broken")
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is False
        assert report.error is not None
    
    def test_diff_samples_limited(self, tmp_path: Path):
        """Test that diff samples are limited."""
        # Create graphs with many differences
        ttl_a = "@prefix ex: <http://example.org/> .\n"
        ttl_b = "@prefix ex: <http://example.org/> .\n"
        
        for i in range(10):
            ttl_a += f"ex:Subject{i} ex:pred ex:ObjA{i} .\n"
            ttl_b += f"ex:Subject{i} ex:pred ex:ObjB{i} .\n"
        
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(ttl_a)
        file_b.write_text(ttl_b)
        
        report = compare_isomorphism(file_a, file_b, max_diff_samples=3)
        
        assert report.are_isomorphic is False
        assert len(report.sample_diff_a) <= 3
        assert len(report.sample_diff_b) <= 3
    
    def test_report_to_dict(self, tmp_path: Path, simple_ttl_content: str):
        """Test report serialization to dict."""
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(simple_ttl_content)
        file_b.write_text(simple_ttl_content)
        
        report = compare_isomorphism(file_a, file_b)
        report_dict = report.to_dict()
        
        assert "are_isomorphic" in report_dict
        assert "graph_a_triple_count" in report_dict
        assert "graph_b_triple_count" in report_dict
        assert report_dict["are_isomorphic"] is True


class TestCompareGraphs:
    """Tests for compare_graphs function (in-memory graphs)."""
    
    def test_identical_graphs_isomorphic(self):
        """Test that identical in-memory graphs are isomorphic."""
        g1 = Graph()
        g2 = Graph()
        
        g1.add((EX.Subject, EX.predicate, EX.Object))
        g2.add((EX.Subject, EX.predicate, EX.Object))
        
        report = compare_graphs(g1, g2)
        
        assert report.are_isomorphic is True
    
    def test_different_graphs_not_isomorphic(self):
        """Test that different in-memory graphs are not isomorphic."""
        g1 = Graph()
        g2 = Graph()
        
        g1.add((EX.Subject, EX.predicate, Literal("Value A")))
        g2.add((EX.Subject, EX.predicate, Literal("Value B")))
        
        report = compare_graphs(g1, g2)
        
        assert report.are_isomorphic is False
    
    def test_empty_graphs_isomorphic(self):
        """Test that empty graphs are isomorphic."""
        g1 = Graph()
        g2 = Graph()
        
        report = compare_graphs(g1, g2)
        
        assert report.are_isomorphic is True
        assert report.graph_a_triple_count == 0
        assert report.graph_b_triple_count == 0


class TestIsomorphismReport:
    """Tests for IsomorphismReport dataclass."""
    
    def test_report_defaults(self):
        """Test report default values."""
        report = IsomorphismReport(
            are_isomorphic=True,
            graph_a_path="a.ttl",
            graph_b_path="b.ttl"
        )
        
        assert report.graph_a_triple_count == 0
        assert report.graph_b_triple_count == 0
        assert report.triples_only_in_a == 0
        assert report.triples_only_in_b == 0
        assert report.sample_diff_a == []
        assert report.sample_diff_b == []
        assert report.error is None
    
    def test_report_to_dict_complete(self):
        """Test complete report serialization."""
        report = IsomorphismReport(
            are_isomorphic=False,
            graph_a_path="a.ttl",
            graph_b_path="b.ttl",
            graph_a_triple_count=10,
            graph_b_triple_count=8,
            triples_only_in_a=3,
            triples_only_in_b=1,
            sample_diff_a=["triple1", "triple2"],
            sample_diff_b=["triple3"],
            error=None
        )
        
        d = report.to_dict()
        
        assert d["are_isomorphic"] is False
        assert d["graph_a_path"] == "a.ttl"
        assert d["graph_b_path"] == "b.ttl"
        assert d["graph_a_triple_count"] == 10
        assert d["graph_b_triple_count"] == 8
        assert d["triples_only_in_a"] == 3
        assert d["triples_only_in_b"] == 1
        assert len(d["sample_diff_a"]) == 2
        assert len(d["sample_diff_b"]) == 1

    def test_report_with_error(self):
        """Test report with error field populated."""
        report = IsomorphismReport(
            are_isomorphic=False,
            graph_a_path="a.ttl",
            graph_b_path="b.ttl",
            error="Comparison failed: ValueError: Invalid format"
        )
        
        d = report.to_dict()
        
        assert d["are_isomorphic"] is False
        assert d["error"] == "Comparison failed: ValueError: Invalid format"


class TestExceptionHandling:
    """Tests for exception handling in isomorphism module."""
    
    def test_compare_isomorphism_with_corrupted_file(self, tmp_path: Path):
        """Test handling of file that causes parse error."""
        file_a = tmp_path / "good.ttl"
        file_b = tmp_path / "bad.ttl"
        
        file_a.write_text("@prefix ex: <http://example.org/> .\nex:s ex:p ex:o .")
        # Write binary garbage that can't be decoded
        file_b.write_bytes(b"\x00\x01\x02\x03")
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is False
        assert report.error is not None
    
    def test_compare_graphs_with_custom_labels(self):
        """Test compare_graphs with custom label parameters."""
        from rdflib import Graph, Namespace, Literal
        EX = Namespace("http://example.org/")
        
        g1 = Graph()
        g2 = Graph()
        
        g1.add((EX.Subject, EX.predicate, Literal("Value A")))
        g2.add((EX.Subject, EX.predicate, Literal("Value B")))
        
        report = compare_graphs(g1, g2, label_a="CustomGraph1", label_b="CustomGraph2")
        
        assert report.graph_a_path == "CustomGraph1"
        assert report.graph_b_path == "CustomGraph2"
        assert report.are_isomorphic is False
    
    def test_compare_isomorphism_missing_file(self, tmp_path: Path):
        """Test handling when one file is missing."""
        file_a = tmp_path / "exists.ttl"
        file_b = tmp_path / "does_not_exist.ttl"
        
        file_a.write_text("@prefix ex: <http://example.org/> .\nex:s ex:p ex:o .")
        # file_b intentionally not created
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is False
        assert report.error is not None
        # Error message may vary by platform/rdflib version
    
    def test_compare_isomorphism_with_different_formats(self, tmp_path: Path):
        """Test comparing files with different formats."""
        ttl_content = "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.n3"
        
        file_a.write_text(ttl_content)
        file_b.write_text(ttl_content)  # n3 is compatible with turtle
        
        report = compare_isomorphism(file_a, file_b)
        
        assert report.are_isomorphic is True


# ============================================================================
# Error / branch coverage
# ============================================================================

class TestIsomorphismErrorPaths:
    """Covers lines 72->89, 172, 229, 234, 239-240 in isomorphism.py."""

    def test_compare_isomorphism_with_explicit_format_skips_auto_detect(self, tmp_path: Path):
        """Calling _load_graph with explicit format bypasses auto-detect block (covers branch 72->89)."""
        from onto_tools.application.verification.isomorphism import _load_graph

        ttl_content = "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        file_a = tmp_path / "a.ttl"
        file_a.write_text(ttl_content)

        # Explicit format= means `if format is None:` is False → branch 72->89 taken
        g = _load_graph(file_a, format="turtle")
        assert len(g) == 1

    def test_compare_isomorphism_file_not_found_returns_error(self, tmp_path: Path):
        """FileNotFoundError handler in compare_isomorphism returns error report (line 172)."""
        from unittest.mock import patch

        file_a = tmp_path / "a.ttl"
        file_a.write_text("@prefix ex: <http://example.org/> .\nex:s ex:p ex:o .")
        file_b = tmp_path / "b.ttl"
        file_b.write_text("@prefix ex: <http://example.org/> .\nex:s ex:p ex:o .")

        # Patch _load_graph to raise FileNotFoundError on the second call
        original_load = None
        call_count = [0]

        from onto_tools.application.verification import isomorphism as iso_module
        original_load = iso_module._load_graph

        def fake_load_graph(path, fmt=None):
            call_count[0] += 1
            if call_count[0] == 2:
                raise FileNotFoundError("mocked: file not found")
            return original_load(path, fmt)

        with patch.object(iso_module, "_load_graph", side_effect=fake_load_graph):
            report = compare_isomorphism(file_a, file_b)

        assert report.are_isomorphic is False
        assert report.error is not None
        assert "not found" in report.error.lower()

    def test_compare_graphs_with_more_diffs_than_max_samples(self):
        """break statements in diff loops are hit when diff > max_diff_samples (lines 229, 234)."""
        g1 = Graph()
        g2 = Graph()
        EX = Namespace("http://example.org/")

        # Create 8 unique triples in each graph (> default max_diff_samples=5)
        for i in range(8):
            g1.add((EX[f"s{i}"], EX.p, URIRef(f"http://example.org/o1_{i}")))
            g2.add((EX[f"s{i}"], EX.p, URIRef(f"http://example.org/o2_{i}")))

        report = compare_graphs(g1, g2, max_diff_samples=5)
        assert report.are_isomorphic is False
        assert len(report.sample_diff_a) == 5   # capped at max_diff_samples
        assert len(report.sample_diff_b) == 5

    def test_compare_graphs_exception_in_isomorphic_check(self):
        """compare_graphs catches unexpected exceptions (covers lines 229-240)."""
        from unittest.mock import patch

        g = Graph()
        with patch(
            "onto_tools.application.verification.isomorphism.isomorphic",
            side_effect=MemoryError("out of memory"),
        ):
            report = compare_graphs(g, g)

        assert report.are_isomorphic is False
        assert report.error is not None
        assert "MemoryError" in report.error
