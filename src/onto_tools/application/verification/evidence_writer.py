"""
EvidenceWriter - Aggregate and organize verification evidence files.

Manages output directory structure and evidence collection for RC runs.
"""
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .hasher import sha256_file
from .manifest_writer import RunManifest, write_manifest_atomic


@dataclass
class EvidenceFile:
    """
    Metadata for an evidence file.
    
    Attributes:
        filename: Name of the file
        path: Full path to the file
        sha256: SHA256 hash of the file
        file_type: Type of evidence (manifest, report, artifact, log)
        description: Human-readable description
    """
    filename: str
    path: str
    sha256: str
    file_type: str
    description: Optional[str] = None


@dataclass
class EvidenceBundle:
    """
    Bundle of all evidence files from a run.
    
    Attributes:
        bundle_id: Unique identifier for this bundle
        created_at: ISO 8601 timestamp
        base_path: Base directory for evidence
        files: List of evidence files
        summary: Summary of the run
    """
    bundle_id: str
    created_at: str
    base_path: str
    files: List[EvidenceFile] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "bundle_id": self.bundle_id,
            "created_at": self.created_at,
            "base_path": self.base_path,
            "files": [
                {
                    "filename": f.filename,
                    "path": f.path,
                    "sha256": f.sha256,
                    "file_type": f.file_type,
                    "description": f.description
                }
                for f in self.files
            ],
            "summary": self.summary
        }


