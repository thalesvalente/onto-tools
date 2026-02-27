"""
Serializador Turtle estilo Protégé.

Este módulo implementa um serializador que produz arquivos TTL
com indentação e alinhamento compatíveis com o Protégé.
"""

from collections import defaultdict
from typing import Any

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD, DCTERMS


class ProtegeStyleTurtleSerializer:
    """
    Serializador Turtle que produz output compatível com Protégé.
    
    Características:
    - Predicados alinhados na mesma coluna
    - Objetos múltiplos alinhados sob o primeiro objeto
    - Ordenação determinística de sujeitos e predicados
    - Blocos de sujeitos separados por linha em branco
    """

    # Ordem preferencial de predicados (como Protégé faz)
    PREDICATE_ORDER = [
        str(RDF.type),
        str(RDFS.subClassOf),
        str(RDFS.subPropertyOf),
        str(RDFS.domain),
        str(RDFS.range),
        str(OWL.equivalentClass),
        str(OWL.disjointWith),
        str(OWL.inverseOf),
        str(DCTERMS.identifier),
        str(RDFS.label),
        str(SKOS.prefLabel),
        str(SKOS.altLabel),
        str(SKOS.definition),
        str(RDFS.comment),
        str(SKOS.note),
        str(SKOS.example),
    ]

    def __init__(self, graph: Graph):
        """
        Inicializa o serializador.
        
        Args:
            graph: Grafo RDF a ser serializado.
        """
        self.graph = graph
        self.ns_manager = graph.namespace_manager
        self._prefix_map: dict[str, str] = {}
        self._build_prefix_map()

    def _build_prefix_map(self) -> None:
        """Constrói mapa de namespaces para prefixos."""
        for prefix, namespace in self.ns_manager.namespaces():
            self._prefix_map[str(namespace)] = prefix

    def serialize(self) -> str:
        """
        Serializa o grafo em formato Turtle estilo Protégé.
        
        Returns:
            String com o conteúdo TTL formatado.
        """
        lines: list[str] = []
        
        # 1. Gerar declarações de prefixo
        lines.extend(self._serialize_prefixes())
        lines.append("")  # Linha em branco após prefixos
        
        # 2. Agrupar triplas por sujeito
        subjects_data = self._group_by_subject()
        
        # 3. Ordenar sujeitos (URIs primeiro, depois BNodes)
        sorted_subjects = self._sort_subjects(list(subjects_data.keys()))
        
        # 4. Serializar cada bloco de sujeito
        for i, subject in enumerate(sorted_subjects):
            predicates = subjects_data[subject]
            block = self._serialize_subject_block(subject, predicates)
            lines.extend(block)
            
            # Linha em branco entre blocos (exceto após o último)
            if i < len(sorted_subjects) - 1:
                lines.append("")
        
        return "\n".join(lines) + "\n"

    def _serialize_prefixes(self) -> list[str]:
        """Gera declarações de prefixo ordenadas, apenas para prefixos usados."""
        # Coletar todos os namespaces realmente usados no grafo
        used_namespaces: set[str] = set()
        
        for s, p, o in self.graph:
            for node in (s, p, o):
                if isinstance(node, URIRef):
                    uri = str(node)
                    # Encontrar o namespace correspondente
                    for ns, prefix in self._prefix_map.items():
                        if uri.startswith(ns) and prefix:
                            used_namespaces.add(ns)
                            break
        
        # Filtrar apenas prefixos usados
        prefixes: list[tuple[str, str]] = []
        
        for prefix, namespace in self.ns_manager.namespaces():
            ns_str = str(namespace)
            if prefix and ns_str in used_namespaces:
                prefixes.append((prefix, ns_str))
        
        # Ordenar alfabeticamente
        prefixes.sort(key=lambda x: x[0])
        
        return [f"@prefix {prefix}: <{ns}> ." for prefix, ns in prefixes]

    def _group_by_subject(self) -> dict[Any, dict[str, list[Any]]]:
        """
        Agrupa triplas por sujeito e predicado.
        
        Returns:
            Dict de sujeito -> dict de predicado -> lista de objetos
        """
        subjects: dict[Any, dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
        
        for s, p, o in self.graph:
            subjects[s][str(p)].append(o)
        
        return subjects

    def _sort_subjects(self, subjects: list[Any]) -> list[Any]:
        """
        Ordena sujeitos: URIs primeiro (alfabético), depois BNodes.
        """
        uris = [s for s in subjects if isinstance(s, URIRef)]
        bnodes = [s for s in subjects if isinstance(s, BNode)]
        
        # Ordenar URIs pelo QName ou URI completa
        uris.sort(key=lambda x: self._to_qname(x))
        
        # BNodes por identificador
        bnodes.sort(key=str)
        
        return uris + bnodes

    def _sort_predicates(self, predicates: list[str]) -> list[str]:
        """
        Ordena predicados seguindo a ordem preferencial do Protégé.
        """
        def pred_key(p: str) -> tuple[int, str]:
            try:
                idx = self.PREDICATE_ORDER.index(p)
            except ValueError:
                idx = len(self.PREDICATE_ORDER)
            return (idx, p)
        
        return sorted(predicates, key=pred_key)

    def _serialize_subject_block(
        self, 
        subject: Any, 
        predicates: dict[str, list[Any]]
    ) -> list[str]:
        """
        Serializa um bloco de sujeito com alinhamento estilo Protégé.
        
        Args:
            subject: O sujeito (URIRef ou BNode)
            predicates: Dict de predicado -> lista de objetos
            
        Returns:
            Lista de linhas formatadas
        """
        lines: list[str] = []
        
        # Obter representação do sujeito
        subject_str = self._to_qname(subject)
        
        # Ordenar predicados
        sorted_preds = self._sort_predicates(list(predicates.keys()))
        
        if not sorted_preds:
            return lines
        
        # Calcular coluna onde predicados devem começar
        # (após o sujeito + 1 espaço)
        col_pred_start = len(subject_str) + 1
        indent_pred = " " * col_pred_start
        
        # Processar cada predicado
        for pred_idx, pred_uri in enumerate(sorted_preds):
            objects = predicates[pred_uri]
            pred_str = self._to_qname(URIRef(pred_uri))
            
            # Ordenar objetos para determinismo
            sorted_objects = self._sort_objects(objects)
            
            # Determinar pontuação final
            is_last_pred = (pred_idx == len(sorted_preds) - 1)
            
            # Gerar linhas para este predicado
            pred_lines = self._serialize_predicate_objects(
                pred_str=pred_str,
                objects=sorted_objects,
                col_pred_start=col_pred_start,
                is_first_pred=(pred_idx == 0),
                is_last_pred=is_last_pred,
                subject_str=subject_str
            )
            
            lines.extend(pred_lines)
        
        return lines

    def _serialize_predicate_objects(
        self,
        pred_str: str,
        objects: list[Any],
        col_pred_start: int,
        is_first_pred: bool,
        is_last_pred: bool,
        subject_str: str
    ) -> list[str]:
        """
        Serializa um predicado com seus objetos.
        
        Args:
            pred_str: QName do predicado
            objects: Lista de objetos
            col_pred_start: Coluna onde o predicado começa
            is_first_pred: Se é o primeiro predicado do bloco
            is_last_pred: Se é o último predicado do bloco
            subject_str: QName do sujeito (para primeira linha)
            
        Returns:
            Lista de linhas formatadas
        """
        lines: list[str] = []
        indent_pred = " " * col_pred_start
        
        if not objects:
            return lines
        
        # Primeiro objeto
        first_obj_str = self._format_object(objects[0])
        
        # Calcular coluna onde objetos devem começar
        col_obj_start = col_pred_start + len(pred_str) + 1
        indent_obj = " " * col_obj_start
        
        # Determinar pontuação
        if len(objects) == 1:
            # Único objeto
            punct = " ." if is_last_pred else " ;"
        else:
            # Múltiplos objetos - primeiro termina com vírgula
            punct = " ,"
        
        # Primeira linha do predicado
        if is_first_pred:
            # Inclui o sujeito
            lines.append(f"{subject_str} {pred_str} {first_obj_str}{punct}")
        else:
            # Apenas predicado indentado
            lines.append(f"{indent_pred}{pred_str} {first_obj_str}{punct}")
        
        # Objetos adicionais (alinhados sob o primeiro objeto)
        for obj_idx, obj in enumerate(objects[1:], start=1):
            obj_str = self._format_object(obj)
            
            # Último objeto deste predicado?
            is_last_obj = (obj_idx == len(objects) - 1)
            
            if is_last_obj:
                punct = " ." if is_last_pred else " ;"
            else:
                punct = " ,"
            
            lines.append(f"{indent_obj}{obj_str}{punct}")
        
        return lines

    def _sort_objects(self, objects: list[Any]) -> list[Any]:
        """
        Ordena objetos para output determinístico.
        
        Ordem: URIs, Literais (por idioma, depois valor), BNodes
        """
        uris = [o for o in objects if isinstance(o, URIRef)]
        literals = [o for o in objects if isinstance(o, Literal)]
        bnodes = [o for o in objects if isinstance(o, BNode)]
        
        # URIs por QName
        uris.sort(key=lambda x: self._to_qname(x))
        
        # Literais por idioma (en primeiro, depois pt-br, depois outros), depois valor
        def literal_key(lit: Literal) -> tuple[int, str, str]:
            lang = lit.language or ""
            lang_order = {"en": 0, "en-us": 1, "en-gb": 2, "pt-br": 10, "pt": 11}.get(lang, 50)
            return (lang_order, lang, str(lit))
        
        literals.sort(key=literal_key)
        
        # BNodes por id
        bnodes.sort(key=str)
        
        return uris + literals + bnodes

    def _to_qname(self, node: URIRef | BNode) -> str:
        """
        Converte um nó para QName ou representação apropriada.
        """
        if isinstance(node, BNode):
            return f"_:{node}"
        
        uri = str(node)
        
        # Tentar encontrar prefixo
        for namespace, prefix in self._prefix_map.items():
            if uri.startswith(namespace):
                local = uri[len(namespace):]
                if prefix:
                    return f"{prefix}:{local}"
                else:
                    return f":{local}"
        
        # Fallback: URI completa entre <>
        return f"<{uri}>"

    def _format_object(self, obj: Any) -> str:
        """
        Formata um objeto RDF para Turtle.
        """
        if isinstance(obj, URIRef):
            return self._to_qname(obj)
        
        if isinstance(obj, BNode):
            return f"_:{obj}"
        
        if isinstance(obj, Literal):
            return self._format_literal(obj)
        
        # Fallback
        return str(obj)

    def _format_literal(self, lit: Literal) -> str:
        """
        Formata um literal RDF para Turtle.
        """
        value = str(lit)
        
        # Escapar caracteres especiais
        value = value.replace("\\", "\\\\")
        value = value.replace('"', '\\"')
        value = value.replace("\n", "\\n")
        value = value.replace("\r", "\\r")
        value = value.replace("\t", "\\t")
        
        # Construir representação
        if lit.language:
            return f'"{value}"@{lit.language}'
        elif lit.datatype:
            datatype_qname = self._to_qname(lit.datatype)
            # Tipos comuns podem ser omitidos ou simplificados
            if lit.datatype == XSD.string:
                return f'"{value}"'
            elif lit.datatype == XSD.integer:
                # Inteiros podem ser escritos sem aspas
                try:
                    int(value)
                    return value
                except ValueError:
                    return f'"{value}"^^{datatype_qname}'
            elif lit.datatype == XSD.decimal:
                return value
            elif lit.datatype == XSD.boolean:
                return value.lower()
            else:
                return f'"{value}"^^{datatype_qname}'
        else:
            return f'"{value}"'


def serialize_protege_style(graph: Graph) -> str:
    """
    Função auxiliar para serializar um grafo em estilo Protégé.
    
    Args:
        graph: Grafo RDF a ser serializado.
        
    Returns:
        String com o conteúdo TTL formatado.
    """
    serializer = ProtegeStyleTurtleSerializer(graph)
    return serializer.serialize()
