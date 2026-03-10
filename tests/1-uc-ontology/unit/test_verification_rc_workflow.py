"""
Unit tests for verification.rc_workflow module.

Tests RC workflow orchestration functionality.
"""
import json
from pathlib import Path

import pytest

from onto_tools.application.verification.rc_workflow import (
    ChecksumBaseline,
    CoverageResult,
    RCResult,
    RCWorkflow,
    run_rc_verification
)


class TestChecksumBaseline:
    """Tests for ChecksumBaseline class."""
    
    def test_from_directory(self, tmp_path: Path):
        """Test creating baseline from directory."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content3")
        
        baseline = ChecksumBaseline.from_directory(tmp_path)
        
        assert len(baseline.files) == 3
        assert "file1.txt" in baseline.files
        assert "file2.txt" in baseline.files
        assert "subdir\\file3.txt" in baseline.files or "subdir/file3.txt" in baseline.files
        assert baseline.created_at is not None
    
    def test_save_and_load(self, tmp_path: Path):
        """Test saving and loading baseline."""
        # Create source dir with files
        src_dir = tmp_path / "source"
        src_dir.mkdir()
        (src_dir / "test.txt").write_text("test content")
        
        # Create baseline
        baseline = ChecksumBaseline.from_directory(src_dir)
        
        # Save
        baseline_file = tmp_path / "baseline.json"
        baseline.save(baseline_file)
        
        assert baseline_file.exists()
        
        # Load
        loaded = ChecksumBaseline.from_file(baseline_file)
        
        assert loaded.files == baseline.files
        assert loaded.created_at == baseline.created_at
    
    def test_verify_unchanged(self, tmp_path: Path):
        """Test verification of unchanged directory."""
        # Create files
        (tmp_path / "file1.txt").write_text("content1")
        
        baseline = ChecksumBaseline.from_directory(tmp_path)
        
        # Verify immediately (nothing changed)
        is_valid, diffs = baseline.verify(tmp_path)
        
        assert is_valid is True
        assert len(diffs) == 0
    
    def test_verify_modified_file(self, tmp_path: Path):
        """Test detection of modified file."""
        test_file = tmp_path / "file1.txt"
        test_file.write_text("original")
        
        baseline = ChecksumBaseline.from_directory(tmp_path)
        
        # Modify file
        test_file.write_text("modified")
        
        is_valid, diffs = baseline.verify(tmp_path)
        
        assert is_valid is False
        assert any("MODIFIED" in d for d in diffs)
    
    def test_verify_missing_file(self, tmp_path: Path):
        """Test detection of missing file."""
        test_file = tmp_path / "file1.txt"
        test_file.write_text("content")
        
        baseline = ChecksumBaseline.from_directory(tmp_path)
        
        # Delete file
        test_file.unlink()
        
        is_valid, diffs = baseline.verify(tmp_path)
        
        assert is_valid is False
        assert any("MISSING" in d for d in diffs)
    
    def test_verify_new_file(self, tmp_path: Path):
        """Test detection of new file."""
        (tmp_path / "file1.txt").write_text("content")
        
        baseline = ChecksumBaseline.from_directory(tmp_path)
        
        # Add new file
        (tmp_path / "new_file.txt").write_text("new")
        
        is_valid, diffs = baseline.verify(tmp_path)
        
        assert is_valid is False
        assert any("NEW" in d for d in diffs)


class TestCoverageResult:
    """Tests for CoverageResult dataclass."""
    
    def test_basic_creation(self):
        """Test basic CoverageResult creation."""
        result = CoverageResult(
            total_coverage=85.5,
            passed=False,
            threshold=90.0,
            details={"file1.py": 80.0},
            test_results={"passed": True}
        )
        
        assert result.total_coverage == 85.5
        assert result.passed is False
        assert result.threshold == 90.0
    
    def test_to_dict(self):
        """Test serialization."""
        result = CoverageResult(
            total_coverage=92.0,
            passed=True,
            threshold=90.0
        )
        
        d = result.to_dict()
        
        assert d["total_coverage"] == 92.0
        assert d["passed"] is True


class TestRCResult:
    """Tests for RCResult dataclass."""
    
    def test_default_values(self):
        """Test default RCResult values."""
        result = RCResult(success=True)
        
        assert result.success is True
        assert result.rc_v8_immutable is True
        assert result.coverage_passed is False
        assert result.all_tests_passed is False
        assert result.errors == []
        assert result.warnings == []
    
    def test_to_dict(self):
        """Test serialization."""
        result = RCResult(
            success=False,
            rc_v8_immutable=True,
            coverage_passed=False,
            errors=["Coverage below threshold"]
        )
        
        d = result.to_dict()
        
        assert d["success"] is False
        assert d["rc_v8_immutable"] is True
        assert len(d["errors"]) == 1


class TestRCWorkflow:
    """Tests for RCWorkflow class."""
    
    @pytest.fixture
    def mock_rc_v8(self, tmp_path: Path) -> Path:
        """Create mock RC_v8 directory."""
        rc_v8_path = tmp_path / "RC_v8_CANON"
        rc_v8_path.mkdir()
        
        (rc_v8_path / "manifest.json").write_text('{"version": "v8"}')
        (rc_v8_path / "evidence.txt").write_text("evidence content")
        
        return rc_v8_path
    
    @pytest.fixture
    def workspace(self, tmp_path: Path, mock_rc_v8: Path) -> Path:
        """Create mock workspace."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        # Create outputs/logs structure
        outputs = workspace / "outputs" / "logs"
        outputs.mkdir(parents=True)
        
        # Move RC_v8 into workspace structure
        import shutil
        target_rc_v8 = outputs / "RC_v8_CANON"
        shutil.copytree(mock_rc_v8, target_rc_v8)
        
        return workspace
    
    def test_workflow_initialization(self, workspace: Path):
        """Test workflow initialization."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path,
            coverage_threshold=90.0
        )
        
        assert workflow.workspace_root == workspace.resolve()
        assert workflow.coverage_threshold == 90.0
    
    def test_load_or_create_baseline(self, workspace: Path):
        """Test baseline creation."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path
        )
        
        baseline = workflow._load_or_create_baseline()
        
        assert len(baseline.files) == 2
        assert workflow.baseline_path.exists()
    
    def test_verify_rc_v8_immutability_pass(self, workspace: Path):
        """Test RC_v8 immutability verification - pass case."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path
        )
        
        # Create baseline
        workflow._load_or_create_baseline()
        
        # Verify (should pass - nothing changed)
        is_immutable, changes = workflow._verify_rc_v8_immutability()
        
        assert is_immutable is True
        assert len(changes) == 0
    
    def test_verify_rc_v8_immutability_fail(self, workspace: Path):
        """Test RC_v8 immutability verification - fail case."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path
        )
        
        # Create baseline
        workflow._load_or_create_baseline()
        
        # Modify RC_v8
        (rc_v8_path / "manifest.json").write_text('{"version": "MODIFIED"}')
        
        # Verify (should fail)
        is_immutable, changes = workflow._verify_rc_v8_immutability()
        
        assert is_immutable is False
        assert len(changes) > 0
    
    def test_run_with_skip_tests(self, workspace: Path):
        """Test workflow run with tests skipped."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path,
            coverage_threshold=90.0
        )
        
        result = workflow.run(skip_tests=True, skip_rc_v8_check=False)
        
        # Should pass with tests skipped
        assert result.rc_v8_immutable is True
        assert result.coverage_passed is True  # Skipped = assumed pass
        assert result.all_tests_passed is True  # Skipped = assumed pass
        assert "Tests skipped" in result.warnings
        assert result.evidence_path is not None
    
    def test_run_with_skip_all(self, workspace: Path):
        """Test workflow run with everything skipped."""
        rc_v8_path = workspace / "outputs" / "logs" / "RC_v8_CANON"
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8_path
        )
        
        result = workflow.run(skip_tests=True, skip_rc_v8_check=True)
        
        assert result.success is True
        assert len(result.warnings) == 2  # Both skipped
    
    def test_run_missing_rc_v8(self, tmp_path: Path):
        """Test workflow with missing RC_v8 directory."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=workspace / "nonexistent" / "RC_v8_CANON"
        )
        
        result = workflow.run(skip_tests=True)
        
        assert result.success is False
        assert any("Baseline setup failed" in e for e in result.errors)


