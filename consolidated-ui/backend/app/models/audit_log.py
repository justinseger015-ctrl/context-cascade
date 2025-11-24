"""
Audit log model - re-export from core.audit_logging.

NFR2.6 compliance for tracking all database changes.
"""

from app.core.audit_logging import AuditLog

__all__ = ["AuditLog"]
