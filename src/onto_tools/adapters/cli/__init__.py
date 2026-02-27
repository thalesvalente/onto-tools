"""
CLI Adapter - RES-116 Interface Única

ADR-0001: CLI exclusiva com framework click
22 comandos organizados em 5 domínios
"""

from .commands import cli

__all__ = ["cli"]
