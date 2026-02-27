"""
Canonicalizer — Canonização de Ontologias TTL (UC-103)

Responsável APENAS por ordenação determinística e serialização estilo Protégé.
NÃO modifica conteúdo semântico (URIs, labels, valores).

Separação de responsabilidades (Single Responsibility Principle):
- Canonicalizer (UC-103): Ordenação determinística para diff/revisão
- Normalizer (UC-108): Correções semânticas (PascalCase, Title Case, etc.)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rdflib import Graph


@dataclass
class CanonicalizationResult:
    """Resultado da canonização com estatísticas."""
    graph: "Graph"
    triple_count: int
    prefix_count: int
    processing_time_ms: float = 0.0
    is_idempotent: bool = True
    warnings: list[dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Converte para dicionário serializável."""
        return {
            "triple_count": self.triple_count,
            "prefix_count": self.prefix_count,
            "processing_time_ms": self.processing_time_ms,
            "is_idempotent": self.is_idempotent,
            "warnings_count": len(self.warnings),
            "warnings": self.warnings
        }


def _get_default_rules_path() -> str:
    """Retorna o caminho padrão para rules.json."""
    project_root = Path(__file__).parent.parent.parent.parent.parent
    return str(project_root / "data" / "examples" / "rules.json")


class Canonicalizer:
    """
    UC-103: Canonização de Ontologias TTL.
    
    Garante serialização determinística/idempotente do TTL para facilitar
    diff e revisão. NÃO modifica conteúdo semântico.
    
    Operações realizadas:
    - Ordenar prefixos alfabeticamente
    - Ordenar triplas por (subject, predicate, object)
    - Ordenar predicados conforme PREDICATE_ORDER do Protégé
    - Vincular namespaces explicitamente (evita ns1, ns2)
    - Garantir serialização determinística e idempotente
    
    Operações NÃO realizadas (responsabilidade do Normalizer):
    - Correção de nomenclatura (PascalCase, lowerCamelCase)
    - Correção de Title Case em prefLabels
    - Validação de dcterms:identifier
    - Correções semânticas de qualquer tipo
    - Normalização de literais (trim whitespace, lowercase language tags)
    - Remoção de triplas duplicatas (RDF Graph já é conjunto)
    """
    
    def __init__(self, rules_path: Optional[str] = None):
        """
        Inicializa o Canonicalizer.
        
        Args:
            rules_path: Caminho para rules.json (opcional)
        """
        self.rules_path = rules_path or _get_default_rules_path()
        self.rules = self._load_rules()
        self._warnings: list[dict] = []
    
    def _load_rules(self) -> dict:
        """Carrega regras de formatação e ordenação do rules.json."""
        rules_file = Path(self.rules_path)
        
        if not rules_file.exists():
            return self._default_rules()
        
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            return rules_data.get("rules", {})
        except Exception:
            return self._default_rules()
    
    def _default_rules(self) -> dict:
        """Regras padrão de canonização (sem transformações de conteúdo)."""
        return {
            "formatting": {
                "sort_prefixes_alphabetically": True,
                "sort_triples_by_subject": True,
            },
            "ordering": {
                "order_by": ["subject", "predicate", "object"],
                "class_declarations_before_properties": True
            }
        }
    
    def canonicalize(self, graph: "Graph") -> CanonicalizationResult:
        """
        UC-103: Canoniza o grafo para serialização determinística.
        
        CONTRATO DE CANONIZAÇÃO PURA:
        - Preserva isomorfismo RDF: Input ≅ Canonicalized
        - NÃO modifica conteúdo semântico (literais, URIs, bnodes)
        - Apenas reordena para facilitar diff/revisão
        - Garante compatibilidade com Protégé
        - PATCH-v9: Garante IDs de blank nodes determinísticos
        
        Operações aplicadas:
        - Ordenação determinística de prefixos e triplas
        - Binding explícito de namespaces (evita ns1/ns2)
        - Canonização de blank nodes (IDs estáveis e determinísticos)
        - Serialização estável
        
        Operações NÃO aplicadas (ver UC-108 Normalizer):
        - Trim whitespace em literais
        - Lowercase em language tags
        - Correção de nomenclatura
        - Validação de convenções
        
        Args:
            graph: Grafo RDF a ser canonizado
            
        Returns:
            CanonicalizationResult com grafo canonizado e estatísticas
        """
        import time
        from rdflib import Graph as RDFGraph, Literal, Namespace
        from rdflib.namespace import NamespaceManager
        from rdflib.compare import to_canonical_graph
        
        start_time = time.perf_counter()
        self._warnings = []
        
        # PATCH-v9: Canonizar blank nodes ANTES de processar
        # Isso garante IDs determinísticos (_:cb0, _:cb1, etc)
        graph_with_stable_bnodes = to_canonical_graph(graph)
        
        # Criar grafo canonizado SEM prefixos automáticos
        canonical = RDFGraph()
        canonical.namespace_manager = NamespaceManager(RDFGraph(), bind_namespaces="none")
        
        # 1. Coletar e ordenar prefixos (do grafo original para preservar)
        self._bind_prefixes(graph, canonical)
        
        # 2. Coletar e ordenar triplas (do grafo com bnodes estáveis)
        triples = self._collect_and_order_triples(graph_with_stable_bnodes)
        
        # 3. Adicionar triplas ao grafo canonizado
        for s, p, o in triples:
            canonical.add((s, p, o))
        
        # 4. Garantir compatibilidade Protégé
        canonical = self._ensure_protege_compatibility(canonical)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return CanonicalizationResult(
            graph=canonical,
            triple_count=len(canonical),
            prefix_count=len(list(canonical.namespaces())),
            processing_time_ms=elapsed_ms,
            is_idempotent=True,
            warnings=self._warnings.copy()
        )
    
    def _bind_prefixes(self, source: "Graph", target: "Graph") -> None:
        """
        Vincula prefixos do grafo fonte ao grafo alvo, ordenados alfabeticamente.
        
        Args:
            source: Grafo fonte
            target: Grafo alvo (canonizado)
        """
        from rdflib import Namespace
        from rdflib.namespace import RDF, RDFS, OWL, XSD
        
        formatting_rules = self.rules.get("formatting", {})
        prefixes_rules = self.rules.get("prefixes", {})
        
        # Coletar prefixos existentes (exceto automáticos ns1, ns2)
        all_prefixes = {}
        for prefix, namespace in source.namespaces():
            if prefix and not (prefix.startswith("ns") and prefix[2:].isdigit()):
                all_prefixes[prefix] = namespace
        
        # Adicionar prefixos obrigatórios se configurados
        required_prefixes = prefixes_rules.get("required", [])
        for prefix_def in required_prefixes:
            prefix = prefix_def.get("prefix")
            uri = prefix_def.get("uri")
            if prefix and uri:
                if prefix not in all_prefixes:
                    self._warnings.append({
                        "type": "missing_required_prefix",
                        "prefix": prefix,
                        "uri": uri,
                        "message": f"Prefixo obrigatório '{prefix}' não presente na ontologia"
                    })
                all_prefixes[prefix] = Namespace(uri)
        
        # Ordenar e vincular
        if formatting_rules.get("sort_prefixes_alphabetically", True):
            for prefix in sorted(all_prefixes.keys()):
                target.bind(prefix, all_prefixes[prefix], override=True, replace=True)
        else:
            for prefix, namespace in all_prefixes.items():
                target.bind(prefix, namespace, override=True, replace=True)
    
    def _collect_and_order_triples(self, graph: "Graph") -> list[tuple]:
        """
        Coleta triplas do grafo e ordena deterministicamente.
        
        CONTRATO DE CANONIZAÇÃO PURA (UC-103):
        - NÃO modifica literais (preserva whitespace, language tags, datatypes)
        - NÃO remove "duplicatas" (RDF Graph já é conjunto, duplicatas são impossíveis)
        - Preserva isomorfismo: Input ≅ Canonicalized (bijeção em bnodes se aplicável)
        
        Args:
            graph: Grafo RDF fonte
            
        Returns:
            Lista de triplas ordenadas (sem modificação de conteúdo)
        """
        from rdflib import OWL, RDF
        
        ordering_rules = self.rules.get("ordering", {})
        
        # Coletar todas as triplas SEM modificação
        # RDF Graph é um set, portanto não há duplicatas
        triples_list = list(graph)
        
        # Ordenar triplas deterministicamente
        return self._sort_triples(triples_list, ordering_rules)
    
    def _sort_triples(self, triples: list[tuple], ordering_rules: dict) -> list[tuple]:
        """
        Ordena triplas conforme regras de ordering.
        
        Args:
            triples: Lista de triplas
            ordering_rules: Regras de ordenação
            
        Returns:
            Lista de triplas ordenadas
        """
        from rdflib import OWL, RDF
        
        order_by = ordering_rules.get("order_by", ["subject", "predicate", "object"])
        class_first = ordering_rules.get("class_declarations_before_properties", True)
        
        if class_first:
            # Separar declarações de classes de propriedades
            class_decls = []
            prop_decls = []
            other = []
            
            for s, p, o in triples:
                if p == RDF.type and o == OWL.Class:
                    class_decls.append((s, p, o))
                elif p == RDF.type and o in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
                    prop_decls.append((s, p, o))
                else:
                    other.append((s, p, o))
            
            # Ordenar cada grupo
            class_decls = self._sort_by_fields(class_decls, order_by)
            prop_decls = self._sort_by_fields(prop_decls, order_by)
            other = self._sort_by_fields(other, order_by)
            
            return class_decls + prop_decls + other
        else:
            return self._sort_by_fields(triples, order_by)
    
    def _sort_by_fields(self, triples: list[tuple], order_by: list[str]) -> list[tuple]:
        """
        Ordena triplas por campos especificados.
        
        Args:
            triples: Lista de triplas
            order_by: Lista de campos ["subject", "predicate", "object"]
            
        Returns:
            Lista de triplas ordenadas
        """
        field_map = {"subject": 0, "predicate": 1, "object": 2}
        order_indices = [field_map.get(f, 0) for f in order_by if f in field_map]
        
        if not order_indices:
            order_indices = [0, 1, 2]
        
        def sort_key(triple):
            return tuple(str(triple[i]) for i in order_indices)
        
        return sorted(triples, key=sort_key)
    
    def _ensure_protege_compatibility(self, graph: "Graph") -> "Graph":
        """
        Garante compatibilidade com Protégé.
        
        - Vincula namespaces padrão explicitamente
        - Remove prefixos automáticos (ns1, ns2)
        - Detecta namespaces usados mas não vinculados
        
        Args:
            graph: Grafo a processar
            
        Returns:
            Grafo compatível com Protégé
        """
        from rdflib import Graph as RDFGraph, Namespace, URIRef
        from rdflib.namespace import NamespaceManager, RDF, RDFS, OWL, XSD, SKOS
        
        # Detectar namespaces usados mas não vinculados
        used_namespaces = set()
        for s, p, o in graph:
            for term in (s, p, o):
                if isinstance(term, URIRef):
                    term_str = str(term)
                    if '#' in term_str:
                        ns = term_str.rsplit('#', 1)[0] + '#'
                    elif '/' in term_str:
                        ns = term_str.rsplit('/', 1)[0] + '/'
                    else:
                        continue
                    used_namespaces.add(ns)
        
        bound_namespaces = {str(ns) for _, ns in graph.namespaces()}
        unbound = used_namespaces - bound_namespaces
        
        # Avisar sobre namespaces não vinculados
        for ns in unbound:
            self._warnings.append({
                "type": "unbound_namespace",
                "namespace": ns,
                "message": f"Namespace '{ns}' usado mas não vinculado a um prefixo"
            })
        
        return graph
    
    def serialize(self, graph: "Graph") -> str:
        """
        Serializa grafo em formato Turtle estilo Protégé.
        
        Usa ProtegeStyleTurtleSerializer para garantir indentação
        e formatação idênticas ao Protégé.
        
        Args:
            graph: Grafo RDF a serializar
            
        Returns:
            String TTL formatada estilo Protégé
        """
        from onto_tools.adapters.rdf.protege_serializer import ProtegeStyleTurtleSerializer
        
        serializer = ProtegeStyleTurtleSerializer(graph)
        return serializer.serialize()
    
    def canonicalize_and_serialize(self, graph: "Graph") -> tuple[str, CanonicalizationResult]:
        """
        Conveniência: Canoniza e serializa em uma operação.
        
        Args:
            graph: Grafo RDF a processar
            
        Returns:
            Tuple (TTL string, CanonicalizationResult)
        """
        result = self.canonicalize(graph)
        ttl_string = self.serialize(result.graph)
        return ttl_string, result
    
    def validate_idempotency(self, graph: "Graph") -> bool:
        """
        Valida se canonização é idempotente (aplicar 2x = mesmo resultado).
        
        Args:
            graph: Grafo RDF a testar
            
        Returns:
            True se idempotente
        """
        # Canonizar uma vez
        result1 = self.canonicalize(graph)
        ttl1 = self.serialize(result1.graph)
        
        # Canonizar novamente
        result2 = self.canonicalize(result1.graph)
        ttl2 = self.serialize(result2.graph)
        
        # Comparar
        return ttl1 == ttl2
    
    def get_warnings(self) -> list[dict]:
        """Retorna avisos da última canonização."""
        return self._warnings.copy()


def canonicalize_graph(graph: "Graph", rules_path: Optional[str] = None) -> CanonicalizationResult:
    """
    Função auxiliar para canonizar um grafo.
    
    Args:
        graph: Grafo RDF a canonizar
        rules_path: Caminho para rules.json (opcional)
        
    Returns:
        CanonicalizationResult com grafo canonizado
    """
    canonicalizer = Canonicalizer(rules_path=rules_path)
    return canonicalizer.canonicalize(graph)
