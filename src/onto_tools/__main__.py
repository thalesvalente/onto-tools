"""
Entry point para ONTO-TOOLS CLI

Permite execução via:
- python -m onto_tools
- ontotools (se instalado via pip)
"""

from onto_tools.adapters.cli import cli

if __name__ == "__main__":
    cli()
