"""
Unit tests for verification.evidence_writer module.

Tests evidence bundle creation and file organization.
"""
import json
from datetime import datetime
from pathlib import Path

import pytest

from onto_tools.application.verification.evidence_writer import (
    EvidenceWriter,
    EvidenceFile,
    EvidenceBundle,
    create_rc_evidence_directory
)
from onto_tools.application.verification.manifest_writer import RunManifest


class TestEvidenceFile:
    """Tests for EvidenceFile dataclass."""
    
    def test_basic_creation(self):
        """Test basic EvidenceFile creation."""
        ef = EvidenceFile(
            filename="test.json",
            path="/path/to/test.json",
            sha256="ABC123",
            file_type="manifest",
            description="Test file"
        )
        
        assert ef.filename == "test.json"
        assert ef.path == "/path/to/test.json"
        assert ef.sha256 == "ABC123"
        assert ef.file_type == "manifest"
        assert ef.description == "Test file"


class TestEvidenceBundle:
    """Tests for EvidenceBundle dataclass."""
    
    def test_basic_creation(self):
        """Test basic EvidenceBundle creation."""
        bundle = EvidenceBundle(
            bundle_id="test_123",
            created_at="2026-01-30T12:00:00Z",
            base_path="/path/to/evidence"
        )
        
        assert bundle.bundle_id == "test_123"
        assert bundle.files == []
        assert bundle.summary == {}
    
    def test_to_dict(self):
        """Test bundle serialization."""
        bundle = EvidenceBundle(
            bundle_id="test_123",
            created_at="2026-01-30T12:00:00Z",
            base_path="/path/to/evidence",
            files=[
                EvidenceFile(
                    filename="test.json",
                    path="/path/test.json",
                    sha256="ABC",
                    file_type="manifest"
                )
            ],
            summary={"status": "success"}
        )
        
        d = bundle.to_dict()
        
        assert d["bundle_id"] == "test_123"
        assert len(d["files"]) == 1
        assert d["summary"]["status"] == "success"