class EvidenceWriter:
    """
    Manages evidence file organization and writing.
    
    Creates a structured output directory with:
    - run_manifest.json - Main run manifest
    - artifacts/ - Output artifacts (canonical ontologies, etc.)
    - reports/ - Verification reports
    - logs/ - Execution logs
    - evidence_index.json - Index of all evidence files
    
    Example:
        >>> writer = EvidenceWriter("outputs/RC_v9_CANON/run_20260130")
        >>> writer.write_manifest(manifest)
        >>> writer.copy_artifact(output_file, "canonical_ontology.ttl")
        >>> writer.write_report("isomorphism", iso_report.to_dict())
        >>> bundle = writer.finalize()
    """
    
    def __init__(self, base_path: Union[str, Path], run_id: Optional[str] = None):
        """
        Initialize EvidenceWriter.
        
        Args:
            base_path: Base directory for evidence output
            run_id: Optional run ID (auto-generated if not provided)
        """
        self.base_path = Path(base_path)
        self.run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.created_at = datetime.now(timezone.utc).isoformat()
        
        self._files: List[EvidenceFile] = []
        self._initialized = False
    
    def _ensure_dirs(self) -> None:
        """Create directory structure if not exists."""
        if self._initialized:
            return
        
        self.base_path.mkdir(parents=True, exist_ok=True)
        (self.base_path / "artifacts").mkdir(exist_ok=True)
        (self.base_path / "reports").mkdir(exist_ok=True)
        (self.base_path / "logs").mkdir(exist_ok=True)
        
        self._initialized = True
    
    def write_manifest(self, manifest: RunManifest) -> Path:
        """
        Write the main run manifest.
        
        Args:
            manifest: RunManifest to write
            
        Returns:
            Path to written manifest file
        """
        self._ensure_dirs()
        
        manifest_path = self.base_path / "run_manifest.json"
        write_manifest_atomic(manifest, manifest_path)
        
        self._files.append(EvidenceFile(
            filename="run_manifest.json",
            path=str(manifest_path),
            sha256=sha256_file(manifest_path),
            file_type="manifest",
            description="Main run manifest with inputs, outputs, and verifications"
        ))
        
        return manifest_path
    
    def copy_artifact(
        self,
        source: Union[str, Path],
        target_name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Path:
        """
        Copy an artifact to the evidence directory.
        
        Args:
            source: Source file path
            target_name: Target filename (uses source name if not provided)
            description: Optional description
            
        Returns:
            Path to copied artifact
        """
        self._ensure_dirs()
        
        source = Path(source)
        target_name = target_name or source.name
        target_path = self.base_path / "artifacts" / target_name
        
        shutil.copy2(source, target_path)
        
        self._files.append(EvidenceFile(
            filename=target_name,
            path=str(target_path),
            sha256=sha256_file(target_path),
            file_type="artifact",
            description=description
        ))
        
        return target_path
    
    def write_report(
        self,
        report_type: str,
        data: Dict[str, Any],
        description: Optional[str] = None
    ) -> Path:
        """
        Write a verification report.
        
        Args:
            report_type: Type of report (e.g., 'isomorphism', 'idempotency')
            data: Report data (will be JSON serialized)
            description: Optional description
            
        Returns:
            Path to written report file
        """
        self._ensure_dirs()
        
        filename = f"{report_type}_report.json"
        report_path = self.base_path / "reports" / filename
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self._files.append(EvidenceFile(
            filename=filename,
            path=str(report_path),
            sha256=sha256_file(report_path),
            file_type="report",
            description=description or f"{report_type} verification report"
        ))
        
        return report_path
    
    def write_log(
        self,
        log_name: str,
        content: str,
        description: Optional[str] = None
    ) -> Path:
        """
        Write a log file.
        
        Args:
            log_name: Name for the log file (without extension)
            content: Log content
            description: Optional description
            
        Returns:
            Path to written log file
        """
        self._ensure_dirs()
        
        filename = f"{log_name}.log"
        log_path = self.base_path / "logs" / filename
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self._files.append(EvidenceFile(
            filename=filename,
            path=str(log_path),
            sha256=sha256_file(log_path),
            file_type="log",
            description=description
        ))
        
        return log_path
    
    def add_existing_file(
        self,
        path: Union[str, Path],
        file_type: str,
        description: Optional[str] = None
    ) -> None:
        """
        Register an existing file as evidence.
        
        Args:
            path: Path to existing file
            file_type: Type of file (artifact, report, log, etc.)
            description: Optional description
        """
        path = Path(path)
        
        self._files.append(EvidenceFile(
            filename=path.name,
            path=str(path),
            sha256=sha256_file(path),
            file_type=file_type,
            description=description
        ))
    
    def finalize(self, summary: Optional[Dict[str, Any]] = None) -> EvidenceBundle:
        """
        Finalize the evidence bundle and write index.
        
        Args:
            summary: Optional summary data to include
            
        Returns:
            EvidenceBundle with all collected evidence
        """
        self._ensure_dirs()
        
        bundle = EvidenceBundle(
            bundle_id=self.run_id,
            created_at=self.created_at,
            base_path=str(self.base_path),
            files=self._files,
            summary=summary or {}
        )
        
        # Write evidence index
        index_path = self.base_path / "evidence_index.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(bundle.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Add index to files list
        bundle.files.append(EvidenceFile(
            filename="evidence_index.json",
            path=str(index_path),
            sha256=sha256_file(index_path),
            file_type="index",
            description="Index of all evidence files in this bundle"
        ))
        
        return bundle


def create_rc_evidence_directory(
    base_output_dir: Union[str, Path],
    run_name: Optional[str] = None
) -> EvidenceWriter:
    """
    Create an evidence writer for RC verification runs.
    
    Creates structure under: base_output_dir/RC_v9_CANON/<run_name>/
    
    Args:
        base_output_dir: Base output directory (e.g., 'outputs/logs')
        run_name: Optional run name (auto-generated if not provided)
        
    Returns:
        Configured EvidenceWriter
        
    Example:
        >>> writer = create_rc_evidence_directory("outputs/logs")
        >>> # Creates: outputs/logs/RC_v9_CANON/run_20260130_123456/
    """
    base_output_dir = Path(base_output_dir)
    run_name = run_name or f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    
    evidence_path = base_output_dir / "RC_v9_CANON" / run_name
    
    return EvidenceWriter(evidence_path, run_id=run_name)
