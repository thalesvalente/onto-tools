"""
Tests for UC-104: Generate Review Package with Verification

These tests verify that UC-104 properly generates:
1. Canonical TTL output
2. Export log (export-log.json)
3. Run manifest (run_manifest.json) when canonized=True
4. Verification results (isomorphism + idempotency)

Coverage targets:
- facade.generate_review_output()
- Integration with verification module
- Console output (artifact paths announcement)
"""
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import tempfile
import shutil

from onto_tools.application.facade import OntoToolsFacade
from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.application.verification import (
    RunManifest,
    write_manifest_atomic,
    read_manifest,
    sha256_file,
    compare_isomorphism,
    check_idempotency
)


class TestManifestWriter:
    """Unit tests for manifest writer functionality."""
    
    def test_manifest_create_has_required_fields(self):
        """Test RunManifest.create() generates required fields."""
        manifest = RunManifest.create(command="test_command")
        
        assert manifest.run_id is not None
        assert manifest.timestamp is not None
        assert manifest.command == "test_command"
        assert manifest.success is True
        assert manifest.error is None
    
    def test_manifest_add_input(self, tmp_path):
        """Test adding input artifact to manifest."""
        # Create test file
        test_file = tmp_path / "input.ttl"
        test_file.write_text("# Test TTL content")
        
        manifest = RunManifest.create(command="test")
        manifest.add_input(test_file)
        
        assert len(manifest.inputs) == 1
        assert manifest.inputs[0].path == str(test_file)
        assert manifest.inputs[0].sha256 is not None
        assert manifest.inputs[0].format == "turtle"
    
    def test_manifest_add_output(self, tmp_path):
        """Test adding output artifact to manifest."""
        test_file = tmp_path / "output.ttl"
        test_file.write_text("# Output TTL")
        
        manifest = RunManifest.create(command="test")
        manifest.add_output(test_file, artifact_type="canonical_ontology")
        
        assert len(manifest.outputs) == 1
        assert manifest.outputs[0].artifact_type == "canonical_ontology"
    
    def test_manifest_add_verification(self):
        """Test adding verification result to manifest."""
        manifest = RunManifest.create(command="test")
        manifest.add_verification("isomorphism", True, {"detail": "test"})
        
        assert len(manifest.verifications) == 1
        assert manifest.verifications[0].check_type == "isomorphism"
        assert manifest.verifications[0].passed is True
    
    def test_manifest_write_atomic(self, tmp_path):
        """Test atomic manifest write creates valid JSON."""
        manifest = RunManifest.create(command="test_atomic")
        manifest_path = tmp_path / "manifest.json"
        
        write_manifest_atomic(manifest, manifest_path)
        
        assert manifest_path.exists()
        with open(manifest_path) as f:
            data = json.load(f)
        assert data["command"] == "test_atomic"
    
    def test_manifest_read_roundtrip(self, tmp_path):
        """Test manifest can be written and read back."""
        manifest = RunManifest.create(command="roundtrip_test")
        manifest.add_verification("test_check", True, {"foo": "bar"})
        
        manifest_path = tmp_path / "roundtrip.json"
        write_manifest_atomic(manifest, manifest_path)
        
        loaded = read_manifest(manifest_path)
        assert loaded.command == "roundtrip_test"
        assert len(loaded.verifications) == 1


class TestVerificationIntegration:
    """Integration tests for verification functions."""
    
    def test_sha256_file_computes_hash(self, tmp_path):
        """Test SHA256 computation for files."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World")
        
        hash_value = sha256_file(test_file)
        
        assert hash_value is not None
        assert len(hash_value) == 64  # SHA256 hex string length
    
    def test_sha256_same_content_same_hash(self, tmp_path):
        """Test identical content produces same hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        content = "Identical content"
        file1.write_text(content)
        file2.write_text(content)
        
        assert sha256_file(file1) == sha256_file(file2)


