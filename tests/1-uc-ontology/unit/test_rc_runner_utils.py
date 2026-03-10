"""Tests for run_rc.py utility functions (standalone script in scripts/)."""
import importlib.util
import json
import re
import sys
from io import StringIO
from pathlib import Path

import pytest

# run_rc.py lives in scripts/, not in the package — import via importlib
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "scripts"
_spec = importlib.util.spec_from_file_location("run_rc", _SCRIPTS_DIR / "run_rc.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_create_execution_id = _mod._create_execution_id
_discover_next_version = _mod._discover_next_version
_read_json_safe = _mod._read_json_safe
_banner = _mod.banner


class TestDiscoverNextVersion:
    """Tests for _discover_next_version."""

    def test_empty_logs_dir(self, tmp_path, monkeypatch):
        logs = tmp_path / "logs"
        logs.mkdir()
        monkeypatch.setattr(_mod, "LOGS_DIR", logs)
        nn, version = _discover_next_version()
        assert nn == 1
        assert version == "RC_v1_CANON"

    def test_logs_dir_not_exists(self, tmp_path, monkeypatch):
        logs = tmp_path / "nonexistent"
        monkeypatch.setattr(_mod, "LOGS_DIR", logs)
        nn, version = _discover_next_version()
        assert nn == 1
        assert version == "RC_v1_CANON"

    def test_existing_versions(self, tmp_path, monkeypatch):
        logs = tmp_path / "logs"
        logs.mkdir()
        (logs / "RC_v3_CANON").mkdir()
        (logs / "RC_v7_CANON").mkdir()
        (logs / "RC_v5_CANON").mkdir()
        (logs / "some_other_dir").mkdir()
        monkeypatch.setattr(_mod, "LOGS_DIR", logs)
        nn, version = _discover_next_version()
        assert nn == 8
        assert version == "RC_v8_CANON"

    def test_ignores_files(self, tmp_path, monkeypatch):
        logs = tmp_path / "logs"
        logs.mkdir()
        (logs / "RC_v2_CANON").mkdir()
        (logs / "RC_v5_CANON.txt").write_text("not a dir")
        monkeypatch.setattr(_mod, "LOGS_DIR", logs)
        nn, version = _discover_next_version()
        assert nn == 3
        assert version == "RC_v3_CANON"


class TestCreateExecutionId:
    """Tests for _create_execution_id."""

    def test_format(self):
        eid = _create_execution_id()
        assert re.match(r"^\d{8}T\d{6}Z_[0-9a-f]{8}$", eid)

    def test_unique(self):
        ids = {_create_execution_id() for _ in range(5)}
        assert len(ids) == 5


class TestReadJsonSafe:
    """Tests for _read_json_safe."""

    def test_valid_json(self, tmp_path):
        p = tmp_path / "data.json"
        p.write_text('{"key": "val"}', encoding="utf-8")
        assert _read_json_safe(p) == {"key": "val"}

    def test_invalid_json(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("not json {{{", encoding="utf-8")
        assert _read_json_safe(p) == {}

    def test_missing_file(self, tmp_path):
        p = tmp_path / "nope.json"
        assert _read_json_safe(p) == {}


class TestBanner:
    """Tests for _banner."""

    def test_prints_message(self, capsys):
        _banner("hello")
        out = capsys.readouterr().out
        assert "hello" in out
        assert "=" in out
