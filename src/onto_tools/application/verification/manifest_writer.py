"""
ManifestWriter - Generate run_manifest.json for pipeline executions.

Provides structured evidence capture for reproducibility and audit.
Implements atomic writes via temp file + rename pattern.
"""
import json
import os
import tempfile
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import platform
import sys

from .hasher import sha256_file


@dataclass
class InputArtifact:
    """
    Input artifact metadata.
    
    Attributes:
        path: Relative or absolute path to input file
        sha256: SHA256 hash of input file at time of run
        size_bytes: File size in bytes
        format: File format (e.g., 'turtle', 'json')
    """
    path: str
    sha256: str
    size_bytes: int
    format: Optional[str] = None
    
    @classmethod
    def from_file(cls, path: Union[str, Path], format: Optional[str] = None) -> "InputArtifact":
        """Create InputArtifact from a file."""
        path = Path(path)
        return cls(
            path=str(path),
            sha256=sha256_file(path),
            size_bytes=path.stat().st_size,
            format=format or cls._detect_format(path)
        )
    
    @staticmethod
    def _detect_format(path: Path) -> str:
        """Auto-detect format from extension."""
        ext_map = {
            ".ttl": "turtle",
            ".turtle": "turtle",
            ".n3": "n3",
            ".nt": "ntriples",
            ".rdf": "rdfxml",
            ".xml": "rdfxml",
            ".owl": "rdfxml",
            ".json": "json",
            ".jsonld": "json-ld",
        }
        return ext_map.get(path.suffix.lower(), "unknown")


@dataclass
class OutputArtifact:
    """
    Output artifact metadata.
    
    Attributes:
        path: Relative or absolute path to output file
        sha256: SHA256 hash of output file after generation
        size_bytes: File size in bytes
        format: File format
        artifact_type: Type of artifact (e.g., 'canonical_ontology', 'report')
    """
    path: str
    sha256: str
    size_bytes: int
    format: Optional[str] = None
    artifact_type: Optional[str] = None
    
    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        artifact_type: Optional[str] = None,
        format: Optional[str] = None
    ) -> "OutputArtifact":
        """Create OutputArtifact from a file."""
        path = Path(path)
        return cls(
            path=str(path),
            sha256=sha256_file(path),
            size_bytes=path.stat().st_size,
            format=format or InputArtifact._detect_format(path),
            artifact_type=artifact_type
        )


@dataclass
class VerificationResult:
    """
    Result of a verification check.
    
    Attributes:
        check_type: Type of check (hash, isomorphism, idempotency)
        passed: Whether the check passed
        details: Additional details about the check
    """
    check_type: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvironmentInfo:
    """
    Execution environment information.
    
    Attributes:
        python_version: Python version string
        platform: OS platform
        hostname: Machine hostname
        cwd: Current working directory
        ontotools_version: OntoTools package version
    """
    python_version: str = field(default_factory=lambda: sys.version)
    platform: str = field(default_factory=lambda: f"{platform.system()} {platform.release()}")
    hostname: str = field(default_factory=lambda: platform.node())
    cwd: str = field(default_factory=lambda: str(Path.cwd()))
    ontotools_version: Optional[str] = None
    
    def __post_init__(self):
        if self.ontotools_version is None:
            try:
                from importlib.metadata import version
                self.ontotools_version = version("onto-tools")
            except Exception:
                self.ontotools_version = "unknown"


