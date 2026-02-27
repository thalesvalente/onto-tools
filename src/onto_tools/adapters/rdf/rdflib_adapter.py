"""RDFlibAdapter — Adapter para rdflib (OntologyPort)"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from rdflib import Graph
from rdflib.plugin import PluginException

from .protege_serializer import serialize_protege_style

if TYPE_CHECKING:
    from typing import Optional


class RDFlibAdapter:
    _format_map = {
        "turtle": "turtle",
        "ttl": "turtle",
        "rdf": "xml",
        "owl": "xml",
        "n3": "n3",
        "nt": "nt",
    }

    @classmethod
    def load_ttl(cls, file_path: str) -> tuple[Graph, dict]:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Caminho não é um arquivo: {file_path}")
        
        try:
            content_bytes = path.read_bytes()
        except Exception as e:
            raise IOError(f"Erro ao ler arquivo: {e}")
        
        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("Encoding inválido. Por favor, salve o arquivo como UTF-8!")
        
        file_hash = hashlib.sha256(content_bytes).hexdigest()
        
        graph = Graph()
        try:
            graph.parse(data=content_str, format="turtle")
        except Exception as e:
            raise ValueError(f"Erro de sintaxe no arquivo .ttl: {e}")
        
        metadata = {
            "hash": file_hash,
            "triple_count": len(graph),
            "source_path": str(path.resolve()),
        }
        
        return graph, metadata

    @classmethod
    def save_ttl(cls, graph: Graph, file_path: str, canonized: bool = False) -> None:
        """
        Salva grafo RDF como arquivo Turtle.
        
        Args:
            graph: Grafo RDF a salvar
            file_path: Caminho do arquivo de saída
            canonized: Se True, usa serializador Protégé (ordenado).
                      Se False, usa serialização padrão RDFLib (mantém ordem).
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if canonized:
            # Usar serializador estilo Protégé (ordenado, para diff/revisão)
            serialized = serialize_protege_style(graph)
        else:
            # Serialização padrão RDFLib (mantém ordem do grafo)
            serialized = graph.serialize(format="turtle")
        
        path.write_bytes(serialized.encode("utf-8"))

    @classmethod
    def parse_turtle(cls, content: str) -> Graph:
        graph = Graph()
        try:
            graph.parse(data=content, format="turtle")
        except Exception as e:
            raise ValueError(f"Erro ao parsear Turtle: {e}")
        return graph

    @classmethod
    def serialize_turtle(cls, graph: Graph, canonized: bool = False) -> str:
        """
        Serializa grafo para Turtle estilo Protégé.
        
        Args:
            graph: Grafo RDF a serializar.
            canonized: Parâmetro mantido por compatibilidade (ignorado).
            
        Returns:
            String com o conteúdo TTL formatado.
        """
        return serialize_protege_style(graph)
