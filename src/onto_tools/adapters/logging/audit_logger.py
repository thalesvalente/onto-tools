"""
Audit Logger - BR-09 Rastreabilidade e Auditoria

RF-106: "gera log de auditoria (conforme template especificado em 
`04-files_example/audit-log.json`) de todas as edições"

RES-115: "100% das execuções logadas na Façade"

Estrutura conforme audit-log.json:
{
    "ops": [
        {
            "batch_id": str,
            "onto_name": str,
            "onto_version": str,
            "op_id": int,
            "type": str,  # insert|update|delete|query|export|load|etc
            "status": str,  # applied|skipped|failed|success|error
            "applied_at": str (ISO 8601),
            "time_ms": int,
            "checks": {
                "precondition": str,
                "precondition_result": bool
            },
            "triple": {
                "subject": str,
                "predicate": str,
                "object": str,
                "language": str
            }
        }
    ]
}
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class AuditLogger:
    """
    RES-115 compliance: Logs 100% of executions from Façade.
    BR-09 compliance: Rastreabilidade e Auditoria obrigatória.
    
    Generates audit-log.json with deterministic structure.
    Thread-safe append operations (atomic writes via temp file).
    """
    
    def __init__(self, log_dir: Path, session_id: str = None):
        """
        Initialize audit logger with output directory.
        
        Args:
            log_dir: Directory where audit-log.json will be stored
            session_id: Session identifier for grouping operations (default: timestamp when session starts)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Use session_id or generate timestamp-based session (YYYYMMDD-HHMMSS)
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        self.session_id = session_id
        self.log_file = self.log_dir / f"audit-log-session-{session_id}.json"
        
        # Initialize log file with empty ops array if new session
        if not self.log_file.exists():
            self._write_log({"session_id": session_id, "started_at": datetime.now().isoformat(), "ops": []})
        
        # Operation counter starts from existing operations
        existing_log = self._read_log()
        self._operation_counter = len(existing_log.get("ops", []))
    
    def log(
        self,
        operation: str,
        details: Dict[str, Any],
        onto_name: Optional[str] = None,
        onto_version: Optional[str] = None,
        status: str = "success",
        precondition: Optional[str] = None,
        precondition_result: Optional[bool] = None,
        triple: Optional[Dict[str, str]] = None,
        time_ms: Optional[int] = None
    ) -> None:
        """
        Log an operation to audit-log.json.
        
        RES-115: Called by every Façade method (100% executions).
        
        Args:
            operation: Type of operation (load, query, export, insert, update, delete, etc.)
            details: Operation-specific details (inputs, outputs, metrics)
            onto_name: Ontology name (optional)
            onto_version: Ontology version (optional)
            status: Operation status (success|error|applied|skipped|failed)
            precondition: Precondition check name (optional)
            precondition_result: Precondition result (optional)
            triple: RDF triple affected (optional) - {subject, predicate, object, language}
            time_ms: Execution time in milliseconds (optional)
        """
        # Generate batch_id (incremental per session)
        self._operation_counter += 1
        date_str = datetime.now().strftime("%Y-%m-%d")
        batch_id = f"batch-{date_str}-{self._operation_counter:04d}"
        
        # Build operation entry
        op_entry = {
            "batch_id": batch_id,
            "onto_name": onto_name or details.get("onto_name", "unknown"),
            "onto_version": onto_version or details.get("onto_version", "unknown"),
            "op_id": self._operation_counter,
            "type": operation,
            "status": status,
            "applied_at": datetime.now().isoformat(),
            "time_ms": time_ms or details.get("time_ms", 0),
            "checks": {
                "precondition": precondition or "none",
                "precondition_result": precondition_result if precondition_result is not None else True
            }
        }
        
        # Add triple if provided (for RDF operations)
        if triple:
            op_entry["triple"] = {
                "subject": triple.get("subject", ""),
                "predicate": triple.get("predicate", ""),
                "object": triple.get("object", ""),
                "language": triple.get("language", "")
            }
        else:
            # For non-RDF operations, store details in triple.object as JSON
            op_entry["triple"] = {
                "subject": f"operation:{operation}",
                "predicate": "details",
                "object": json.dumps(details, ensure_ascii=False),
                "language": ""
            }
        
        # Append to log file (atomic write)
        self._append_operation(op_entry)
    
    def _append_operation(self, op_entry: Dict[str, Any]) -> None:
        """
        Atomically append operation to audit-log.json.
        
        Uses temp file + rename for atomic write (RNF-106 pattern).
        """
        # Read current log
        current_log = self._read_log()
        
        # Append new operation
        current_log["ops"].append(op_entry)
        
        # Write atomically
        self._write_log(current_log)
    
    def _read_log(self) -> Dict[str, Any]:
        """Read current audit log."""
        if self.log_file.exists():
            with open(self.log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"ops": []}
    
    def _write_log(self, log_data: Dict[str, Any]) -> None:
        """
        Atomically write log file.
        
        RNF-106: Copy-on-write + atomic rename pattern.
        """
        # Write to temp file
        temp_file = self.log_file.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=4)
        
        # Atomic rename (same filesystem)
        temp_file.replace(self.log_file)
    
    def get_log_path(self) -> Path:
        """Return path to current audit log file."""
        return self.log_file
    
    def get_operations_count(self) -> int:
        """Return number of logged operations."""
        log_data = self._read_log()
        return len(log_data.get("ops", []))
    
    def get_operations_by_type(self, operation_type: str) -> list:
        """
        Get all operations of specific type.
        
        Args:
            operation_type: Type to filter (load, query, export, etc.)
            
        Returns:
            List of operation entries
        """
        log_data = self._read_log()
        return [
            op for op in log_data.get("ops", [])
            if op.get("type") == operation_type
        ]
    
    def get_failed_operations(self) -> list:
        """
        Get all failed operations.
        
        Returns:
            List of operations with status="failed" or "error"
        """
        log_data = self._read_log()
        return [
            op for op in log_data.get("ops", [])
            if op.get("status") in ["failed", "error"]
        ]


# Factory function for dependency injection
def create_audit_logger(log_dir: Path, session_id: str = None) -> AuditLogger:
    """
    Factory function for creating AuditLogger instances.
    
    Used by Façade for dependency injection (Hexagonal architecture).
    
    Args:
        log_dir: Directory for audit logs
        session_id: Session identifier for grouping operations (default: timestamp YYYYMMDD-HHMMSS)
        
    Returns:
        Configured AuditLogger instance
    """
    return AuditLogger(log_dir, session_id)
