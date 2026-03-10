"""Fixtures para testes CLI."""
import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """CliRunner para testes."""
    return CliRunner()
