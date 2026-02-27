"""
Hasher - SHA256 hashing utilities for verification.

Provides deterministic hashing for files and bytes.
Used by manifest_writer and idempotency checks.
"""
import hashlib
from pathlib import Path
from typing import Union


def sha256_file(path: Union[str, Path]) -> str:
    """
    Compute SHA256 hash of a file.
    
    Args:
        path: Path to the file to hash
        
    Returns:
        Uppercase hexadecimal SHA256 hash string (64 characters)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IsADirectoryError: If path is a directory
        PermissionError: If file cannot be read
        
    Example:
        >>> sha256_file("data/ontology.ttl")
        '6E45156A401AD58418844CFAC960D1F551FFE6CAA0771FFD97D4E88F42761286'
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")
    
    sha256_hash = hashlib.sha256()
    
    with open(path, "rb") as f:
        # Read in 64KB chunks for memory efficiency
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest().upper()


def sha256_bytes(data: bytes) -> str:
    """
    Compute SHA256 hash of bytes.
    
    Args:
        data: Bytes to hash
        
    Returns:
        Uppercase hexadecimal SHA256 hash string (64 characters)
        
    Raises:
        TypeError: If data is not bytes
        
    Example:
        >>> sha256_bytes(b"Hello, World!")
        'DFFD6021BB2BD5B0AF676290809EC3A53191DD81C7F70A4B28688A362182986F'
    """
    if not isinstance(data, bytes):
        raise TypeError(f"Expected bytes, got {type(data).__name__}")
    
    return hashlib.sha256(data).hexdigest().upper()


def sha256_string(text: str, encoding: str = "utf-8") -> str:
    """
    Compute SHA256 hash of a string.
    
    Args:
        text: String to hash
        encoding: Text encoding (default: utf-8)
        
    Returns:
        Uppercase hexadecimal SHA256 hash string (64 characters)
        
    Example:
        >>> sha256_string("Hello, World!")
        'DFFD6021BB2BD5B0AF676290809EC3A53191DD81C7F70A4B28688A362182986F'
    """
    return sha256_bytes(text.encode(encoding))


def file_size_bytes(path: Union[str, Path]) -> int:
    """
    Get file size in bytes.
    
    Args:
        path: Path to the file
        
    Returns:
        File size in bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    return path.stat().st_size