class TestUC104GenerateReviewOutput:
    """Integration tests for UC-104 generate_review_output."""
    
    @pytest.fixture
    def facade_with_loaded_ontology(self, data_examples_dir, tmp_path):
        """Create facade with a loaded test ontology."""
        # Create mock audit logger
        audit_logger = MagicMock()
        audit_logger.log = MagicMock()
        
        facade = OntoToolsFacade(
            rdf_adapter=RDFlibAdapter(),
            audit_logger=audit_logger
        )
        
        # Load test ontology
        test_ontology = data_examples_dir / "energy-domain-ontology-test.ttl"
        if test_ontology.exists():
            facade.load_ontology(str(test_ontology))
        else:
            # Create minimal test ontology if example doesn't exist
            minimal_ttl = tmp_path / "minimal.ttl"
            minimal_ttl.write_text("""
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix edo: <https://w3id.org/energy-domain/edo#> .

<https://w3id.org/energy-domain/edo> a owl:Ontology .
edo:TestClass a owl:Class ;
    rdfs:label "Test Class" .
""")
            facade.load_ontology(str(minimal_ttl))
        
        return facade
    
    def test_generate_review_without_canonization(self, facade_with_loaded_ontology, tmp_path):
        """Test UC-104 without canonization doesn't generate manifest."""
        facade = facade_with_loaded_ontology
        output_path = tmp_path / "output.ttl"
        
        result = facade.generate_review_output(
            output_path=str(output_path),
            canonized=False,
            enable_verification=True
        )
        
        assert result["status"] == "success"
        assert output_path.exists()
        assert "manifest_path" not in result  # No manifest without canonization
    
    def test_generate_review_with_canonization_creates_manifest(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """Test UC-104 with canonization generates run_manifest.json."""
        facade = facade_with_loaded_ontology
        output_path = tmp_path / "canonical_output.ttl"
        
        # First canonicalize
        facade.canonicalize_ontology()
        
        result = facade.generate_review_output(
            output_path=str(output_path),
            canonized=True,
            enable_verification=True
        )
        
        assert result["status"] == "success"
        assert "manifest_path" in result
        
        manifest_path = Path(result["manifest_path"])
        assert manifest_path.exists()
        
        # Verify manifest content (now a list for audit log style)
        with open(manifest_path) as f:
            manifest_data = json.load(f)
        
        # Handle both list and single object format
        manifest = manifest_data[-1] if isinstance(manifest_data, list) else manifest_data
        
        assert manifest["command"] == "generate_review_output"
        assert len(manifest["inputs"]) >= 1
        assert len(manifest["outputs"]) >= 1
        assert len(manifest["verifications"]) == 2
    
    def test_generate_review_verifications_pass(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """Test that verification checks pass for valid canonization."""
        facade = facade_with_loaded_ontology
        output_path = tmp_path / "verified_output.ttl"
        
        facade.canonicalize_ontology()
        
        result = facade.generate_review_output(
            output_path=str(output_path),
            canonized=True,
            enable_verification=True
        )
        
        assert result["status"] == "success"
        assert "verifications" in result
        
        verifications = result["verifications"]
        
        # Isomorphism should pass (semantic equivalence)
        assert verifications["isomorphism"]["passed"] is True
        
        # Idempotency should pass (f(f(x)) == f(x))
        assert verifications["idempotency"]["passed"] is True
    
    def test_generate_review_returns_all_paths(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """Test that result contains all expected artifact paths."""
        facade = facade_with_loaded_ontology
        output_path = tmp_path / "full_output.ttl"
        
        facade.canonicalize_ontology()
        
        result = facade.generate_review_output(
            output_path=str(output_path),
            canonized=True,
            enable_verification=True
        )
        
        # Must have all path fields
        assert "ttl_path" in result
        assert "log_path" in result
        assert "manifest_path" in result
        
        # All paths should point to existing files
        assert Path(result["ttl_path"]).exists()
        assert Path(result["log_path"]).exists()
        assert Path(result["manifest_path"]).exists()
    
    def test_generate_review_disable_verification(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """Test verification can be disabled."""
        facade = facade_with_loaded_ontology
        output_path = tmp_path / "no_verify_output.ttl"
        
        facade.canonicalize_ontology()
        
        result = facade.generate_review_output(
            output_path=str(output_path),
            canonized=True,
            enable_verification=False
        )
        
        assert result["status"] == "success"
        assert "manifest_path" not in result
        assert "verifications" not in result

    def test_generate_review_output_appends_to_existing_log(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """Two calls to same directory append to existing export-log.json (covers lines 316-322)."""
        import json

        facade = facade_with_loaded_ontology

        # First call – creates the log file
        result1 = facade.generate_review_output(
            output_path=str(tmp_path / "output1.ttl"),
            canonized=False,
            enable_verification=False,
        )
        assert result1["status"] == "success"

        # Second call – log file already exists; code reads + appends
        result2 = facade.generate_review_output(
            output_path=str(tmp_path / "output2.ttl"),
            canonized=False,
            enable_verification=False,
        )
        assert result2["status"] == "success"

        log_path = tmp_path / "export-log.json"
        assert log_path.exists()
        with open(log_path) as f:
            log_data = json.load(f)
        assert len(log_data) == 2  # Both entries appended

    def test_generate_review_output_corrupted_log_recovers(self, facade_with_loaded_ontology, tmp_path):
        """When existing export-log.json is corrupted JSON, code recovers with empty list (covers line 321)."""
        # Create a corrupted log file
        log_path = tmp_path / "export-log.json"
        log_path.write_text("this is not valid json {{{", encoding="utf-8")

        result = facade_with_loaded_ontology.generate_review_output(
            output_path=str(tmp_path / "output.ttl"),
            canonized=False,
            enable_verification=False,
        )
        assert result["status"] == "success"  # Should recover gracefully

    def test_generate_review_output_exception_returns_error(
        self, facade_with_loaded_ontology, tmp_path
    ):
        """generate_review_output returns error dict on unexpected exception (covers lines 493-495)."""
        from unittest.mock import patch

        facade = facade_with_loaded_ontology

        # Force save to raise so the except block runs
        with patch.object(
            facade._ontology_graph,
            "save",
            side_effect=IOError("Simulated disk error"),
        ):
            result = facade.generate_review_output(
                output_path=str(tmp_path / "output.ttl"),
                canonized=False,
            )

        assert result["status"] == "error"
        assert "Simulated disk error" in result["message"]


class TestMenuUC104Display:
    """Tests for UC-104 menu display (UX requirements)."""
    
    def test_action_ontology_review_displays_verification(self):
        """Test that menu action displays verification results."""
        # This is a mock test to verify the menu function would display
        # verification results. Full E2E testing requires interactive testing.
        from onto_tools.adapters.cli.menu import action_ontology_review
        
        # Verify the function exists and has proper signature
        assert callable(action_ontology_review)


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
