"""
Idempotency - Verify that operations produce identical results when reapplied.

Implements idempotency checks for canonicalization and other operations.
Idempotency: f(f(x)) == f(x)
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Union
import tempfile
import shutil

from rdflib import Graph
from rdflib.compare import isomorphic

from .hasher import sha256_file
from .isomorphism import compare_isomorphism, IsomorphismReport


@dataclass
class IdempotencyReport:
    """
    Report of idempotency check.
    
    Attributes:
        is_idempotent: True if operation is idempotent (f(f(x)) == f(x))
        input_path: Path to original input file
        first_result_hash: SHA256 of f(x)
        second_result_hash: SHA256 of f(f(x))
        hashes_match: True if first and second hashes are identical (byte-level)
        isomorphism_report: Detailed isomorphism comparison if hashes differ
        error: Error message if check failed
    """
    is_idempotent: bool
    input_path: str
    first_result_hash: Optional[str] = None
    second_result_hash: Optional[str] = None
    hashes_match: bool = False
    isomorphism_report: Optional[IsomorphismReport] = None
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "is_idempotent": self.is_idempotent,
            "input_path": self.input_path,
            "first_result_hash": self.first_result_hash,
            "second_result_hash": self.second_result_hash,
            "hashes_match": self.hashes_match,
            "isomorphism_report": self.isomorphism_report.to_dict() if self.isomorphism_report else None,
            "error": self.error
        }


def check_idempotency(
    input_path: Union[str, Path],
    transform_fn: Callable[[Path, Path], None],
    format: str = "turtle"
) -> IdempotencyReport:
    """
    Check if a transformation is idempotent.
    
    Applies the transformation twice and verifies:
    1. Hash equality (byte-level): SHA256(f(x)) == SHA256(f(f(x)))
    2. If hashes differ, checks isomorphism (semantic equality)
    
    The operation is idempotent if either condition is true.
    
    Args:
        input_path: Path to input file
        transform_fn: Transformation function (input_path, output_path) -> None
        format: RDF format for isomorphism check
        
    Returns:
        IdempotencyReport with results
        
    Example:
        >>> def canonicalize(inp, out):
        ...     # canonicalization logic
        ...     pass
        >>> report = check_idempotency("ontology.ttl", canonicalize)
        >>> assert report.is_idempotent
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        return IdempotencyReport(
            is_idempotent=False,
            input_path=str(input_path),
            error=f"Input file not found: {input_path}"
        )
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # First application: f(x)
            first_output = tmpdir / "first_result.ttl"
            transform_fn(input_path, first_output)
            
            if not first_output.exists():
                return IdempotencyReport(
                    is_idempotent=False,
                    input_path=str(input_path),
                    error="Transform function did not produce output file"
                )
            
            first_hash = sha256_file(first_output)
            
            # Second application: f(f(x))
            second_output = tmpdir / "second_result.ttl"
            transform_fn(first_output, second_output)
            
            if not second_output.exists():
                return IdempotencyReport(
                    is_idempotent=False,
                    input_path=str(input_path),
                    first_result_hash=first_hash,
                    error="Second transform application did not produce output file"
                )
            
            second_hash = sha256_file(second_output)
            
            # Check hash equality (byte-level idempotency)
            hashes_match = first_hash == second_hash
            
            if hashes_match:
                return IdempotencyReport(
                    is_idempotent=True,
                    input_path=str(input_path),
                    first_result_hash=first_hash,
                    second_result_hash=second_hash,
                    hashes_match=True
                )
            
            # Hashes differ - check isomorphism (semantic idempotency)
            iso_report = compare_isomorphism(first_output, second_output)
            
            return IdempotencyReport(
                is_idempotent=iso_report.are_isomorphic,
                input_path=str(input_path),
                first_result_hash=first_hash,
                second_result_hash=second_hash,
                hashes_match=False,
                isomorphism_report=iso_report
            )
            
    except Exception as e:
        return IdempotencyReport(
            is_idempotent=False,
            input_path=str(input_path),
            error=f"Idempotency check failed: {type(e).__name__}: {e}"
        )


def check_graph_idempotency(
    input_graph: Graph,
    transform_fn: Callable[[Graph], Graph],
    label: str = "input"
) -> IdempotencyReport:
    """
    Check if a graph transformation is idempotent using in-memory graphs.
    
    Args:
        input_graph: Input rdflib.Graph
        transform_fn: Transformation function (Graph) -> Graph
        label: Label for the input in the report
        
    Returns:
        IdempotencyReport with results
    """
    try:
        # First application: f(x)
        first_result = transform_fn(input_graph)
        
        # Second application: f(f(x))
        second_result = transform_fn(first_result)
        
        # Check isomorphism
        are_iso = isomorphic(first_result, second_result)
        
        return IdempotencyReport(
            is_idempotent=are_iso,
            input_path=label,
            hashes_match=are_iso  # For in-memory, isomorphism implies idempotency
        )
        
    except Exception as e:
        return IdempotencyReport(
            is_idempotent=False,
            input_path=label,
            error=f"Idempotency check failed: {type(e).__name__}: {e}"
        )


