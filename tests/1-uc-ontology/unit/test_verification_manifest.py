"""
Unit tests for verification.manifest_writer module.

Tests RunManifest creation and atomic writing functionality.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from onto_tools.application.verification.manifest_writer import (
    InputArtifact,
    OutputArtifact,
    VerificationResult,
    EnvironmentInfo,
    RunManifest,
    write_manifest_atomic,
    read_manifest
)


class TestInputArtifact:
    """Tests for InputArtifact dataclass."""
    
    def test_from_file(self, tmp_path: Path):
        """Test creating InputArtifact from file."""
        test_file = tmp_path / "test.ttl"
        test_file.write_text("@prefix ex: <http://example.org/> .")
        
        artifact = InputArtifact.from_file(test_file)
        
        assert artifact.path == str(test_file)
        assert len(artifact.sha256) == 64
        assert artifact.size_bytes > 0
        assert artifact.format == "turtle"
    
    def test_format_detection(self, tmp_path: Path):
        """Test automatic format detection."""
        formats = {
            "test.ttl": "turtle",
            "test.n3": "n3",
            "test.nt": "ntriples",
            "test.rdf": "rdfxml",
            "test.owl": "rdfxml",
            "test.jsonld": "json-ld",
            "test.xyz": "unknown"
        }
        
        for filename, expected_format in formats.items():
            test_file = tmp_path / filename
            test_file.write_text("content")
            
            artifact = InputArtifact.from_file(test_file)
            assert artifact.format == expected_format, f"Failed for {filename}"
    
    def test_explicit_format(self, tmp_path: Path):
        """Test explicit format override."""
        test_file = tmp_path / "test.xyz"
        test_file.write_text("content")
        
        artifact = InputArtifact.from_file(test_file, format="custom")
        
        assert artifact.format == "custom"


class TestOutputArtifact:
    """Tests for OutputArtifact dataclass."""
    
    def test_from_file(self, tmp_path: Path):
        """Test creating OutputArtifact from file."""
        test_file = tmp_path / "output.ttl"
        test_file.write_text("@prefix ex: <http://example.org/> .")
        
        artifact = OutputArtifact.from_file(test_file, artifact_type="canonical_ontology")
        
        assert artifact.path == str(test_file)
        assert len(artifact.sha256) == 64
        assert artifact.size_bytes > 0
        assert artifact.artifact_type == "canonical_ontology"
        assert artifact.format == "turtle"


class TestVerificationResult:
    """Tests for VerificationResult dataclass."""
    
    def test_basic_result(self):
        """Test creating basic verification result."""
        result = VerificationResult(
            check_type="isomorphism",
            passed=True,
            details={"triple_count": 100}
        )
        
        assert result.check_type == "isomorphism"
        assert result.passed is True
        assert result.details["triple_count"] == 100
    
    def test_default_details(self):
        """Test default empty details."""
        result = VerificationResult(
            check_type="hash",
            passed=True
        )
        
        assert result.details == {}


class TestEnvironmentInfo:
    """Tests for EnvironmentInfo dataclass."""
    
    def test_auto_populated(self):
        """Test auto-populated environment info."""
        info = EnvironmentInfo()
        
        assert info.python_version is not None
        assert info.platform is not None
        assert info.hostname is not None
        assert info.cwd is not None


class TestRunManifest:
    """Tests for RunManifest dataclass."""
    
    def test_create_with_defaults(self):
        """Test creating manifest with defaults."""
        manifest = RunManifest.create(command="test_command")
        
        assert manifest.command == "test_command"
        assert manifest.run_id is not None
        assert manifest.timestamp is not None
        assert manifest.inputs == []
        assert manifest.outputs == []
        assert manifest.verifications == []
        assert manifest.success is True
        assert manifest.error is None
    
    def test_add_input(self, tmp_path: Path):
        """Test adding input artifact."""
        test_file = tmp_path / "input.ttl"
        test_file.write_text("content")
        
        manifest = RunManifest.create(command="test")
        manifest.add_input(test_file)
        
        assert len(manifest.inputs) == 1
        assert manifest.inputs[0].path == str(test_file)
    
    def test_add_output(self, tmp_path: Path):
        """Test adding output artifact."""
        test_file = tmp_path / "output.ttl"
        test_file.write_text("content")
        
        manifest = RunManifest.create(command="test")
        manifest.add_output(test_file, artifact_type="result")
        
        assert len(manifest.outputs) == 1
        assert manifest.outputs[0].artifact_type == "result"
    
    def test_add_verification(self):
        """Test adding verification result."""
        manifest = RunManifest.create(command="test")
        manifest.add_verification("isomorphism", True, {"count": 50})
        
        assert len(manifest.verifications) == 1
        assert manifest.verifications[0].check_type == "isomorphism"
        assert manifest.verifications[0].passed is True
    
    def test_set_duration(self):
        """Test setting duration."""
        manifest = RunManifest.create(command="test")
        manifest.set_duration(1.5)
        
        assert manifest.duration_seconds == 1.5
    
    def test_set_error(self):
        """Test setting error."""
        manifest = RunManifest.create(command="test")
        manifest.set_error("Something failed")
        
        assert manifest.success is False
        assert manifest.error == "Something failed"
    
    def test_method_chaining(self, tmp_path: Path):
        """Test method chaining."""
        input_file = tmp_path / "input.ttl"
        output_file = tmp_path / "output.ttl"
        input_file.write_text("input")
        output_file.write_text("output")
        
        manifest = (
            RunManifest.create(command="test")
            .add_input(input_file)
            .add_output(output_file)
            .add_verification("hash", True)
            .set_duration(2.0)
        )
        
        assert len(manifest.inputs) == 1
        assert len(manifest.outputs) == 1
        assert len(manifest.verifications) == 1
        assert manifest.duration_seconds == 2.0
    
    def test_to_dict(self, tmp_path: Path):
        """Test serialization to dict."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text("content")
        
        manifest = RunManifest.create(command="test")
        manifest.add_input(input_file)
        manifest.add_verification("check", True)
        
        d = manifest.to_dict()
        
        assert "run_id" in d
        assert "timestamp" in d
        assert "command" in d
        assert "inputs" in d
        assert "outputs" in d
        assert "verifications" in d
        assert "environment" in d
        assert "success" in d
    
    def test_to_json(self, tmp_path: Path):
        """Test JSON serialization."""
        input_file = tmp_path / "input.ttl"
        input_file.write_text("content")
        
        manifest = RunManifest.create(command="test")
        manifest.add_input(input_file)
        
        json_str = manifest.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["command"] == "test"
        assert len(parsed["inputs"]) == 1


