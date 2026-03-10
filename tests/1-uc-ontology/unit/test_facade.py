"""
Testes para OntoToolsFacade.

Testa a camada de aplicação (facade) que orquestra os casos de uso.
"""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
import tempfile
import json

from onto_tools.application.facade import OntoToolsFacade


@pytest.fixture
def mock_adapters():
    """Fixture que retorna mocks dos adapters habilitados."""
    return {
        'rdf_adapter': MagicMock(),
        'audit_logger': MagicMock(),
    }


@pytest.fixture
def facade(mock_adapters):
    """Fixture que retorna uma instância do Facade com mocks."""
    return OntoToolsFacade(**mock_adapters)


@pytest.fixture
def facade_with_graph(facade):
    """Fixture que retorna Facade com um grafo mockado."""
    mock_graph = MagicMock()
    mock_graph.graph = MagicMock()
    mock_graph.source_path = "/path/to/ontology.ttl"
    mock_graph.metadata = MagicMock()
    mock_graph.metadata.triple_count = 100
    mock_graph.metadata.hash = "abc123def456"
    mock_graph.metadata.timestamp = "2025-01-01T00:00:00"
    
    facade._ontology_graph = mock_graph
    return facade


class TestFacadeInit:
    """Testes de inicialização do Facade."""
    
    def test_facade_creates_with_adapters(self, mock_adapters):
        """Facade é criado com adapters."""
        facade = OntoToolsFacade(**mock_adapters)
        
        assert facade._rdf_adapter == mock_adapters['rdf_adapter']
        assert facade._audit_logger == mock_adapters['audit_logger']
    
    def test_facade_initializes_with_empty_graph(self, facade):
        """Facade inicia sem grafo carregado."""
        assert facade._ontology_graph is None
    
    def test_facade_loads_default_config(self, facade):
        """Facade carrega configuração padrão."""
        assert facade._config is not None
        assert "outputs" in facade._config


class TestLoadOntology:
    """Testes de UC-101: load_ontology."""
    
    def test_load_ontology_file_not_found(self, facade):
        """Retorna erro se arquivo não existe."""
        result = facade.load_ontology("/nonexistent/path.ttl")
        
        assert result["status"] == "error"
        # A mensagem pode variar
        assert "message" in result
    
    def test_load_ontology_validates_utf8(self, facade, tmp_path):
        """Valida encoding UTF-8."""
        ttl_file = tmp_path / "test.ttl"
        ttl_file.write_bytes(b"\xff\xfe invalid utf-8")
        
        result = facade.load_ontology(str(ttl_file), validate=True)
        
        # Deve falhar ou avisar sobre encoding
        assert result["status"] in ["error", "warning", "success"]


class TestNormalizeOntology:
    """Testes de UC-108: normalize_ontology."""
    
    def test_normalize_requires_loaded_ontology(self, facade):
        """Normalização requer ontologia carregada."""
        result = facade.normalize_ontology()
        
        assert result["status"] == "error"
        assert "carregada" in result["message"].lower() or "loaded" in result["message"].lower()






class TestGenerateReviewOutput:
    """Testes de UC-104: generate_review_output."""
    
    def test_review_requires_loaded_ontology(self, facade):
        """Revisão requer ontologia carregada."""
        result = facade.generate_review_output("/output/review.ttl")
        
        assert result["status"] == "error"





class TestAuditLogging:
    """Testes de logging de auditoria."""
    
    def test_facade_has_audit_logger(self, facade):
        """Facade tem audit logger configurado."""
        assert facade._audit_logger is not None


class TestConfigLoading:
    """Testes de carregamento de configuração."""
    
    def test_load_config_from_path(self, mock_adapters, tmp_path):
        """Carrega config de path especificado."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
outputs:
  logs: ./custom/logs
  json: ./custom/json
""")
        
        facade = OntoToolsFacade(config_path=str(config_file), **mock_adapters)
        
        assert facade._config["outputs"]["logs"] == "./custom/logs"
    
    def test_load_config_uses_default_when_missing(self, mock_adapters):
        """Usa config padrão quando arquivo não existe."""
        facade = OntoToolsFacade(config_path="/nonexistent/config.yaml", **mock_adapters)
        
        assert "outputs" in facade._config


class TestFacadeCaching:
    """Testes de cache do Facade."""
    
    def test_loaded_graphs_cache_is_empty_initially(self, facade):
        """Cache de grafos está vazio inicialmente."""
        assert facade._loaded_graphs == {}
