"""
Testes para adapters auxiliares.

Testa logging e reporting adapters.
"""
import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, patch
import tempfile


# ============================================================================
# Testes para AuditLogger
# ============================================================================

class TestAuditLogger:
    """Testes do AuditLogger."""
    
    def test_audit_logger_creates_log_dir(self, tmp_path):
        """Logger cria diretório se não existe."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        log_dir = tmp_path / "new_logs"
        logger = AuditLogger(log_dir=log_dir)
        
        assert log_dir.exists()
    
    def test_audit_logger_creates_session_file(self, tmp_path):
        """Logger cria arquivo de sessão."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        logger = AuditLogger(log_dir=tmp_path, session_id="test-session")
        
        expected_file = tmp_path / "audit-log-session-test-session.json"
        assert expected_file.exists()
    
    def test_audit_logger_logs_operation(self, tmp_path):
        """Logger registra operação."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        logger = AuditLogger(log_dir=tmp_path, session_id="test")
        
        logger.log(
            operation="load",
            details={"file": "test.ttl", "triples": 100},
            onto_name="test-ontology"
        )
        
        log_file = tmp_path / "audit-log-session-test.json"
        with open(log_file) as f:
            log_data = json.load(f)
        
        assert len(log_data["ops"]) == 1
        assert log_data["ops"][0]["type"] == "load"
    
    def test_audit_logger_increments_op_counter(self, tmp_path):
        """Logger incrementa contador de operações."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        logger = AuditLogger(log_dir=tmp_path, session_id="counter-test")
        
        logger.log("op1", {})
        logger.log("op2", {})
        logger.log("op3", {})
        
        log_file = tmp_path / "audit-log-session-counter-test.json"
        with open(log_file) as f:
            log_data = json.load(f)
        
        assert len(log_data["ops"]) == 3
        op_ids = [op.get("op_id", i) for i, op in enumerate(log_data["ops"])]
        assert len(set(op_ids)) == 3  # IDs únicos
    
    def test_audit_logger_records_timestamp(self, tmp_path):
        """Logger registra timestamp ISO 8601."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        logger = AuditLogger(log_dir=tmp_path, session_id="time-test")
        
        before = datetime.now().isoformat()
        logger.log("test", {})
        after = datetime.now().isoformat()
        
        log_file = tmp_path / "audit-log-session-time-test.json"
        with open(log_file) as f:
            log_data = json.load(f)
        
        op_time = log_data["ops"][0].get("applied_at")
        assert op_time is not None
    
    def test_audit_logger_get_log_path(self, tmp_path):
        """Logger retorna caminho do log."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        
        logger = AuditLogger(log_dir=tmp_path, session_id="path-test")
        
        log_path = logger.get_log_path()
        
        assert log_path == tmp_path / "audit-log-session-path-test.json"


class TestCreateAuditLogger:
    """Testes da função factory create_audit_logger."""
    
    def test_create_audit_logger_returns_logger(self, tmp_path):
        """Factory retorna instância de AuditLogger."""
        from onto_tools.adapters.logging.audit_logger import create_audit_logger
        
        logger = create_audit_logger(tmp_path)
        
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        assert isinstance(logger, AuditLogger)
    
    def test_create_audit_logger_with_session_id(self, tmp_path):
        """Factory aceita session_id."""
        from onto_tools.adapters.logging.audit_logger import create_audit_logger
        
        logger = create_audit_logger(tmp_path, session_id="custom-session")
        
        assert logger.session_id == "custom-session"



# ============================================================================
# Testes para AuditFormatter
# ============================================================================