def verify_canonicalization_idempotent(
    input_path: Union[str, Path],
    canonicalize_fn: Callable[[Path, Path], None]
) -> IdempotencyReport:
    """
    Convenience function to verify canonicalization idempotency.
    
    This is a specialized wrapper for the common use case of
    verifying that canonicalization is idempotent.
    
    Args:
        input_path: Path to ontology file
        canonicalize_fn: Canonicalization function (input, output) -> None
        
    Returns:
        IdempotencyReport
    """
    return check_idempotency(input_path, canonicalize_fn, format="turtle")


@dataclass
class FullIdempotencyReport:
    """
    Extended report that includes verification of saved file consistency.
    
    Verifies not just f(f(x)) == f(x), but also that:
    - saved_file_hash == first_result_hash (saved file is truly canonical)
    
    Attributes:
        is_idempotent: True if f(f(x)) == f(x)
        is_fully_consistent: True if saved_hash == first_result_hash AND f(f(x)) == f(x)
        saved_file_hash: SHA256 of the actually saved file
        first_result_hash: SHA256 of f(saved_file)
        second_result_hash: SHA256 of f(f(saved_file))
        saved_matches_first: True if saved_file_hash == first_result_hash
        hashes_match: True if first_result_hash == second_result_hash
        error: Error message if check failed
    """
    is_idempotent: bool
    is_fully_consistent: bool
    saved_file_path: str
    saved_file_hash: Optional[str] = None
    first_result_hash: Optional[str] = None
    second_result_hash: Optional[str] = None
    saved_matches_first: bool = False
    hashes_match: bool = False
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "is_idempotent": self.is_idempotent,
            "is_fully_consistent": self.is_fully_consistent,
            "saved_file_path": self.saved_file_path,
            "saved_file_hash": self.saved_file_hash,
            "first_result_hash": self.first_result_hash,
            "second_result_hash": self.second_result_hash,
            "saved_matches_first": self.saved_matches_first,
            "hashes_match": self.hashes_match,
            "error": self.error
        }


def check_full_idempotency(
    saved_file_path: Union[str, Path],
    transform_fn: Callable[[Path, Path], None],
) -> FullIdempotencyReport:
    """
    Check full idempotency including saved file consistency.
    
    This verifies:
    1. saved_file_hash == first_result_hash (saved file is already canonical)
    2. first_result_hash == second_result_hash (f(f(x)) == f(x))
    
    The first check catches bugs where the save operation uses a different
    transformation than the idempotency verification.
    
    Args:
        saved_file_path: Path to the file that was saved
        transform_fn: Transformation function used for canonicalization
        
    Returns:
        FullIdempotencyReport with all consistency checks
    """
    saved_file_path = Path(saved_file_path)
    
    if not saved_file_path.exists():
        return FullIdempotencyReport(
            is_idempotent=False,
            is_fully_consistent=False,
            saved_file_path=str(saved_file_path),
            error=f"Saved file not found: {saved_file_path}"
        )
    
    try:
        # Hash of the saved file
        saved_hash = sha256_file(saved_file_path)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # First application: f(saved_file)
            first_output = tmpdir / "first_result.ttl"
            transform_fn(saved_file_path, first_output)
            
            if not first_output.exists():
                return FullIdempotencyReport(
                    is_idempotent=False,
                    is_fully_consistent=False,
                    saved_file_path=str(saved_file_path),
                    saved_file_hash=saved_hash,
                    error="Transform function did not produce output file"
                )
            
            first_hash = sha256_file(first_output)
            
            # Second application: f(f(saved_file))
            second_output = tmpdir / "second_result.ttl"
            transform_fn(first_output, second_output)
            
            if not second_output.exists():
                return FullIdempotencyReport(
                    is_idempotent=False,
                    is_fully_consistent=False,
                    saved_file_path=str(saved_file_path),
                    saved_file_hash=saved_hash,
                    first_result_hash=first_hash,
                    error="Second transform did not produce output file"
                )
            
            second_hash = sha256_file(second_output)
            
            # Check all conditions
            saved_matches_first = saved_hash == first_hash
            hashes_match = first_hash == second_hash
            is_idempotent = hashes_match
            is_fully_consistent = saved_matches_first and hashes_match
            
            return FullIdempotencyReport(
                is_idempotent=is_idempotent,
                is_fully_consistent=is_fully_consistent,
                saved_file_path=str(saved_file_path),
                saved_file_hash=saved_hash,
                first_result_hash=first_hash,
                second_result_hash=second_hash,
                saved_matches_first=saved_matches_first,
                hashes_match=hashes_match
            )
            
    except Exception as e:
        return FullIdempotencyReport(
            is_idempotent=False,
            is_fully_consistent=False,
            saved_file_path=str(saved_file_path),
            error=f"Full idempotency check failed: {type(e).__name__}: {e}"
        )
