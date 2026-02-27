"""Fixtures para testes E2E."""
import pytest
from pathlib import Path


@pytest.fixture
def e2e_data_dir():
    """Retorna diretório de dados para E2E."""
    return Path(__file__).parent.parent.parent.parent / "data" / "examples"


@pytest.fixture
def sample_ontology(e2e_data_dir):
    """Retorna caminho para ontologia de exemplo."""
    return str(e2e_data_dir / "energy-domain-ontology.ttl")