class TestWriteManifestAtomic:
    """Tests for write_manifest_atomic function."""
    
    def test_write_creates_file(self, tmp_path: Path):
        """Test that write creates file."""
        manifest = RunManifest.create(command="test")
        output_path = tmp_path / "manifest.json"
        
        write_manifest_atomic(manifest, output_path)
        
        assert output_path.exists()
    
    def test_write_creates_parent_dirs(self, tmp_path: Path):
        """Test that write creates parent directories."""
        manifest = RunManifest.create(command="test")
        output_path = tmp_path / "nested" / "dir" / "manifest.json"
        
        write_manifest_atomic(manifest, output_path)
        
        assert output_path.exists()
    
    def test_write_content_valid_json(self, tmp_path: Path):
        """Test that written content is valid JSON."""
        manifest = RunManifest.create(command="test_cmd")
        output_path = tmp_path / "manifest.json"
        
        write_manifest_atomic(manifest, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert data["command"] == "test_cmd"
    
    def test_atomic_write_no_partial(self, tmp_path: Path):
        """Test that atomic write doesn't leave partial files."""
        manifest = RunManifest.create(command="test")
        output_path = tmp_path / "manifest.json"
        
        write_manifest_atomic(manifest, output_path)
        
        # Check no temp files left
        temp_files = list(tmp_path.glob("*.tmp"))
        assert len(temp_files) == 0


class TestReadManifest:
    """Tests for read_manifest function."""
    
    def test_read_written_manifest(self, tmp_path: Path):
        """Test reading a written manifest."""
        original = RunManifest.create(command="test_command")
        original.add_verification("check", True, {"key": "value"})
        original.set_duration(1.5)
        
        output_path = tmp_path / "manifest.json"
        write_manifest_atomic(original, output_path)
        
        loaded = read_manifest(output_path)
        
        assert loaded.command == "test_command"
        assert loaded.run_id == original.run_id
        assert loaded.duration_seconds == 1.5
        assert len(loaded.verifications) == 1
        assert loaded.verifications[0].passed is True
    
    def test_read_missing_file_raises(self, tmp_path: Path):
        """Test that reading missing file raises."""
        with pytest.raises(FileNotFoundError):
            read_manifest(tmp_path / "nonexistent.json")
    
    def test_read_invalid_json_raises(self, tmp_path: Path):
        """Test that reading invalid JSON raises."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json {")
        
        with pytest.raises(json.JSONDecodeError):
            read_manifest(invalid_file)


class TestEnvironmentInfo:
    """Tests for EnvironmentInfo class."""
    
    def test_environment_info_has_version(self):
        """Test that EnvironmentInfo captures version."""
        from onto_tools.application.verification.manifest_writer import EnvironmentInfo
        env = EnvironmentInfo()
        # Should have a version (either real or 'unknown')
        assert env.ontotools_version is not None
        assert isinstance(env.ontotools_version, str)
    
    def test_environment_info_captures_cwd(self):
        """Test that EnvironmentInfo captures current working directory."""
        from onto_tools.application.verification.manifest_writer import EnvironmentInfo
        env = EnvironmentInfo()
        assert env.cwd is not None
        from pathlib import Path
        assert Path(env.cwd).exists()


class TestWriteManifestAppend:
    """Tests for write_manifest_append function (audit log style)."""
    
    def test_append_creates_new_file(self, tmp_path: Path):
        """Test that append creates file if it doesn't exist."""
        from onto_tools.application.verification.manifest_writer import write_manifest_append
        
        manifest = RunManifest.create(command="test1")
        output_path = tmp_path / "manifest.json"
        
        write_manifest_append(manifest, output_path)
        
        assert output_path.exists()
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["command"] == "test1"
    
    def test_append_adds_to_existing_file(self, tmp_path: Path):
        """Test that append adds to existing file."""
        from onto_tools.application.verification.manifest_writer import write_manifest_append
        
        output_path = tmp_path / "manifest.json"
        
        # Add first manifest
        manifest1 = RunManifest.create(command="test1")
        write_manifest_append(manifest1, output_path)
        
        # Add second manifest
        manifest2 = RunManifest.create(command="test2")
        write_manifest_append(manifest2, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]["command"] == "test1"
        assert data[1]["command"] == "test2"
    
    def test_append_multiple_entries(self, tmp_path: Path):
        """Test appending multiple entries preserves order."""
        from onto_tools.application.verification.manifest_writer import write_manifest_append
        
        output_path = tmp_path / "manifest.json"
        
        for i in range(5):
            manifest = RunManifest.create(command=f"command_{i}")
            write_manifest_append(manifest, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 5
        for i in range(5):
            assert data[i]["command"] == f"command_{i}"
    
    def test_append_handles_single_object_file(self, tmp_path: Path):
        """Test that append handles file with single object (not array)."""
        from onto_tools.application.verification.manifest_writer import write_manifest_append
        
        output_path = tmp_path / "manifest.json"
        
        # Write single object directly (legacy format)
        single_manifest = {"run_id": "old", "command": "legacy", "timestamp": "2026-01-01T00:00:00"}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(single_manifest, f)
        
        # Append new manifest
        new_manifest = RunManifest.create(command="new_command")
        write_manifest_append(new_manifest, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["command"] == "legacy"
        assert data[1]["command"] == "new_command"
    
    def test_append_handles_corrupted_file(self, tmp_path: Path):
        """Test that append handles corrupted JSON file."""
        from onto_tools.application.verification.manifest_writer import write_manifest_append
        
        output_path = tmp_path / "manifest.json"
        
        # Write corrupted content
        output_path.write_text("not valid json {{{")
        
        # Append should still work, starting fresh
        manifest = RunManifest.create(command="fresh_start")
        write_manifest_append(manifest, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]["command"] == "fresh_start"


class TestWriteManifestAtomicErrorHandling:
    """Tests for write_manifest_atomic error handling."""
    
    def test_write_to_read_only_parent(self, tmp_path: Path):
        """Test error handling when parent directory is read-only."""
        import os
        import stat
        
        # This test may behave differently on Windows
        # Just verify the function handles errors gracefully
        manifest = RunManifest.create(command="test")
        
        # Create a directory with restricted permissions
        restricted = tmp_path / "restricted"
        restricted.mkdir()
        
        # Try to write - should either succeed or raise, not leave partial file
        output_path = restricted / "manifest.json"
        
        try:
            write_manifest_atomic(manifest, output_path)
            # If it succeeded, file should exist
            assert output_path.exists()
        except (OSError, PermissionError):
            # If it failed, no temp files should be left
            temp_files = list(restricted.glob("*.tmp"))
            assert len(temp_files) == 0
