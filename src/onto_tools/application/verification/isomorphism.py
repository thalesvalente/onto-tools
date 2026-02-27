"""
Isomorphism - RDF graph isomorphism comparison.

Uses rdflib.compare.isomorphic for semantically equivalent comparison.
Two graphs are isomorphic if they represent the same triples modulo blank node labels.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Set, Tuple, Union

from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff


@dataclass
class IsomorphismReport:
    """
    Report of isomorphism comparison between two RDF graphs.
    
    Attributes:
        are_isomorphic: True if graphs are semantically equivalent
        graph_a_path: Path to first graph file
        graph_b_path: Path to second graph file
        graph_a_triple_count: Number of triples in first graph
        graph_b_triple_count: Number of triples in second graph
        triples_only_in_a: Count of triples only in A (if not isomorphic)
        triples_only_in_b: Count of triples only in B (if not isomorphic)
        sample_diff_a: Sample triples only in A (max 5)
        sample_diff_b: Sample triples only in B (max 5)
        error: Error message if comparison failed
    """
    are_isomorphic: bool
    graph_a_path: str
    graph_b_path: str
    graph_a_triple_count: int = 0
    graph_b_triple_count: int = 0
    triples_only_in_a: int = 0
    triples_only_in_b: int = 0
    sample_diff_a: list = field(default_factory=list)
    sample_diff_b: list = field(default_factory=list)
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "are_isomorphic": self.are_isomorphic,
            "graph_a_path": self.graph_a_path,
            "graph_b_path": self.graph_b_path,
            "graph_a_triple_count": self.graph_a_triple_count,
            "graph_b_triple_count": self.graph_b_triple_count,
            "triples_only_in_a": self.triples_only_in_a,
            "triples_only_in_b": self.triples_only_in_b,
            "sample_diff_a": self.sample_diff_a,
            "sample_diff_b": self.sample_diff_b,
            "error": self.error
        }


def _load_graph(path: Union[str, Path], format: Optional[str] = None) -> Graph:
    """
    Load RDF graph from file.
    
    Args:
        path: Path to the RDF file
        format: RDF format (auto-detected if None)
        
    Returns:
        Loaded rdflib.Graph
    """
    path = Path(path)
    
    if format is None:
        # Auto-detect format from extension
        ext = path.suffix.lower()
        format_map = {
            ".ttl": "turtle",
            ".turtle": "turtle",
            ".n3": "n3",
            ".nt": "nt",
            ".ntriples": "nt",
            ".rdf": "xml",
            ".xml": "xml",
            ".owl": "xml",
            ".jsonld": "json-ld",
            ".json": "json-ld",
        }
        format = format_map.get(ext, "turtle")
    
    g = Graph()
    g.parse(str(path), format=format)
    return g


def _triple_to_str(triple: Tuple) -> str:
    """Convert a triple to string representation."""
    s, p, o = triple
    return f"({s}, {p}, {o})"


def compare_isomorphism(
    path_a: Union[str, Path],
    path_b: Union[str, Path],
    format_a: Optional[str] = None,
    format_b: Optional[str] = None,
    max_diff_samples: int = 5
) -> IsomorphismReport:
    """
    Compare two RDF graphs for isomorphism.
    
    Two graphs are isomorphic if they represent the same set of triples
    modulo blank node labels. This is the standard for semantic equivalence.
    
    Args:
        path_a: Path to first RDF file
        path_b: Path to second RDF file
        format_a: RDF format for first file (auto-detected if None)
        format_b: RDF format for second file (auto-detected if None)
        max_diff_samples: Maximum number of diff samples to include
        
    Returns:
        IsomorphismReport with comparison results
        
    Example:
        >>> report = compare_isomorphism("original.ttl", "canonicalized.ttl")
        >>> if report.are_isomorphic:
        ...     print("Graphs are semantically equivalent")
    """
    path_a = Path(path_a)
    path_b = Path(path_b)
    
    try:
        # Load both graphs
        graph_a = _load_graph(path_a, format_a)
        graph_b = _load_graph(path_b, format_b)
        
        # Count triples
        count_a = len(graph_a)
        count_b = len(graph_b)
        
        # Check isomorphism
        are_iso = isomorphic(graph_a, graph_b)
        
        report = IsomorphismReport(
            are_isomorphic=are_iso,
            graph_a_path=str(path_a),
            graph_b_path=str(path_b),
            graph_a_triple_count=count_a,
            graph_b_triple_count=count_b
        )
        
        # If not isomorphic, compute diff
        if not are_iso:
            in_both, only_in_a, only_in_b = graph_diff(graph_a, graph_b)
            
            report.triples_only_in_a = len(only_in_a)
            report.triples_only_in_b = len(only_in_b)
            
            # Sample diffs
            for i, triple in enumerate(only_in_a):
                if i >= max_diff_samples:
                    break
                report.sample_diff_a.append(_triple_to_str(triple))
            
            for i, triple in enumerate(only_in_b):
                if i >= max_diff_samples:
                    break
                report.sample_diff_b.append(_triple_to_str(triple))
        
        return report
        
    except FileNotFoundError as e:
        return IsomorphismReport(
            are_isomorphic=False,
            graph_a_path=str(path_a),
            graph_b_path=str(path_b),
            error=f"File not found: {e}"
        )
    except Exception as e:
        return IsomorphismReport(
            are_isomorphic=False,
            graph_a_path=str(path_a),
            graph_b_path=str(path_b),
            error=f"Comparison failed: {type(e).__name__}: {e}"
        )


def compare_graphs(
    graph_a: Graph,
    graph_b: Graph,
    label_a: str = "graph_a",
    label_b: str = "graph_b",
    max_diff_samples: int = 5
) -> IsomorphismReport:
    """
    Compare two in-memory RDF graphs for isomorphism.
    
    Args:
        graph_a: First rdflib.Graph
        graph_b: Second rdflib.Graph
        label_a: Label for first graph in report
        label_b: Label for second graph in report
        max_diff_samples: Maximum number of diff samples to include
        
    Returns:
        IsomorphismReport with comparison results
    """
    try:
        count_a = len(graph_a)
        count_b = len(graph_b)
        
        are_iso = isomorphic(graph_a, graph_b)
        
        report = IsomorphismReport(
            are_isomorphic=are_iso,
            graph_a_path=label_a,
            graph_b_path=label_b,
            graph_a_triple_count=count_a,
            graph_b_triple_count=count_b
        )
        
        if not are_iso:
            in_both, only_in_a, only_in_b = graph_diff(graph_a, graph_b)
            
            report.triples_only_in_a = len(only_in_a)
            report.triples_only_in_b = len(only_in_b)
            
            for i, triple in enumerate(only_in_a):
                if i >= max_diff_samples:
                    break
                report.sample_diff_a.append(_triple_to_str(triple))
            
            for i, triple in enumerate(only_in_b):
                if i >= max_diff_samples:
                    break
                report.sample_diff_b.append(_triple_to_str(triple))
        
        return report
        
    except Exception as e:
        return IsomorphismReport(
            are_isomorphic=False,
            graph_a_path=label_a,
            graph_b_path=label_b,
            error=f"Comparison failed: {type(e).__name__}: {e}"
        )
