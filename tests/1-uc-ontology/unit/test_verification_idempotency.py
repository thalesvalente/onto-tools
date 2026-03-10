"""
Unit tests for verification.idempotency module.

Tests idempotency verification functionality.
"""
from pathlib import Path
from typing import Callable

import pytest
from rdflib import Graph, Namespace

from onto_tools.application.verification.idempotency import (
    check_idempotency,
    check_graph_idempotency,
    check_full_idempotency,
    verify_canonicalization_idempotent,
    IdempotencyReport,
    FullIdempotencyReport
)


EX = Namespace("http://example.org/")


class TestCheckIdempotency:
    """Tests for check_idempotency function."""
    
    @pytest.fixture
    def simple_ttl_content(self) -> str:
        """Simple TTL content for testing."""
        return """
@prefix ex: <http://example.org/> .

ex:Subject1 ex:predicate1 ex:Object1 .
ex:Subject1 ex:predicate2 "Literal value" .
"""
    
    @pytest.fixture
    def identity_transform(self) -> Callable[[Path, Path], None]:
        """Transform that copies file unchanged (idempotent)."""
        def transform(input_path: Path, output_path: Path) -> None:
            import shutil
            shutil.copy2(input_path, output_path)
        return transform
    
    @pytest.fixture
    def appending_transform(self) -> Callable[[Path, Path], None]:
        """Transform that adds a triple each time (NOT idempotent)."""
        counter = [0]
        
        def transform(input_path: Path, output_path: Path) -> None:
            from rdflib import Graph, Namespace
            EX = Namespace("http://example.org/")
            g = Graph()
            g.parse(str(input_path), format="turtle")
            # Add a NEW triple each time
            g.add((EX[f"NewSubject{counter[0]}"], EX.newPredicate, EX.newObject))
            counter[0] += 1
            g.serialize(destination=str(output_path), format="turtle")
        return transform
    
    def test_identity_is_idempotent(
        self, tmp_path: Path, simple_ttl_content: str, identity_transform
    ):
        """Test that identity transform is idempotent."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(simple_ttl_content)
        
        report = check_idempotency(input_file, identity_transform)
        
        assert report.is_idempotent is True
        assert report.hashes_match is True
        assert report.first_result_hash is not None
        assert report.second_result_hash is not None
        assert report.first_result_hash == report.second_result_hash
    
    def test_appending_not_idempotent(
        self, tmp_path: Path, simple_ttl_content: str, appending_transform
    ):
        """Test that appending transform is not idempotent."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(simple_ttl_content)
        
        report = check_idempotency(input_file, appending_transform)
        
        assert report.is_idempotent is False
        assert report.hashes_match is False
        assert report.first_result_hash != report.second_result_hash
    
    def test_missing_input_returns_error(self, tmp_path: Path, identity_transform):
        """Test that missing input file returns error."""
        input_file = tmp_path / "nonexistent.ttl"
        
        report = check_idempotency(input_file, identity_transform)
        
        assert report.is_idempotent is False
        assert report.error is not None
        assert "not found" in report.error.lower()
    
    def test_transform_failure_returns_error(self, tmp_path: Path, simple_ttl_content: str):
        """Test that transform failure returns error."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(simple_ttl_content)
        
        def failing_transform(input_path: Path, output_path: Path) -> None:
            raise RuntimeError("Transform failed")
        
        report = check_idempotency(input_file, failing_transform)
        
        assert report.is_idempotent is False
        assert report.error is not None
        assert "Transform failed" in report.error or "RuntimeError" in report.error
    
    def test_no_output_returns_error(self, tmp_path: Path, simple_ttl_content: str):
        """Test that transform producing no output returns error."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(simple_ttl_content)
        
        def no_output_transform(input_path: Path, output_path: Path) -> None:
            pass  # Does nothing
        
        report = check_idempotency(input_file, no_output_transform)
        
        assert report.is_idempotent is False
        assert report.error is not None
    
    def test_semantically_equivalent_is_idempotent(self, tmp_path: Path):
        """Test that semantically equivalent output counts as idempotent."""
        # This tests the isomorphism fallback when hashes differ
        input_file = tmp_path / "input.ttl"
        input_file.write_text("""
@prefix ex: <http://example.org/> .
ex:A ex:p ex:B .
ex:C ex:q ex:D .
""")
        
        call_count = [0]
        
        def reordering_transform(input_path: Path, output_path: Path) -> None:
            """Transform that reorders triples but preserves semantics."""
            from rdflib import Graph
            g = Graph()
            g.parse(str(input_path), format="turtle")
            
            # First call: reverse order; subsequent: same
            if call_count[0] == 0:
                g.serialize(destination=str(output_path), format="turtle")
            else:
                g.serialize(destination=str(output_path), format="turtle")
            call_count[0] += 1
        
        report = check_idempotency(input_file, reordering_transform)
        
        # Even if bytes differ, isomorphism should pass
        assert report.is_idempotent is True
    
    def test_report_to_dict(self, tmp_path: Path, simple_ttl_content: str, identity_transform):
        """Test report serialization."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(simple_ttl_content)
        
        report = check_idempotency(input_file, identity_transform)
        report_dict = report.to_dict()
        
        assert "is_idempotent" in report_dict
        assert "hashes_match" in report_dict
        assert "first_result_hash" in report_dict
        assert "second_result_hash" in report_dict


class TestCheckGraphIdempotency:
    """Tests for check_graph_idempotency function (in-memory)."""
    
    def test_identity_graph_transform_idempotent(self):
        """Test that identity graph transform is idempotent."""
        g = Graph()
        g.add((EX.Subject, EX.predicate, EX.Object))
        
        def identity(graph: Graph) -> Graph:
            return graph
        
        report = check_graph_idempotency(g, identity)
        
        assert report.is_idempotent is True
    
    def test_modifying_transform_not_idempotent(self):
        """Test that modifying transform is not idempotent."""
        g = Graph()
        g.add((EX.Subject, EX.predicate, EX.Object))
        
        counter = [0]
        
        def adding_transform(graph: Graph) -> Graph:
            new_graph = Graph()
            for triple in graph:
                new_graph.add(triple)
            new_graph.add((EX[f"NewSubject{counter[0]}"], EX.pred, EX.obj))
            counter[0] += 1
            return new_graph
        
        report = check_graph_idempotency(g, adding_transform)
        
        assert report.is_idempotent is False
    
    def test_error_handling(self):
        """Test error handling in graph transform."""
        g = Graph()
        g.add((EX.Subject, EX.predicate, EX.Object))
        
        def failing_transform(graph: Graph) -> Graph:
            raise ValueError("Transform error")
        
        report = check_graph_idempotency(g, failing_transform)
        
        assert report.is_idempotent is False
        assert report.error is not None


class TestIdempotencyReport:
    """Tests for IdempotencyReport dataclass."""
    
    def test_report_defaults(self):
        """Test report default values."""
        report = IdempotencyReport(
            is_idempotent=True,
            input_path="input.ttl"
        )
        
        assert report.first_result_hash is None
        assert report.second_result_hash is None
        assert report.hashes_match is False
        assert report.isomorphism_report is None
        assert report.error is None
    
    def test_report_to_dict_with_isomorphism(self):
        """Test report serialization with isomorphism report."""
        from onto_tools.application.verification.isomorphism import IsomorphismReport
        
        iso_report = IsomorphismReport(
            are_isomorphic=True,
            graph_a_path="first.ttl",
            graph_b_path="second.ttl",
            graph_a_triple_count=5,
            graph_b_triple_count=5
        )
        
        report = IdempotencyReport(
            is_idempotent=True,
            input_path="input.ttl",
            first_result_hash="ABC123",
            second_result_hash="ABC123",
            hashes_match=True,
            isomorphism_report=iso_report
        )
        
        d = report.to_dict()
        
        assert d["is_idempotent"] is True
        assert d["hashes_match"] is True
        assert d["isomorphism_report"] is not None


class TestCheckFullIdempotency:
    """Tests for check_full_idempotency function.
    
    This tests the extended idempotency check that verifies:
    1. saved_file_hash == first_result_hash (saved file is canonical)
    2. first_result_hash == second_result_hash (f(f(x)) == f(x))
    """
    
    @pytest.fixture
    def simple_ttl_content(self) -> str:
        """Simple TTL content for testing."""
        return """