class TestEvidenceWriter:
    """Tests for EvidenceWriter class."""
    
    def test_initialization(self, tmp_path: Path):
        """Test EvidenceWriter initialization."""
        writer = EvidenceWriter(tmp_path / "evidence")
        
        assert writer.base_path == tmp_path / "evidence"
        assert writer.run_id is not None
    
    def test_custom_run_id(self, tmp_path: Path):
        """Test custom run ID."""
        writer = EvidenceWriter(tmp_path / "evidence", run_id="custom_id")
        
        assert writer.run_id == "custom_id"
    
    def test_write_manifest(self, tmp_path: Path):
        """Test writing manifest."""
        writer = EvidenceWriter(tmp_path / "evidence")
        manifest = RunManifest.create(command="test")
        
        manifest_path = writer.write_manifest(manifest)
        
        assert manifest_path.exists()
        assert manifest_path.name == "run_manifest.json"
        
        with open(manifest_path, "r") as f:
            data = json.load(f)
        assert data["command"] == "test"
    
    def test_copy_artifact(self, tmp_path: Path):
        """Test copying artifact."""
        # Create source file
        source = tmp_path / "source.ttl"
        source.write_text("@prefix ex: <http://example.org/> .")
        
        # Create evidence writer
        writer = EvidenceWriter(tmp_path / "evidence")
        
        artifact_path = writer.copy_artifact(source, "copied.ttl", "Test artifact")
        
        assert artifact_path.exists()
        assert artifact_path.parent.name == "artifacts"
        assert artifact_path.read_text() == source.read_text()
    
    def test_copy_artifact_default_name(self, tmp_path: Path):
        """Test copying artifact with default name."""
        source = tmp_path / "original.ttl"
        source.write_text("content")
        
        writer = EvidenceWriter(tmp_path / "evidence")
        
        artifact_path = writer.copy_artifact(source)
        
        assert artifact_path.name == "original.ttl"
    
    def test_write_report(self, tmp_path: Path):
        """Test writing report."""
        writer = EvidenceWriter(tmp_path / "evidence")
        
        report_data = {
            "check": "isomorphism",
            "passed": True,
            "details": {"count": 100}
        }
        
        report_path = writer.write_report("isomorphism", report_data)
        
        assert report_path.exists()
        assert report_path.parent.name == "reports"
        assert report_path.name == "isomorphism_report.json"
        
        with open(report_path, "r") as f:
            loaded = json.load(f)
        assert loaded["passed"] is True
    
    def test_write_log(self, tmp_path: Path):
        """Test writing log."""
        writer = EvidenceWriter(tmp_path / "evidence")
        
        log_content = "Line 1\nLine 2\nLine 3"
        
        log_path = writer.write_log("execution", log_content)
        
        assert log_path.exists()
        assert log_path.parent.name == "logs"
        assert log_path.name == "execution.log"
        assert log_path.read_text() == log_content
    
    def test_add_existing_file(self, tmp_path: Path):
        """Test registering existing file."""
        existing = tmp_path / "existing.txt"
        existing.write_text("existing content")
        
        writer = EvidenceWriter(tmp_path / "evidence")
        writer.add_existing_file(existing, "external", "External file")
        
        # Should be in files list
        assert len(writer._files) == 1
        assert writer._files[0].filename == "existing.txt"
        assert writer._files[0].file_type == "external"
    
    def test_finalize_creates_index(self, tmp_path: Path):
        """Test finalize creates evidence index."""
        writer = EvidenceWriter(tmp_path / "evidence")
        
        # Add some content
        manifest = RunManifest.create(command="test")
        writer.write_manifest(manifest)
        
        writer.write_report("test", {"result": "pass"})
        
        # Finalize
        bundle = writer.finalize(summary={"overall": "success"})
        
        # Check index exists
        index_path = tmp_path / "evidence" / "evidence_index.json"
        assert index_path.exists()
        
        with open(index_path, "r") as f:
            index_data = json.load(f)
        
        assert index_data["bundle_id"] == writer.run_id
        assert len(index_data["files"]) >= 2  # manifest + report + index
        assert index_data["summary"]["overall"] == "success"
    
    def test_finalize_returns_bundle(self, tmp_path: Path):
        """Test finalize returns EvidenceBundle."""
        writer = EvidenceWriter(tmp_path / "evidence")
        manifest = RunManifest.create(command="test")
        writer.write_manifest(manifest)
        
        bundle = writer.finalize()
        
        assert isinstance(bundle, EvidenceBundle)
        assert bundle.bundle_id == writer.run_id
        assert len(bundle.files) >= 1
    
    def test_directory_structure_created(self, tmp_path: Path):
        """Test directory structure is created."""
        writer = EvidenceWriter(tmp_path / "evidence")
        
        # Trigger directory creation
        manifest = RunManifest.create(command="test")
        writer.write_manifest(manifest)
        
        assert (tmp_path / "evidence").exists()
        assert (tmp_path / "evidence" / "artifacts").exists()
        assert (tmp_path / "evidence" / "reports").exists()
        assert (tmp_path / "evidence" / "logs").exists()


class TestCreateRCEvidenceDirectory:
    """Tests for create_rc_evidence_directory function."""
    
    def test_creates_correct_path(self, tmp_path: Path):
        """Test that correct path structure is created."""
        writer = create_rc_evidence_directory(tmp_path, "test_run")
        
        expected_path = tmp_path / "RC_v9_CANON" / "test_run"
        assert writer.base_path == expected_path
    
    def test_auto_generated_run_name(self, tmp_path: Path):
        """Test auto-generated run name."""
        writer = create_rc_evidence_directory(tmp_path)
        
        # Should have RC_v9_CANON in path
        assert "RC_v9_CANON" in str(writer.base_path)
        
        # Run name should start with "run_"
        assert "run_" in writer.base_path.name
    
    def test_writer_functional(self, tmp_path: Path):
        """Test that returned writer is functional."""
        writer = create_rc_evidence_directory(tmp_path, "functional_test")
        
        manifest = RunManifest.create(command="test")
        manifest_path = writer.write_manifest(manifest)
        
        assert manifest_path.exists()
        assert "RC_v9_CANON" in str(manifest_path)