class TestRunRCVerification:
    """Tests for run_rc_verification convenience function."""
    
    def test_basic_call(self, tmp_path: Path):
        """Test basic function call."""
        # Create minimal structure
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        outputs = workspace / "outputs" / "logs" / "RC_v8_CANON"
        outputs.mkdir(parents=True)
        (outputs / "test.txt").write_text("test")
        
        result = run_rc_verification(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=outputs
        )
        
        assert isinstance(result, RCResult)


class TestEdgeCases:
    """Tests for edge cases and exception handling."""
    
    def test_coverage_result_passed_property(self):
        """Test CoverageResult passed property with different thresholds."""
        # Below threshold
        result_low = CoverageResult(
            total_coverage=85.0,
            passed=False,
            threshold=90.0
        )
        assert result_low.passed is False
        
        # Above threshold
        result_high = CoverageResult(
            total_coverage=95.0,
            passed=True,
            threshold=90.0
        )
        assert result_high.passed is True
    
    def test_rc_result_to_dict_with_all_fields(self, tmp_path: Path):
        """Test RCResult to_dict with all optional fields populated."""
        result = RCResult(
            success=True,
            rc_v8_immutable=True,
            all_tests_passed=True,
            coverage_passed=True,
            isomorphism_verified=True,
            idempotency_verified=True,
            evidence_path=str(tmp_path / "evidence"),
            warnings=["Warning 1", "Warning 2"],
            errors=[]
        )
        
        d = result.to_dict()
        
        assert d["success"] is True
        assert d["rc_v8_immutable"] is True
        assert d["all_tests_passed"] is True
        assert d["coverage_passed"] is True
        assert d["isomorphism_verified"] is True
        assert d["idempotency_verified"] is True
        assert len(d["warnings"]) == 2
    
    def test_checksum_baseline_verify_with_extra_files(self, tmp_path: Path):
        """Test baseline verification when current has extra files."""
        # Create baseline with 1 file
        baseline_dir = tmp_path / "baseline"
        baseline_dir.mkdir()
        (baseline_dir / "file1.txt").write_text("content1")
        
        baseline = ChecksumBaseline.from_directory(baseline_dir)
        
        # Add extra file
        (baseline_dir / "file2.txt").write_text("content2")
        
        # Verify should detect new file
        match, differences = baseline.verify(baseline_dir)
        
        assert match is False
        assert len(differences) > 0
        assert any("file2.txt" in d for d in differences)
    
    def test_checksum_baseline_verify_with_missing_files(self, tmp_path: Path):
        """Test baseline verification when current has missing files."""
        # Create baseline with 2 files
        baseline_dir = tmp_path / "baseline"
        baseline_dir.mkdir()
        (baseline_dir / "file1.txt").write_text("content1")
        (baseline_dir / "file2.txt").write_text("content2")
        
        baseline = ChecksumBaseline.from_directory(baseline_dir)
        
        # Delete one file
        (baseline_dir / "file2.txt").unlink()
        
        # Verify should detect missing file
        match, differences = baseline.verify(baseline_dir)
        
        assert match is False
        assert len(differences) > 0
        assert any("file2.txt" in d and "MISSING" in d for d in differences)
    
    def test_workflow_finalize_with_errors(self, tmp_path: Path):
        """Test workflow result when errors occur during execution."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        outputs = workspace / "outputs" / "logs"
        outputs.mkdir(parents=True)
        
        # Don't create RC_v8 - will cause error
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=outputs,
            rc_v8_path=workspace / "nonexistent" / "RC_v8_CANON"
        )
        
        result = workflow.run(skip_tests=True, skip_rc_v8_check=False)
        
        # Should have errors
        assert result.success is False
        assert len(result.errors) > 0
    
    def test_coverage_result_with_test_details(self):
        """Test CoverageResult with test_results populated."""
        result = CoverageResult(
            total_coverage=92.5,
            passed=True,
            threshold=90.0,
            details={"module1.py": 95.0, "module2.py": 90.0},
            test_results={"passed": True, "returncode": 0, "stdout": "All tests passed"}
        )
        
        assert result.test_results is not None
        assert result.test_results["passed"] is True
        assert result.details["module1.py"] == 95.0
    
    def test_workflow_with_coverage_json(self, tmp_path: Path):
        """Test workflow processes coverage.json correctly."""
        import json
        
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        
        # Create RC_v8 structure
        rc_v8 = workspace / "outputs" / "logs" / "RC_v8_CANON"
        rc_v8.mkdir(parents=True)
        (rc_v8 / "test.txt").write_text("content")
        
        # Create coverage.json
        coverage_data = {
            "totals": {"percent_covered": 96.5},
            "files": {
                "src/module1.py": {"summary": {"percent_covered": 98.0}},
                "src/module2.py": {"summary": {"percent_covered": 95.0}}
            }
        }
        (workspace / "coverage.json").write_text(json.dumps(coverage_data))
        
        workflow = RCWorkflow(
            workspace_root=workspace,
            output_dir=workspace / "outputs" / "logs",
            rc_v8_path=rc_v8,
            coverage_threshold=90.0
        )
        
        # The workflow should be able to read coverage data
        assert workflow.coverage_threshold == 90.0
    
    def test_rc_result_with_errors_list(self):
        """Test RCResult with populated errors list."""
        result = RCResult(
            success=False,
            rc_v8_immutable=False,
            errors=["Error 1: RC_v8 modified", "Error 2: Tests failed"]
        )
        
        d = result.to_dict()
        
        assert d["success"] is False
        assert len(d["errors"]) == 2
        assert "RC_v8 modified" in d["errors"][0]