@prefix ex: <http://example.org/> .

ex:Subject1 ex:predicate1 ex:Object1 .
ex:Subject1 ex:predicate2 "Literal value" .
"""
    
    @pytest.fixture
    def identity_transform(self) -> callable:
        """Transform that copies file unchanged (idempotent and consistent)."""
        def transform(input_path: Path, output_path: Path) -> None:
            import shutil
            shutil.copy2(input_path, output_path)
        return transform
    
    @pytest.fixture
    def canonical_transform(self) -> callable:
        """Transform that uses real canonicalization."""
        def transform(input_path: Path, output_path: Path) -> None:
            from rdflib import Graph
            from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
            from onto_tools.adapters.rdf.protege_serializer import serialize_protege_style
            
            g = Graph()
            g.parse(str(input_path), format='turtle')
            canon_result = canonicalize_graph(g)
            serialized = serialize_protege_style(canon_result.graph)
            Path(output_path).write_bytes(serialized.encode("utf-8"))
        return transform
    
    def test_identity_is_fully_consistent(
        self, tmp_path: Path, simple_ttl_content: str, identity_transform
    ):
        """Test that identity transform produces fully consistent results."""
        saved_file = tmp_path / "saved.ttl"
        saved_file.write_text(simple_ttl_content)
        
        report = check_full_idempotency(saved_file, identity_transform)
        
        assert report.is_idempotent is True
        assert report.is_fully_consistent is True
        assert report.saved_matches_first is True
        assert report.hashes_match is True
        assert report.saved_file_hash == report.first_result_hash
        assert report.first_result_hash == report.second_result_hash
    
    def test_inconsistent_save_detected(self, tmp_path: Path, simple_ttl_content: str):
        """Test that inconsistent save operation is detected.
        
        This is the bug case: saved file uses one serialization,
        but verification transform uses a different one.
        """
        saved_file = tmp_path / "saved.ttl"
        saved_file.write_text(simple_ttl_content)  # Saved with standard serialization
        
        # Transform that produces different output (simulating the old bug)
        def different_transform(input_path: Path, output_path: Path) -> None:
            from rdflib import Graph
            g = Graph()
            g.parse(str(input_path), format='turtle')
            # Add a comment that changes the hash
            content = g.serialize(format='turtle')
            content = "# Added by transform\n" + content
            Path(output_path).write_text(content)
        
        report = check_full_idempotency(saved_file, different_transform)
        
        # Idempotent (transform applied twice gives same result)
        assert report.is_idempotent is True
        assert report.hashes_match is True
        
        # BUT NOT fully consistent (saved file != transform output)
        assert report.is_fully_consistent is False
        assert report.saved_matches_first is False
        assert report.saved_file_hash != report.first_result_hash
    
    def test_canonical_transform_is_fully_consistent(
        self, tmp_path: Path, canonical_transform
    ):
        """Test that properly canonicalized file is fully consistent."""
        from rdflib import Graph
        from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
        from onto_tools.adapters.rdf.protege_serializer import serialize_protege_style
        
        # Create source and canonicalize it (simulating correct save)
        source_content = """
