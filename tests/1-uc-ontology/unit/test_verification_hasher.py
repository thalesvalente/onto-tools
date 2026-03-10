"""
Unit tests for verification.hasher module.

Tests SHA256 hashing functionality for files and bytes.
"""
import tempfile
from pathlib import Path

import pytest

from onto_tools.application.verification.hasher import (
    sha256_file,
    sha256_bytes,
    sha256_string,
    file_size_bytes
)


class TestSha256File:
    """Tests for sha256_file function."""
    
    def test_hash_simple_file(self, tmp_path: Path):
        """Test hashing a simple text file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        result = sha256_file(test_file)
        
        # SHA256 of "Hello, World!" encoded as UTF-8
        expected = "DFFD6021BB2BD5B0AF676290809EC3A53191DD81C7F70A4B28688A362182986F"
        assert result == expected
        assert len(result) == 64
        assert result == result.upper()  # Always uppercase
    
    def test_hash_empty_file(self, tmp_path: Path):
        """Test hashing an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_bytes(b"")
        
        result = sha256_file(test_file)
        
        # SHA256 of empty content
        expected = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
        assert result == expected
    
    def test_hash_binary_file(self, tmp_path: Path):
        """Test hashing a binary file."""
        test_file = tmp_path / "binary.bin"
        test_file.write_bytes(b"\x00\x01\x02\x03")
        
        result = sha256_file(test_file)
        
        assert len(result) == 64
        assert result.isalnum()
    
    def test_hash_same_content_same_hash(self, tmp_path: Path):
        """Test that same content produces same hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        content = "Same content"
        file1.write_text(content)
        file2.write_text(content)
        
        assert sha256_file(file1) == sha256_file(file2)
    
    def test_hash_different_content_different_hash(self, tmp_path: Path):
        """Test that different content produces different hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        
        file1.write_text("Content A")
        file2.write_text("Content B")
        
        assert sha256_file(file1) != sha256_file(file2)
    
    def test_file_not_found_raises(self, tmp_path: Path):
        """Test that non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            sha256_file(tmp_path / "nonexistent.txt")
    
    def test_directory_raises(self, tmp_path: Path):
        """Test that directory path raises IsADirectoryError."""
        with pytest.raises(IsADirectoryError):
            sha256_file(tmp_path)
    
    def test_accepts_string_path(self, tmp_path: Path):
        """Test that string path is accepted."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        result = sha256_file(str(test_file))
        
        assert len(result) == 64
    
    def test_large_file_chunked(self, tmp_path: Path):
        """Test hashing large file (> 64KB chunk size)."""
        test_file = tmp_path / "large.bin"
        # Create 100KB file
        test_file.write_bytes(b"x" * 100_000)
        
        result = sha256_file(test_file)
        
        assert len(result) == 64


class TestSha256Bytes:
    """Tests for sha256_bytes function."""
    
    def test_hash_bytes(self):
        """Test hashing bytes."""
        result = sha256_bytes(b"Hello, World!")
        
        expected = "DFFD6021BB2BD5B0AF676290809EC3A53191DD81C7F70A4B28688A362182986F"
        assert result == expected
    
    def test_hash_empty_bytes(self):
        """Test hashing empty bytes."""
        result = sha256_bytes(b"")
        
        expected = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
        assert result == expected
    
    def test_not_bytes_raises(self):
        """Test that non-bytes input raises TypeError."""
        with pytest.raises(TypeError):
            sha256_bytes("not bytes")  # type: ignore
    
    def test_hash_deterministic(self):
        """Test that hashing is deterministic."""
        data = b"Test data"
        assert sha256_bytes(data) == sha256_bytes(data)


class TestSha256String:
    """Tests for sha256_string function."""
    
    def test_hash_string(self):
        """Test hashing a string."""
        result = sha256_string("Hello, World!")
        
        expected = "DFFD6021BB2BD5B0AF676290809EC3A53191DD81C7F70A4B28688A362182986F"
        assert result == expected
    
    def test_hash_unicode(self):
        """Test hashing unicode string."""
        result = sha256_string("Olá, Mundo! 🌍")
        
        assert len(result) == 64
    
    def test_custom_encoding(self):
        """Test hashing with custom encoding."""
        # Same ASCII string, same hash regardless of encoding
        result_utf8 = sha256_string("Hello", encoding="utf-8")
        result_ascii = sha256_string("Hello", encoding="ascii")
        
        assert result_utf8 == result_ascii


class TestFileSizeBytes:
    """Tests for file_size_bytes function."""
    
    def test_file_size(self, tmp_path: Path):
        """Test getting file size."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"12345")
        
        assert file_size_bytes(test_file) == 5
    
    def test_empty_file_size(self, tmp_path: Path):
        """Test getting empty file size."""
        test_file = tmp_path / "empty.txt"
        test_file.write_bytes(b"")
        
        assert file_size_bytes(test_file) == 0
    
    def test_file_not_found_raises(self, tmp_path: Path):
        """Test that non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            file_size_bytes(tmp_path / "nonexistent.txt")