class TestAuditFormatter:
    """Testes do AuditFormatter."""
    
    def test_format_audit_log_creates_md(self, tmp_path):
        """Formatter cria arquivo Markdown."""
        from onto_tools.adapters.reporting.audit_formatter import format_audit_log
        
        # Criar log JSON
        log_file = tmp_path / "audit.json"
        log_data = {
            "session_id": "test",
            "started_at": "2025-01-01T00:00:00",
            "ops": [
                {
                    "type": "load_ontology",
                    "status": "success",
                    "applied_at": "2025-01-01T00:00:01",
                    "triple": {
                        "subject": "",
                        "predicate": "",
                        "object": json.dumps({"file": "test.ttl"})
                    }
                }
            ]
        }
        log_file.write_text(json.dumps(log_data))
        
        output_md = tmp_path / "audit.md"
        format_audit_log(str(log_file), str(output_md))
        
        assert output_md.exists()
    
    def test_format_audit_log_includes_operations(self, tmp_path):
        """Markdown inclui operações."""
        from onto_tools.adapters.reporting.audit_formatter import format_audit_log
        
        log_file = tmp_path / "audit.json"
        log_data = {
            "session_id": "ops-test",
            "started_at": "2025-01-01T00:00:00",
            "ops": [
                {
                    "type": "load_ontology",
                    "status": "success",
                    "applied_at": "2025-01-01T00:00:01",
                    "triple": {
                        "subject": "",
                        "predicate": "",
                        "object": json.dumps({"file": "test.ttl"})
                    }
                },
            ]
        }
        log_file.write_text(json.dumps(log_data))
        
        output_md = tmp_path / "audit.md"
        format_audit_log(str(log_file), str(output_md))
        
        content = output_md.read_text()
        # Verifica que contém informações de operações
        assert "Carregamento" in content or "Relatório" in content



# ============================================================================
# Testes de Integração entre Adapters
# ============================================================================

class TestAdaptersIntegration:
    """Testes de integração entre adapters."""
    
    def test_audit_to_report_flow(self, tmp_path):
        """Fluxo: AuditLogger -> AuditFormatter."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger
        from onto_tools.adapters.reporting.audit_formatter import format_audit_log
        
        # 1. Criar logs
        logger = AuditLogger(log_dir=tmp_path, session_id="integration")
        logger.log("load", {"file": "test.ttl"}, onto_name="test-onto")
        logger.log("normalize", {"rules": "rules.json"})
        logger.log("export", {"format": "xlsx"})
        
        # 2. Formatar em MD
        log_path = logger.get_log_path()
        md_path = tmp_path / "report.md"
        format_audit_log(str(log_path), str(md_path))
        
        # 3. Verificar
        assert md_path.exists()
        content = md_path.read_text()
        assert len(content) > 0
    

# ============================================================================
# Testes de coverage para métodos utilitários do AuditLogger
# ============================================================================

class TestAuditLoggerUtilityMethods:
    """Covers lines 128, 166, 188-189, 201-202, 214-215 in audit_logger.py."""

    def test_log_with_triple_kwarg_stores_triple(self, tmp_path):
        """log() with triple kwarg uses if-triple branch (line 128)."""
        import json
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="triple-test")
        logger.log(
            "insert",
            details={},
            triple={"subject": "http://s", "predicate": "http://p", "object": "http://o", "language": ""},
        )

        log_data = json.loads(logger.log_file.read_text(encoding="utf-8"))
        op = log_data["ops"][0]
        assert op["triple"]["subject"] == "http://s"
        assert op["triple"]["predicate"] == "http://p"

    def test_get_operations_count_empty(self, tmp_path):
        """get_operations_count() is 0 for fresh logger (lines 188-189)."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="cnt0-test")
        assert logger.get_operations_count() == 0

    def test_get_operations_count_after_logging(self, tmp_path):
        """get_operations_count() reflects logged operations."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="cnt2-test")
        logger.log("op1", {"status": "success"})
        logger.log("op2", {"status": "success"})
        assert logger.get_operations_count() == 2

    def test_get_operations_by_type_filters(self, tmp_path):
        """get_operations_by_type() returns matching ops (lines 201-202)."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="bytype-test")
        logger.log("load_ontology", {"status": "success"})
        logger.log("normalize", {"status": "success"})
        logger.log("load_ontology", {"status": "success"})

        ops = logger.get_operations_by_type("load_ontology")
        assert len(ops) == 2
        assert all(op["type"] == "load_ontology" for op in ops)

    def test_get_failed_operations_filters_error_and_failed(self, tmp_path):
        """get_failed_operations() returns error/failed ops (lines 214-215)."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="failed-test")
        logger.log("op1", {"status": "success"})
        logger.log("op2", {}, status="error")
        logger.log("op3", {}, status="failed")

        failed = logger.get_failed_operations()
        assert len(failed) == 2
        assert all(op["status"] in ("error", "failed") for op in failed)

    def test_read_log_returns_empty_when_file_missing(self, tmp_path):
        """_read_log() returns empty dict when log file was deleted (line 166)."""
        from onto_tools.adapters.logging.audit_logger import AuditLogger

        logger = AuditLogger(log_dir=tmp_path, session_id="missing-test")
        # Delete the log file that __init__ created
        logger.log_file.unlink()

        data = logger._read_log()
        assert data == {"ops": []}
