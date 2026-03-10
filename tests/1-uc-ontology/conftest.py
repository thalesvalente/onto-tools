"""Fixtures compartilhadas para testes do UC-Ontology."""
import pytest
from pathlib import Path

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.graph import OntologyGraph
from onto_tools.domain.ontology.normalizer import Normalizer
from onto_tools.domain.ontology.naming_validator import NamingValidator
from onto_tools.domain.ontology.uri_resolver import URIResolver

# Caminho para dados de teste
DATA_DIR = Path(__file__).parent / "data"
ONTOLOGIES_DIR = DATA_DIR / "ontologies"
VALID_ONTOLOGIES_DIR = ONTOLOGIES_DIR / "valid"
INVALID_ONTOLOGIES_DIR = ONTOLOGIES_DIR / "invalid"
RULES_DIR = DATA_DIR / "rules"


def load_ontology(name: str, valid: bool = True) -> Graph:
    """Carrega ontologia de teste."""
    base_dir = VALID_ONTOLOGIES_DIR if valid else INVALID_ONTOLOGIES_DIR
    path = base_dir / f"{name}.ttl"
    g = Graph()
    g.parse(path, format="turtle")
    return g


def get_rules_path(name: str) -> Path:
    """Retorna caminho para regras de teste."""
    return RULES_DIR / f"{name}.json"


# Namespaces
EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


@pytest.fixture
def project_root() -> Path:
    """Retorna caminho para a raiz do projeto."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def fixtures_dir() -> Path:
    """Retorna caminho para diretório de fixtures."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def data_dir() -> Path:
    """Retorna caminho para diretório de dados de teste."""
    return DATA_DIR


@pytest.fixture
def data_examples_dir(project_root) -> Path:
    """Retorna caminho para data/examples."""
    return project_root / "data" / "examples"


@pytest.fixture
def rules_json_path(data_examples_dir) -> str:
    """Retorna caminho para rules.json."""
    return str(data_examples_dir / "rules.json")


@pytest.fixture
def test_rules_path() -> str:
    """Retorna caminho para regras de teste."""
    return str(get_rules_path("test-rules"))


@pytest.fixture
def sample_ontology_path(data_examples_dir) -> str:
    """Retorna caminho para ontologia de exemplo."""
    return str(data_examples_dir / "energy-domain-ontology.ttl")


@pytest.fixture
def rdf_adapter():
    """Instância do RDFlibAdapter."""
    return RDFlibAdapter()


@pytest.fixture
def normalizer(rules_json_path):
    """Instância do Normalizer com rules.json."""
    return Normalizer(rules_path=rules_json_path)


@pytest.fixture
def naming_validator(rules_json_path):
    """Instância do NamingValidator."""
    return NamingValidator(rules_path=rules_json_path)


@pytest.fixture
def empty_graph():
    """Grafo RDF vazio."""
    return Graph()


@pytest.fixture
def minimal_class_graph():
    """Grafo com uma classe OWL mínima - carregado de arquivo."""
    return load_ontology("minimal-class")


@pytest.fixture
def class_with_subclass_graph():
    """Grafo com classe e subclasse - carregado de arquivo."""
    return load_ontology("class-with-subclass")


@pytest.fixture
def property_graph():
    """Grafo com propriedades OWL - carregado de arquivo."""
    return load_ontology("properties")


@pytest.fixture
def invalid_naming_graph():
    """Grafo com nomes que violam convenções - carregado de arquivo."""
    return load_ontology("invalid-naming", valid=False)


@pytest.fixture
def valid_naming_graph():
    """Grafo com nomes seguindo convenções - carregado de arquivo."""
    return load_ontology("valid-naming")


@pytest.fixture
def tmp_ttl_file(tmp_path, minimal_class_graph):
    """Cria arquivo TTL temporário."""
    ttl_file = tmp_path / "test.ttl"
    minimal_class_graph.serialize(destination=str(ttl_file), format="turtle")
    return str(ttl_file)


@pytest.fixture
def uri_resolver(minimal_class_graph):
    """Instância do URIResolver com prefixos."""
    return URIResolver(minimal_class_graph)
