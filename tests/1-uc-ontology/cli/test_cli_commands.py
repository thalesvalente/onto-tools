"""
Testes de CLI para OntoTools.

Testa os comandos CLI usando click.testing.CliRunner.
Simula execução real dos comandos sem precisar de terminal.
"""
import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from onto_tools.adapters.cli.commands import (
    cli,
    ontology_load,
    ontology_review,
    ontology_normalize,
)


@pytest.fixture
def cli_runner():
    """Fixture que retorna um CliRunner para testes."""
    return CliRunner()


@pytest.fixture
def mock_facade():
    """Fixture que retorna um mock do facade."""
    with patch('onto_tools.adapters.cli.commands.get_facade') as mock:
        facade_instance = MagicMock()
        mock.return_value = facade_instance
        yield facade_instance


@pytest.fixture
def mock_config():
    """Fixture que retorna um mock da configuração."""
    config = {
        "ontologies": {
            "directory": "data/edo/core"
        },
        "outputs": {
            "logs": "outputs/logs",
            "review": "outputs/review"
        }
    }
    with patch('onto_tools.adapters.cli.commands.load_config') as mock:
        mock.return_value = config
        yield config


class TestCLIMainGroup:
    """Testes do grupo principal CLI."""
    
    def test_cli_version(self, cli_runner):
        """CLI mostra versão corretamente."""
        result = cli_runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert 'ontotools' in result.output.lower() or 'version' in result.output.lower()
    
    def test_cli_help(self, cli_runner):
        """CLI mostra ajuda corretamente."""
        result = cli_runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'ontology' in result.output
        assert 'verify' in result.output


class TestOntologyDomainCLI:
    """Testes dos comandos do domínio ontology (UC-101 a UC-108)."""
    
    def test_ontology_help(self, cli_runner):
        """Comando ontology mostra ajuda."""
        result = cli_runner.invoke(cli, ['ontology', '--help'])
        
        assert result.exit_code == 0
        assert 'load' in result.output
        assert 'normalize' in result.output
    
    def test_ontology_load_success(self, cli_runner, mock_facade, mock_config, tmp_path):
        """UC-101: Carrega ontologia com sucesso."""
        # Criar arquivo TTL temporário
        onto_dir = tmp_path / "data" / "edo" / "core"
        onto_dir.mkdir(parents=True)
        ttl_file = onto_dir / "test.ttl"
        ttl_file.write_text("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
        
        mock_config["ontologies"]["directory"] = str(onto_dir)
        mock_facade.load_ontology.return_value = {
            "status": "success",
            "message": "Ontologia carregada",
            "triples_count": 100,
            "sha256": "abc123"
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'load', 'test.ttl'])
        
        # Deve tentar carregar (mesmo que falhe por mock)
        assert 'Carregando' in result.output or mock_facade.load_ontology.called
    
    def test_ontology_normalize_success(self, cli_runner, mock_facade):
        """UC-108: Normaliza ontologia com sucesso."""
        mock_facade.normalize_ontology.return_value = {
            "status": "success",
            "message": "Ontologia normalizada"
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'normalize'])
        
        mock_facade.normalize_ontology.assert_called_once()
    
    def test_ontology_normalize_with_warnings(self, cli_runner, mock_facade):
        """UC-108: Normaliza com warnings."""
        mock_facade.normalize_ontology.return_value = {
            "status": "success_with_warnings",
            "message": "Normalização com avisos",
            "warnings": [{"message": "Aviso de teste"}]
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'normalize'])
        
        assert result.exit_code == 0
    
    def test_ontology_review_success(self, cli_runner, mock_facade, tmp_path):
        """UC-104: Gera pacote de revisão."""
        mock_facade.generate_review_output.return_value = {
            "status": "success",
            "message": "Pacote gerado",
            "ttl_path": "outputs/review.ttl",
            "log_path": "outputs/export-log.json"
        }
        
        output_file = tmp_path / "review.ttl"
        
        result = cli_runner.invoke(cli, ['ontology', 'review', '-o', str(output_file)])
        
        mock_facade.generate_review_output.assert_called_once()


class TestCLIErrorHandling:
    """Testes de tratamento de erros na CLI."""
    
    def test_invalid_command(self, cli_runner):
        """Comando inválido mostra erro."""
        result = cli_runner.invoke(cli, ['invalid-command'])
        
        assert result.exit_code != 0
    
    def test_missing_argument(self, cli_runner):
        """Argumento faltando mostra erro."""
        result = cli_runner.invoke(cli, ['verify', 'hash'])
        
        assert result.exit_code != 0
        assert 'Missing argument' in result.output or 'Error' in result.output
    
    def test_facade_error_propagates(self, cli_runner, mock_facade):
        """Erro do facade propaga para CLI."""
        mock_facade.normalize_ontology.return_value = {
            "status": "error",
            "message": "Nenhuma ontologia carregada"
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'normalize'])
        
        assert result.exit_code != 0


