"""
Logging Adapters - BR-09 Compliance

Provides audit logging infrastructure for RES-115 (100% executions logged).
"""

from .audit_logger import AuditLogger, create_audit_logger

__all__ = [
    "AuditLogger",
    "create_audit_logger",
]