@dataclass
class RunManifest:
    """
    Complete manifest for a pipeline run.
    
    Captures all information needed to reproduce and verify a run.
    
    Attributes:
        run_id: Unique identifier for this run
        timestamp: ISO 8601 timestamp of run start
        command: Command or operation performed
        inputs: List of input artifacts
        outputs: List of output artifacts
        verifications: List of verification results
        environment: Execution environment info
        parameters: Command parameters
        duration_seconds: Execution duration
        success: Whether the run succeeded
        error: Error message if failed
    """
    run_id: str
    timestamp: str
    command: str
    inputs: List[InputArtifact] = field(default_factory=list)
    outputs: List[OutputArtifact] = field(default_factory=list)
    verifications: List[VerificationResult] = field(default_factory=list)
    environment: EnvironmentInfo = field(default_factory=EnvironmentInfo)
    parameters: Dict[str, Any] = field(default_factory=dict)
    duration_seconds: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    
    @classmethod
    def create(cls, command: str, **kwargs) -> "RunManifest":
        """
        Create a new RunManifest with generated ID and timestamp.
        
        Args:
            command: The command/operation name
            **kwargs: Additional manifest fields
            
        Returns:
            New RunManifest instance
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        return cls(
            run_id=run_id,
            timestamp=timestamp,
            command=command,
            **kwargs
        )
    
    def add_input(self, path: Union[str, Path], format: Optional[str] = None) -> "RunManifest":
        """Add an input artifact from file path."""
        self.inputs.append(InputArtifact.from_file(path, format))
        return self
    
    def add_output(
        self,
        path: Union[str, Path],
        artifact_type: Optional[str] = None,
        format: Optional[str] = None
    ) -> "RunManifest":
        """Add an output artifact from file path."""
        self.outputs.append(OutputArtifact.from_file(path, artifact_type, format))
        return self
    
    def add_verification(
        self,
        check_type: str,
        passed: bool,
        details: Optional[Dict[str, Any]] = None
    ) -> "RunManifest":
        """Add a verification result."""
        self.verifications.append(VerificationResult(
            check_type=check_type,
            passed=passed,
            details=details or {}
        ))
        return self
    
    def set_duration(self, seconds: float) -> "RunManifest":
        """Set execution duration."""
        self.duration_seconds = seconds
        return self
    
    def set_error(self, error: str) -> "RunManifest":
        """Mark run as failed with error message."""
        self.success = False
        self.error = error
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "command": self.command,
            "inputs": [asdict(i) for i in self.inputs],
            "outputs": [asdict(o) for o in self.outputs],
            "verifications": [asdict(v) for v in self.verifications],
            "environment": asdict(self.environment),
            "parameters": self.parameters,
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "error": self.error
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def write_manifest_atomic(
    manifest: RunManifest,
    output_path: Union[str, Path],
    indent: int = 2
) -> None:
    """
    Write manifest to file atomically.
    
    Uses temp file + rename pattern to ensure atomic writes.
    The output file will never be in a partially written state.
    
    Args:
        manifest: RunManifest to write
        output_path: Target file path
        indent: JSON indentation level
        
    Raises:
        OSError: If write fails
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    json_content = manifest.to_json(indent=indent)
    
    # Write to temp file in same directory (ensures same filesystem for rename)
    fd, temp_path = tempfile.mkstemp(
        suffix=".json.tmp",
        dir=output_path.parent
    )
    
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json_content)
        
        # Atomic rename
        Path(temp_path).replace(output_path)
        
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def write_manifest_append(
    manifest: RunManifest,
    output_path: Union[str, Path],
    indent: int = 2
) -> None:
    """
    Append manifest to file (audit log style).
    
    If file exists, reads existing entries and appends new manifest.
    If file doesn't exist, creates new file with single entry.
    Uses atomic write pattern for safety.
    
    Args:
        manifest: RunManifest to append
        output_path: Target file path
        indent: JSON indentation level
        
    Raises:
        OSError: If write fails
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing manifests if file exists
    existing_entries = []
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                # Handle both array and single object formats
                if isinstance(content, list):
                    existing_entries = content
                else:
                    existing_entries = [content]
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, start fresh
            existing_entries = []
    
    # Append new manifest
    existing_entries.append(manifest.to_dict())
    
    # Write atomically
    json_content = json.dumps(existing_entries, indent=indent, ensure_ascii=False)
    
    fd, temp_path = tempfile.mkstemp(
        suffix=".json.tmp",
        dir=output_path.parent
    )
    
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json_content)
        
        # Atomic rename
        Path(temp_path).replace(output_path)
        
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def read_manifest(path: Union[str, Path]) -> RunManifest:
    """
    Read a manifest from JSON file.
    
    Args:
        path: Path to manifest JSON file
        
    Returns:
        RunManifest instance
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(path)
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return RunManifest(
        run_id=data["run_id"],
        timestamp=data["timestamp"],
        command=data["command"],
        inputs=[InputArtifact(**i) for i in data.get("inputs", [])],
        outputs=[OutputArtifact(**o) for o in data.get("outputs", [])],
        verifications=[VerificationResult(**v) for v in data.get("verifications", [])],
        environment=EnvironmentInfo(**data.get("environment", {})),
        parameters=data.get("parameters", {}),
        duration_seconds=data.get("duration_seconds"),
        success=data.get("success", True),
        error=data.get("error")
    )
