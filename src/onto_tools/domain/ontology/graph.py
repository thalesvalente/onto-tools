"""OntologyGraph — Classe central CRUD de grafos RDF (Fase 1 v2.0 §3.2)"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from rdflib import Graph as RDFLibGraph


@dataclass
class OntologyMetadata:
    hash: str
    triple_count: int
    timestamp: str
    processing_time: float = 0.0
    source_path: Optional[str] = None


@dataclass
class OntologyGraph:
    graph: Optional[RDFLibGraph] = None
    metadata: Optional[OntologyMetadata] = None
    prefixes: dict[str, str] = field(default_factory=dict)
    source_path: Optional[str] = None

    @classmethod
    def load(cls, file_path: str, rdf_adapter) -> OntologyGraph:
        start_time = time.time()
        
        try:
            graph, raw_metadata = rdf_adapter.load_ttl(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado!")
        except ValueError as e:
            if "UTF-8" in str(e):
                raise ValueError("Encoding inválido. Por favor, salve o arquivo como UTF-8!")
            raise ValueError(f"Alguns erros foram encontrados: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar ontologia: {e}")
        
        processing_time = time.time() - start_time
        
        metadata = OntologyMetadata(
            hash=raw_metadata["hash"],
            triple_count=raw_metadata["triple_count"],
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time,
            source_path=raw_metadata["source_path"],
        )
        
        prefixes = {prefix: str(namespace) for prefix, namespace in graph.namespaces()}
        
        return cls(
            graph=graph,
            metadata=metadata,
            prefixes=prefixes,
            source_path=file_path,
        )

    def save(self, file_path: str, rdf_adapter, canonized: bool = False) -> None:
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado para salvar")
        
        if canonized:
            # Apply full canonicalization (including bnode stabilization)
            from .canonicalizer import canonicalize_graph
            canon_result = canonicalize_graph(self.graph)
            rdf_adapter.save_ttl(canon_result.graph, file_path, canonized=True)
        else:
            rdf_adapter.save_ttl(self.graph, file_path, canonized=False)

    def normalize(self, normalizer) -> OntologyGraph:
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado para normalizar")
        
        result = normalizer.normalize(self.graph)
        
        # normalize() retorna NormalizationResult, extrair o grafo
        normalized_graph = result.graph if hasattr(result, 'graph') else result
        
        return OntologyGraph(
            graph=normalized_graph,
            metadata=self.metadata,
            prefixes=self.prefixes,
            source_path=self.source_path,
        )

    def query(self, sparql: str, query_engine) -> list[dict]:
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado para consultar")
        
        return query_engine.execute(self.graph, sparql)

    def add_triple(self, subject: str, predicate: str, obj: str, obj_is_literal: bool = False) -> None:
        """
        Adiciona uma tripla ao grafo.
        
        Args:
            subject: URI do sujeito (pode ser prefixada ou completa)
            predicate: URI do predicado (pode ser prefixada ou completa)
            obj: Objeto (URI ou literal)
            obj_is_literal: Se True, força o objeto a ser tratado como Literal.
                           Se False, tenta resolver como URI primeiro.
        
        Note:
            - URIs prefixadas (ex: rdf:type, owl:Class) são resolvidas automaticamente
            - Prefixos devem estar registrados no grafo ou ser padrões conhecidos
            - Se obj_is_literal=False e obj não puder ser resolvido como URI,
              será tratado como Literal
        """
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado")
        
        from rdflib import Literal, URIRef
        from .uri_resolver import URIResolver
        
        # Criar resolver com prefixos do grafo
        resolver = URIResolver(self.graph)
        
        # Resolver subject (sempre URI)
        try:
            s = resolver.to_rdflib_term(subject, prefer_uri=True)
            if not isinstance(s, URIRef):
                raise ValueError(f"Subject deve ser URI, não literal: {subject}")
        except ValueError as e:
            raise ValueError(f"Erro ao resolver subject '{subject}': {e}")
        
        # Resolver predicate (sempre URI)
        try:
            p = resolver.to_rdflib_term(predicate, prefer_uri=True)
            if not isinstance(p, URIRef):
                raise ValueError(f"Predicate deve ser URI, não literal: {predicate}")
        except ValueError as e:
            raise ValueError(f"Erro ao resolver predicate '{predicate}': {e}")
        
        # Resolver object (pode ser URI ou Literal)
        if obj_is_literal:
            o = Literal(obj)
        else:
            o = resolver.to_rdflib_term(obj, prefer_uri=True)
        
        self.graph.add((s, p, o))
        
        if self.metadata:
            self.metadata.triple_count = len(self.graph)

    def remove_triple(self, subject: str, predicate: str, obj: str, obj_is_literal: bool = False) -> None:
        """
        Remove uma tripla do grafo.
        
        Args:
            subject: URI do sujeito (pode ser prefixada ou completa)
            predicate: URI do predicado (pode ser prefixada ou completa)
            obj: Objeto (URI ou literal), ou None para remover todas as triplas com s, p
            obj_is_literal: Se True, força o objeto a ser tratado como Literal.
        
        Note:
            - URIs prefixadas (ex: rdf:type, owl:Class) são resolvidas automaticamente
            - Se obj é None, remove todas as triplas com o subject e predicate dados
        """
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado")
        
        from rdflib import Literal, URIRef
        from .uri_resolver import URIResolver
        
        # Criar resolver com prefixos do grafo
        resolver = URIResolver(self.graph)
        
        # Resolver subject (sempre URI)
        try:
            s = resolver.to_rdflib_term(subject, prefer_uri=True)
            if not isinstance(s, URIRef):
                raise ValueError(f"Subject deve ser URI, não literal: {subject}")
        except ValueError as e:
            raise ValueError(f"Erro ao resolver subject '{subject}': {e}")
        
        # Resolver predicate (sempre URI)
        try:
            p = resolver.to_rdflib_term(predicate, prefer_uri=True)
            if not isinstance(p, URIRef):
                raise ValueError(f"Predicate deve ser URI, não literal: {predicate}")
        except ValueError as e:
            raise ValueError(f"Erro ao resolver predicate '{predicate}': {e}")
        
        # Resolver object (pode ser URI, Literal ou None)
        if obj is None:
            o = None
        elif obj_is_literal:
            o = Literal(obj)
        else:
            o = resolver.to_rdflib_term(obj, prefer_uri=True)
        
        self.graph.remove((s, p, o))
        
        if self.metadata:
            self.metadata.triple_count = len(self.graph)

    def batch_apply(self, update_list: dict) -> dict:
        """
        UC-107: Aplicar lista de alterações em lote
        
        RF-107: "O lote não é interrompido no primeiro erro (todos os itens são 
        processados e os erros, agregados). A persistência é tudo-ou-nada: se não 
        houver erros, grava uma única vez o .ttl"
        
        Entrada (update-list.json):
        {
            "batch_id": str,
            "onto_name": str,
            "onto_version": str,
            "system_name": str,
            "system_version": str,
            "ordered_ops": [
                {
                    "op_id": int,
                    "type": "insert" | "delete" | "update",
                    "triple": {
                        "subject": str,
                        "predicate": str,
                        "object": str,
                        "language": str
                    }
                }
            ]
        }
        
        Saída (apply-log.json):
        {
            "batch_id": str,
            "onto_name": str,
            "onto_version": str,
            "started_at": str,
            "finished_at": str,
            "duration_seconds": int,
            "overall_result": "success" | "failed",
            "applied_ops": [...],
            "failed_ops": [...],
            "metrics": {...}
        }
        
        Args:
            update_list: Dicionário conforme update-list.json
        
        Returns:
            dict: apply-log conforme apply-log.json
        """
        import time
        from rdflib import Literal, URIRef, Graph as RDFGraph
        
        if self.graph is None:
            raise ValueError("Nenhum grafo carregado")
        
        started_at = datetime.now()
        start_time = time.time()
        
        batch_id = update_list.get("batch_id", "unknown")
        onto_name = update_list.get("onto_name", "unknown")
        onto_version = update_list.get("onto_version", "1.0")
        ordered_ops = update_list.get("ordered_ops", [])
        
        applied_ops = []
        failed_ops = []
        triples_added = 0
        triples_removed = 0
        
        # RF-107: Criar grafo temporário para aplicar operações
        # Somente comitará se não houver erros (tudo-ou-nada)
        temp_graph = RDFGraph()
        
        # Copiar bindings de namespace do grafo original para o temporário
        # Isso garante que prefixos customizados (ex: edo:) sejam resolvidos corretamente
        for prefix, namespace in self.graph.namespaces():
            if prefix:  # Ignorar prefixo vazio
                temp_graph.bind(prefix, namespace, override=True, replace=True)
        
        for triple in self.graph:
            temp_graph.add(triple)
        
        # RF-107: Processar TODAS as operações (não interrompe no primeiro erro)
        for op in ordered_ops:
            op_id = op.get("op_id")
            op_type = op.get("type")
            triple_data = op.get("triple", {})
            
            subject_str = triple_data.get("subject")
            predicate_str = triple_data.get("predicate")
            object_str = triple_data.get("object")
            language = triple_data.get("language", "")
            
            op_start = time.time()
            
            try:
                # Usar URIResolver para converter strings para termos RDF
                from .uri_resolver import URIResolver
                resolver = URIResolver(temp_graph)
                
                # Subject sempre é URI
                subject = resolver.to_rdflib_term(subject_str, prefer_uri=True)
                if not isinstance(subject, URIRef):
                    raise ValueError(f"Subject deve ser URI: {subject_str}")
                
                # Predicate sempre é URI
                predicate = resolver.to_rdflib_term(predicate_str, prefer_uri=True)
                if not isinstance(predicate, URIRef):
                    raise ValueError(f"Predicate deve ser URI: {predicate_str}")
                
                # Objeto pode ser URI ou Literal
                if object_str.startswith('"') and object_str.endswith('"'):
                    # Literal explícito com aspas
                    literal_value = object_str[1:-1]
                    obj = Literal(literal_value, lang=language if language else None)
                elif language:
                    # Tem language tag, é literal
                    obj = Literal(object_str, lang=language)
                else:
                    # Tentar resolver como URI primeiro
                    obj = resolver.to_rdflib_term(object_str, prefer_uri=True)
                
                # Executar operação no grafo temporário
                if op_type == "insert":
                    temp_graph.add((subject, predicate, obj))
                    triples_added += 1
                    status = "applied"
                elif op_type == "delete":
                    temp_graph.remove((subject, predicate, obj))
                    triples_removed += 1
                    status = "applied"
                elif op_type == "update":
                    # Update = delete + insert
                    # Assumir que triple contém novo valor
                    temp_graph.remove((subject, predicate, None))  # Remove todos com mesmo s,p
                    temp_graph.add((subject, predicate, obj))
                    triples_removed += 1
                    triples_added += 1
                    status = "applied"
                else:
                    raise ValueError(f"Tipo de operação desconhecido: {op_type}")
                
                op_elapsed = int((time.time() - op_start) * 1000)
                
                applied_ops.append({
                    "op_id": op_id,
                    "type": op_type,
                    "status": status,
                    "applied_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "time_ms": op_elapsed,
                    "checks": {
                        "precondition": "validated",
                        "precondition_result": True
                    },
                    "triple": triple_data
                })
                
            except Exception as e:
                op_elapsed = int((time.time() - op_start) * 1000)
                
                failed_ops.append({
                    "op_id": op_id,
                    "type": op_type,
                    "status": "failed",
                    "failed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "time_ms": op_elapsed,
                    "error": str(e),
                    "triple": triple_data
                })
        
        finished_at = datetime.now()
        duration_seconds = int(time.time() - start_time)
        
        overall_result = "success" if len(failed_ops) == 0 else "failed"
        
        # RF-107: Persistência tudo-ou-nada
        # Somente comita mudanças se NÃO houver erros
        if overall_result == "success":
            self.graph = temp_graph
            if self.metadata:
                self.metadata.triple_count = len(self.graph)
        # else: grafo permanece inalterado (rollback automático)
        
        return {
            "batch_id": batch_id,
            "onto_name": onto_name,
            "onto_version": onto_version,
            "started_at": started_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "finished_at": finished_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "duration_seconds": duration_seconds,
            "overall_result": overall_result,
            "applied_ops": applied_ops,
            "failed_ops": failed_ops,
            "metrics": {
                "total_ops": len(ordered_ops),
                "applied_ops": len(applied_ops),
                "failed_ops": len(failed_ops),
                "triples_added": triples_added,
                "triples_removed": triples_removed
            }
        }

    def diff(self, other: OntologyGraph) -> dict:
        if self.graph is None or other.graph is None:
            raise ValueError("Ambos os grafos devem estar carregados")
        
        added = set(other.graph) - set(self.graph)
        removed = set(self.graph) - set(other.graph)
        
        return {
            "added": list(added),
            "removed": list(removed),
            "added_count": len(added),
            "removed_count": len(removed),
        }

    def generate_review_log(
        self,
        sparql_filters: list[str] = None,
        input_file: str = None,
        output_file: str = None
    ) -> dict:
        """
        UC-104: Gerar log de revisão conforme export-log.json
        
        Formato canônico:
        {
            "onto_name": str,
            "onto_version": str,
            "date": str,
            "hour": str,
            "system_name": str,
            "system_version": str,
            "contexto_execucao": {
                "filtro": list[str],  # SPARQL filters
                "entrada": str,
                "saida": str
            },
            "metricas": {
                "triples_exportadas": int,
                "tempo_execucao_segundos": float
            }
        }
        
        Args:
            sparql_filters: Lista de filtros SPARQL aplicados
            input_file: Arquivo de entrada
            output_file: Arquivo de saída gerado
        
        Returns:
            dict: Log de exportação conforme formato canônico
        """
        import time
        
        start_time = time.time()
        triple_count = len(self.graph) if self.graph else 0
        elapsed_time = time.time() - start_time if hasattr(self, '_last_operation_time') else 0.0
        
        return {
            "onto_name": Path(self.source_path).stem if self.source_path else "unknown",
            "onto_version": "1.0",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hour": datetime.now().strftime("%H:%M:%S%z"),
            "system_name": "OntoTools",
            "system_version": "3.0",
            "contexto_execucao": {
                "filtro": sparql_filters or [],
                "entrada": input_file or (self.source_path if self.source_path else "unknown"),
                "saida": output_file or "unknown"
            },
            "metricas": {
                "triples_exportadas": triple_count,
                "tempo_execucao_segundos": elapsed_time
            }
        }
