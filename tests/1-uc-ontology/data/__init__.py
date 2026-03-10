"""
Helpers para carregamento de dados de teste.
Centraliza o acesso aos arquivos de dados do diretório data/.
"""
from pathlib import Path
from rdflib import Graph
import json
from typing import Optional

# Diretórios de dados
DATA_DIR = Path(__file__).parent
ONTOLOGIES_DIR = DATA_DIR / "ontologies"
VALID_ONTOLOGIES_DIR = ONTOLOGIES_DIR / "valid"
INVALID_ONTOLOGIES_DIR = ONTOLOGIES_DIR / "invalid"
RULES_DIR = DATA_DIR / "rules"
EXPECTED_DIR = DATA_DIR / "expected"
FIXTURES_DIR = DATA_DIR / "fixtures"


def load_ontology(name: str, valid: bool = True) -> Graph:
    """
    Carrega uma ontologia de teste.
    
    Args:
        name: Nome do arquivo (sem extensão .ttl)
        valid: Se True, carrega de valid/, senão de invalid/
    
    Returns:
        Graph: Grafo RDF carregado
    """
    base_dir = VALID_ONTOLOGIES_DIR if valid else INVALID_ONTOLOGIES_DIR
    path = base_dir / f"{name}.ttl"
    
    if not path.exists():
        raise FileNotFoundError(f"Ontologia não encontrada: {path}")
    
    g = Graph()
    g.parse(path, format="turtle")
    return g


def load_rules(name: str) -> dict:
    """
    Carrega um arquivo de regras JSON.
    
    Args:
        name: Nome do arquivo (sem extensão .json)
    
    Returns:
        dict: Regras carregadas
    """
    path = RULES_DIR / f"{name}.json"
    
    if not path.exists():
        raise FileNotFoundError(f"Regras não encontradas: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_expected(name: str) -> str:
    """
    Carrega um arquivo de resultado esperado.
    
    Args:
        name: Nome do arquivo (com extensão)
    
    Returns:
        str: Conteúdo do arquivo
    """
    path = EXPECTED_DIR / name
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo esperado não encontrado: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_fixture(name: str) -> dict:
    """
    Carrega um fixture JSON.
    
    Args:
        name: Nome do arquivo (sem extensão .json)
    
    Returns:
        dict: Dados do fixture
    """
    path = FIXTURES_DIR / f"{name}.json"
    
    if not path.exists():
        raise FileNotFoundError(f"Fixture não encontrado: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_ontology_path(name: str, valid: bool = True) -> Path:
    """
    Retorna o caminho para uma ontologia de teste.
    
    Args:
        name: Nome do arquivo (sem extensão .ttl)
        valid: Se True, retorna de valid/, senão de invalid/
    
    Returns:
        Path: Caminho para o arquivo
    """
    base_dir = VALID_ONTOLOGIES_DIR if valid else INVALID_ONTOLOGIES_DIR
    return base_dir / f"{name}.ttl"


def get_rules_path(name: str) -> Path:
    """
    Retorna o caminho para um arquivo de regras.
    
    Args:
        name: Nome do arquivo (sem extensão .json)
    
    Returns:
        Path: Caminho para o arquivo
    """
    return RULES_DIR / f"{name}.json"


# Ontologias disponíveis
AVAILABLE_VALID_ONTOLOGIES = [
    "basic-ontology",
    "minimal-ontology",
    "minimal-class",
    "class-with-subclass",
    "properties",
    "valid-naming",
]

AVAILABLE_INVALID_ONTOLOGIES = [
    "naming-errors",
    "invalid-naming",
]

AVAILABLE_RULES = [
    "test-rules",
    "minimal-rules",
]