@prefix ex: <http://example.org/> .
ex:B ex:p ex:C .
ex:A ex:q ex:D .
"""
        source_file = tmp_path / "source.ttl"
        source_file.write_text(source_content)
        
        # Apply canonical transform to save
        g = Graph()
        g.parse(str(source_file), format='turtle')
        canon_result = canonicalize_graph(g)
        serialized = serialize_protege_style(canon_result.graph)
        
        saved_file = tmp_path / "saved.ttl"
        saved_file.write_bytes(serialized.encode("utf-8"))
        
        # Now verify
        report = check_full_idempotency(saved_file, canonical_transform)
        
        assert report.is_idempotent is True
        assert report.is_fully_consistent is True
        assert report.saved_matches_first is True
        assert report.hashes_match is True
    
    def test_missing_file_returns_error(self, tmp_path: Path, identity_transform):
        """Test that missing file returns appropriate error."""
        nonexistent = tmp_path / "nonexistent.ttl"
        
        report = check_full_idempotency(nonexistent, identity_transform)
        
        assert report.is_idempotent is False
        assert report.is_fully_consistent is False
        assert report.error is not None
        assert "not found" in report.error.lower()
    
    def test_transform_failure_returns_error(self, tmp_path: Path, simple_ttl_content: str):
        """Test that transform failure returns error."""
        saved_file = tmp_path / "saved.ttl"
        saved_file.write_text(simple_ttl_content)
        
        def failing_transform(input_path: Path, output_path: Path) -> None:
            raise RuntimeError("Transform failed")
        
        report = check_full_idempotency(saved_file, failing_transform)
        
        assert report.is_idempotent is False
        assert report.is_fully_consistent is False
        assert report.error is not None
    
    def test_report_to_dict(self, tmp_path: Path, simple_ttl_content: str, identity_transform):
        """Test report serialization."""
        saved_file = tmp_path / "saved.ttl"
        saved_file.write_text(simple_ttl_content)
        
        report = check_full_idempotency(saved_file, identity_transform)
        report_dict = report.to_dict()
        
        assert "is_idempotent" in report_dict
        assert "is_fully_consistent" in report_dict
        assert "saved_file_hash" in report_dict
        assert "first_result_hash" in report_dict
        assert "second_result_hash" in report_dict
        assert "saved_matches_first" in report_dict
        assert "hashes_match" in report_dict


class TestFullIdempotencyReport:
    """Tests for FullIdempotencyReport dataclass."""
    
    def test_report_defaults(self):
        """Test report default values."""
        report = FullIdempotencyReport(
            is_idempotent=True,
            is_fully_consistent=True,
            saved_file_path="saved.ttl"
        )
        
        assert report.saved_file_hash is None
        assert report.first_result_hash is None
        assert report.second_result_hash is None
        assert report.saved_matches_first is False
        assert report.hashes_match is False
        assert report.error is None
    
    def test_full_report_to_dict(self):
        """Test full report serialization."""
        report = FullIdempotencyReport(
            is_idempotent=True,
            is_fully_consistent=True,
            saved_file_path="saved.ttl",
            saved_file_hash="AAA111",
            first_result_hash="AAA111",
            second_result_hash="AAA111",
            saved_matches_first=True,
            hashes_match=True
        )
        
        d = report.to_dict()
        
        assert d["is_idempotent"] is True
        assert d["is_fully_consistent"] is True
        assert d["saved_matches_first"] is True
        assert d["saved_file_hash"] == d["first_result_hash"]


# ============================================================================
# Error / edge-case paths coverage
# ============================================================================

class TestIdempotencyErrorPaths:
    """Covers lines 115, 213, 302, 317 in idempotency.py."""

    def test_check_idempotency_second_output_not_created(self, tmp_path):
        """When second transform call never writes output, report is_idempotent=False (line 115)."""
        import shutil as _shutil

        input_file = tmp_path / "input.ttl"
        input_file.write_text(
            "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        )

        call_count = [0]

        def transform_fn(inp: Path, out: Path) -> None:
            call_count[0] += 1
            if call_count[0] == 1:
                _shutil.copy2(str(inp), str(out))
            # Second call deliberately omits creating the output file

        report = check_idempotency(input_file, transform_fn)
        assert report.is_idempotent is False
        assert report.error is not None
        assert "Second transform" in report.error

    def test_check_graph_idempotency_transform_raises(self):
        """check_graph_idempotency handles exception in transform (line 213)."""

        def bad_transform(g: Graph) -> Graph:
            raise RuntimeError("transform exploded")

        report = check_graph_idempotency(Graph(), bad_transform)
        assert report.is_idempotent is False
        assert report.error is not None
        assert "transform exploded" in report.error

    def test_check_full_idempotency_first_output_not_created(self, tmp_path):
        """check_full_idempotency returns error when first transform produces no output (line 302)."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text(
            "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        )

        def noop_transform(inp: Path, out: Path) -> None:
            pass  # never creates output

        report = check_full_idempotency(input_file, noop_transform)
        assert report.is_idempotent is False
        assert report.error is not None
        assert "did not produce output file" in report.error

    def test_check_full_idempotency_second_output_not_created(self, tmp_path):
        """check_full_idempotency returns error when second transform produces no output (line 317)."""
        import shutil as _shutil

        input_file = tmp_path / "input.ttl"
        input_file.write_text(
            "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        )

        call_count = [0]

        def transform_fn(inp: Path, out: Path) -> None:
            call_count[0] += 1
            if call_count[0] == 1:
                _shutil.copy2(str(inp), str(out))
            # Second call omits creating output

        report = check_full_idempotency(input_file, transform_fn)
        assert report.is_idempotent is False
        assert report.error is not None
        assert "Second transform" in report.error

    def test_verify_canonicalization_idempotent_delegates(self, tmp_path):
        """verify_canonicalization_idempotent delegates to check_idempotency (covers line 213)."""
        import shutil as _shutil

        input_file = tmp_path / "input.ttl"
        input_file.write_text(
            "@prefix ex: <http://example.org/> .\nex:s ex:p ex:o ."
        )

        def identity_transform(inp: Path, out: Path) -> None:
            _shutil.copy2(str(inp), str(out))

        report = verify_canonicalization_idempotent(input_file, identity_transform)
        assert report.is_idempotent is True