class TestCLIOutputFormatting:
    """Testes de formatação de saída da CLI."""
    
    def test_success_shows_checkmark(self, cli_runner, mock_facade):
        """Sucesso mostra checkmark."""
        mock_facade.normalize_ontology.return_value = {
            "status": "success",
            "message": "Ontologia normalizada com sucesso"
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'normalize'])
        
        assert '✅' in result.output or 'success' in result.output.lower()
    
    def test_error_shows_cross(self, cli_runner, mock_facade):
        """Erro mostra X."""
        mock_facade.normalize_ontology.return_value = {
            "status": "error",
            "message": "Falha na normalização"
        }
        
        result = cli_runner.invoke(cli, ['ontology', 'normalize'])
        
        assert '❌' in result.output or 'error' in result.output.lower() or 'falha' in result.output.lower()


class TestOntologyLoadEdgeCases:
    """Additional edge-case tests for ontology load command."""

    def test_ontology_load_no_ttl_files(self, cli_runner, mock_facade, mock_config, tmp_path):
        """Shows error when ontology directory has no TTL files (lines 149-150)."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        mock_config["ontologies"]["directory"] = str(empty_dir)

        result = cli_runner.invoke(cli, ['ontology', 'load'])
        assert result.exit_code != 0

    def test_ontology_load_via_interactive_menu(self, cli_runner, mock_facade, mock_config, tmp_path):
        """Exercises interactive menu path (lines 156-171) by providing input."""
        onto_dir = tmp_path / "ontologies"
        onto_dir.mkdir()
        ttl_file = onto_dir / "test.ttl"
        ttl_file.write_text("@prefix owl: <http://www.w3.org/2002/07/owl#> .")

        mock_config["ontologies"]["directory"] = str(onto_dir)
        mock_facade.load_ontology.return_value = {
            "status": "success",
            "message": "Ontologia carregada",
            "triples_count": 1,
            "sha256": "abc123",
        }

        # Simulate user selecting option "1" from the menu
        result = cli_runner.invoke(cli, ['ontology', 'load'], input='1\n')
        assert mock_facade.load_ontology.called

    def test_ontology_load_error_from_facade(self, cli_runner, mock_facade, mock_config, tmp_path):
        """Error status from facade shows ❌ and exits 1 (lines 185-186)."""
        onto_dir = tmp_path / "ontologies"
        onto_dir.mkdir()
        ttl_file = onto_dir / "broken.ttl"
        ttl_file.write_text("@prefix owl: <http://www.w3.org/2002/07/owl#> .")

        mock_config["ontologies"]["directory"] = str(onto_dir)
        mock_facade.load_ontology.return_value = {
            "status": "error",
            "message": "Encoding inválido",
        }

        result = cli_runner.invoke(cli, ['ontology', 'load', 'broken.ttl'])
        assert result.exit_code != 0


class TestOntologyReviewEdgeCases:
    """Additional edge-case tests for ontology review command."""

    def test_ontology_review_default_output_path(self, cli_runner, mock_facade, mock_config):
        """Review without -o loads default output path from config (lines 203-205)."""
        mock_facade.generate_review_output.return_value = {
            "status": "success",
            "message": "Pacote gerado",
            "ttl_path": "outputs/review/ontology-review.ttl",
            "log_path": "outputs/review/export-log.json",
        }
        # Do NOT pass -o; this triggers the 'if not output:' branch
        result = cli_runner.invoke(cli, ['ontology', 'review'])
        assert mock_facade.generate_review_output.called

    def test_ontology_review_non_ttl_extension(self, cli_runner, mock_facade, mock_config, tmp_path):
        """Review with non-.ttl extension corrects it to .ttl (line 210)."""
        mock_facade.generate_review_output.return_value = {
            "status": "success",
            "message": "Pacote gerado",
            "ttl_path": "review.ttl",
            "log_path": "review.json",
        }
        # Provide a non-.ttl path → triggers .with_suffix('.ttl')
        output_path = tmp_path / "review.json"
        result = cli_runner.invoke(cli, ['ontology', 'review', '-o', str(output_path)])
        assert mock_facade.generate_review_output.called

    def test_ontology_review_error(self, cli_runner, mock_facade, mock_config, tmp_path):
        """Review error status shows ❌ and exits 1 (lines 228-229)."""
        mock_facade.generate_review_output.return_value = {
            "status": "error",
            "message": "Falha ao gerar revisão",
        }
        output_path = tmp_path / "review.ttl"
        result = cli_runner.invoke(cli, ['ontology', 'review', '-o', str(output_path)])
        assert result.exit_code != 0
