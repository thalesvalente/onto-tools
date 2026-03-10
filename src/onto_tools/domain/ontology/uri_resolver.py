"""URIResolver — Utilitários para resolução de URIs e prefixos (UC-103/UC-106)"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from rdflib import Graph


# Prefixos padrão conhecidos (W3C e comuns em ontologias)
STANDARD_PREFIXES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "vann": "http://purl.org/vocab/vann/",
    "void": "http://rdfs.org/ns/void#",
    "prov": "http://www.w3.org/ns/prov#",
    "sh": "http://www.w3.org/ns/shacl#",
}

# Padrão para detectar URIs prefixadas (prefix:localname)
PREFIXED_URI_PATTERN = re.compile(r'^([a-zA-Z][a-zA-Z0-9_-]*):([a-zA-Z0-9_.-]+)$')

# Padrão para detectar URIs completas
FULL_URI_PATTERN = re.compile(r'^<?(https?://[^>]+)>?$')


class URIResolver:
    """
    Resolve URIs prefixadas para URIs completas e vice-versa.
    
    Usado em UC-103 (Canonicalização) e UC-106 (Edição) para garantir
    que URIs sejam tratadas corretamente como recursos e não literais.
    """
    
    def __init__(self, graph: Optional[Graph] = None, custom_prefixes: Optional[dict] = None):
        """
        Args:
            graph: Grafo RDF para extrair prefixos (opcional)
            custom_prefixes: Prefixos customizados para adicionar (opcional)
        """
        self._prefixes = dict(STANDARD_PREFIXES)
        
        # Extrair prefixos do grafo se fornecido
        if graph is not None:
            for prefix, namespace in graph.namespaces():
                if prefix:  # Ignorar prefixo vazio
                    self._prefixes[prefix] = str(namespace)
        
        # Adicionar prefixos customizados
        if custom_prefixes:
            self._prefixes.update(custom_prefixes)
    
    @property
    def prefixes(self) -> dict:
        """Retorna cópia dos prefixos conhecidos."""
        return dict(self._prefixes)
    
    def add_prefix(self, prefix: str, namespace: str) -> None:
        """Adiciona ou atualiza um prefixo."""
        self._prefixes[prefix] = namespace
    
    def is_prefixed_uri(self, value: str) -> bool:
        """
        Verifica se o valor é uma URI prefixada (prefix:localname).
        
        Args:
            value: String a verificar
            
        Returns:
            True se for URI prefixada, False caso contrário
        """
        return bool(PREFIXED_URI_PATTERN.match(value))
    
    def is_full_uri(self, value: str) -> bool:
        """
        Verifica se o valor é uma URI completa.
        
        Args:
            value: String a verificar
            
        Returns:
            True se for URI completa, False caso contrário
        """
        return bool(FULL_URI_PATTERN.match(value)) or value.startswith("http://") or value.startswith("https://")
    
    def is_uri(self, value: str) -> bool:
        """
        Verifica se o valor é uma URI (prefixada ou completa).
        
        Args:
            value: String a verificar
            
        Returns:
            True se for URI, False caso contrário
        """
        return self.is_prefixed_uri(value) or self.is_full_uri(value)
    
    def resolve_prefixed_uri(self, prefixed_uri: str) -> Optional[str]:
        """
        Resolve uma URI prefixada para URI completa.
        
        Args:
            prefixed_uri: URI no formato prefix:localname
            
        Returns:
            URI completa ou None se o prefixo não for conhecido
            
        Raises:
            ValueError: Se o formato da URI for inválido
        """
        match = PREFIXED_URI_PATTERN.match(prefixed_uri)
        if not match:
            raise ValueError(f"Formato de URI inválido: {prefixed_uri}")
        
        prefix, localname = match.groups()
        
        if prefix not in self._prefixes:
            return None  # Prefixo desconhecido
        
        return self._prefixes[prefix] + localname
    
    def to_full_uri(self, value: str) -> str:
        """
        Converte qualquer URI para URI completa.
        
        Args:
            value: URI (prefixada ou completa)
            
        Returns:
            URI completa
            
        Raises:
            ValueError: Se não for possível resolver a URI
        """
        # Remover < > se presentes
        value = value.strip()
        if value.startswith('<') and value.endswith('>'):
            value = value[1:-1]
        
        # Já é URI completa
        if self.is_full_uri(value):
            return value
        
        # Tentar resolver como prefixada
        if self.is_prefixed_uri(value):
            resolved = self.resolve_prefixed_uri(value)
            if resolved:
                return resolved
            
            # Prefixo desconhecido
            match = PREFIXED_URI_PATTERN.match(value)
            prefix = match.group(1) if match else "unknown"
            raise ValueError(f"Prefixo desconhecido: '{prefix}'. Use URI completa ou registre o prefixo.")
        
        raise ValueError(f"Formato de URI não reconhecido: {value}")
    
    def to_prefixed_uri(self, full_uri: str) -> Optional[str]:
        """
        Converte URI completa para forma prefixada se possível.
        
        Args:
            full_uri: URI completa
            
        Returns:
            URI prefixada ou None se não houver prefixo correspondente
        """
        # Remover < > se presentes
        full_uri = full_uri.strip()
        if full_uri.startswith('<') and full_uri.endswith('>'):
            full_uri = full_uri[1:-1]
        
        # Procurar prefixo que corresponde
        best_match = None
        best_length = 0
        
        for prefix, namespace in self._prefixes.items():
            if full_uri.startswith(namespace) and len(namespace) > best_length:
                best_match = prefix
                best_length = len(namespace)
        
        if best_match:
            localname = full_uri[best_length:]
            return f"{best_match}:{localname}"
        
        return None
    
    def to_rdflib_term(self, value: str, prefer_uri: bool = True):
        """
        Converte string para termo RDFLib apropriado (URIRef ou Literal).
        
        Args:
            value: Valor a converter
            prefer_uri: Se True, tenta resolver como URI primeiro
            
        Returns:
            URIRef se for URI, Literal caso contrário
        """
        from rdflib import Literal, URIRef
        
        # Valor vazio
        if not value or not value.strip():
            return Literal("")
        
        value = value.strip()
        
        # Se prefer_uri, tentar resolver como URI primeiro
        if prefer_uri:
            # URI completa
            if self.is_full_uri(value):
                # Remover < > se presentes
                if value.startswith('<') and value.endswith('>'):
                    value = value[1:-1]
                return URIRef(value)
            
            # URI prefixada com prefixo conhecido
            if self.is_prefixed_uri(value):
                try:
                    full_uri = self.to_full_uri(value)
                    return URIRef(full_uri)
                except ValueError:
                    pass  # Prefixo desconhecido, tratar como literal
        
        # Não é URI ou prefer_uri=False, retornar como Literal
        return Literal(value)
    
    def ensure_namespace_bindings(self, graph: Graph, bind_standard: bool = True) -> None:
        """
        Garante que todos os namespaces usados estão vinculados ao grafo.
        
        Isso previne que o RDFLib crie prefixos automáticos como ns1, ns2.
        
        Args:
            graph: Grafo RDF para vincular namespaces
            bind_standard: Se True, vincula também prefixos padrão
        """
        from rdflib import Namespace
        
        # Coletar todos os namespaces usados nas triplas
        used_namespaces = set()
        
        for s, p, o in graph:
            for term in (s, p, o):
                term_str = str(term)
                if term_str.startswith("http://") or term_str.startswith("https://"):
                    # Extrair namespace (até último # ou /)
                    if '#' in term_str:
                        ns = term_str.rsplit('#', 1)[0] + '#'
                    elif '/' in term_str:
                        ns = term_str.rsplit('/', 1)[0] + '/'
                    else:
                        ns = term_str
                    used_namespaces.add(ns)
        
        # Vincular namespaces usados que têm prefixo conhecido
        for prefix, namespace in self._prefixes.items():
            if namespace in used_namespaces or bind_standard:
                if prefix in STANDARD_PREFIXES or bind_standard:
                    graph.bind(prefix, Namespace(namespace), override=True, replace=True)
        
        # Vincular namespaces que ainda não têm prefixo
        existing_prefixes = {str(ns): prefix for prefix, ns in graph.namespaces()}
        for ns in used_namespaces:
            if ns not in existing_prefixes:
                # Tentar encontrar prefixo nos nossos conhecidos
                for prefix, known_ns in self._prefixes.items():
                    if known_ns == ns:
                        graph.bind(prefix, Namespace(ns), override=True, replace=True)
                        break


def resolve_prefixed_uri_for_graph(value: str, graph: Graph) -> str:
    """
    Função de conveniência para resolver URI prefixada usando prefixos do grafo.
    
    Args:
        value: URI (prefixada ou completa)
        graph: Grafo RDF com prefixos
        
    Returns:
        URI completa
    """
    resolver = URIResolver(graph)
    return resolver.to_full_uri(value)


def to_rdflib_term_for_graph(value: str, graph: Graph, prefer_uri: bool = True):
    """
    Função de conveniência para converter string em termo RDFLib.
    
    Args:
        value: Valor a converter
        graph: Grafo RDF com prefixos
        prefer_uri: Se True, tenta resolver como URI primeiro
        
    Returns:
        URIRef ou Literal
    """
    resolver = URIResolver(graph)
    return resolver.to_rdflib_term(value, prefer_uri)
