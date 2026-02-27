#!/usr/bin/env python3
"""
RDF Graph Isomorphism Checker — Semantic Preservation Gate
Patch-v5 — OntoTools Núcleo 1

Objetivo: Provar que canonização e normalização preservam semântica RDF
via isomorfismo de grafos (permite renomeação de bnodes por bijeção).

Uso:
    python scripts/isomorphism_check.py

Saída:
    outputs/logs/isomorphism_check_<timestamp>.json
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff

def sha256_file(filepath: Path) -> str:
    """Calcula SHA256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_graph(filepath: Path, format="turtle") -> Graph:
    """Carrega grafo RDF de arquivo."""
    g = Graph()
    g.parse(str(filepath), format=format)
    return g

def compare_graphs(g1: Graph, g2: Graph, label1: str, label2: str) -> dict:
    """
    Compara dois grafos RDF via isomorfismo.
    
    Returns:
        dict com:
        - isomorphic: bool
        - triples_g1: int
        - triples_g2: int
        - only_in_g1_count: int (se não isomórfico)
        - only_in_g2_count: int (se não isomórfico)
        - sample_only_in_g1: list[str] (até 10 triplas NT)
        - sample_only_in_g2: list[str] (até 10 triplas NT)
    """
    result = {
        "label1": label1,
        "label2": label2,
        "triples_g1": len(g1),
        "triples_g2": len(g2),
        "isomorphic": isomorphic(g1, g2)
    }
    
    if not result["isomorphic"]:
        # Gerar diff
        in_both, in_first, in_second = graph_diff(g1, g2)
        
        result["only_in_g1_count"] = len(in_first)
        result["only_in_g2_count"] = len(in_second)
        
        # Amostra de triplas (até 10 de cada) — graph_diff retorna Graph objects
        result["sample_only_in_g1"] = [
            f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in list(in_first)[:10]
        ]
        result["sample_only_in_g2"] = [
            f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in list(in_second)[:10]
        ]
    
    return result

def main():
    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Paths
    project_root = Path(__file__).parent.parent
    input_path = project_root / "data" / "edo" / "core" / "energy-domain-ontology.ttl"
    review_dir = project_root / "data" / "edo" / "governance" / "review"
    
    # Identificar outputs dos 3 runs
    output_run1 = review_dir / "result-normalization.ttl"
    output_run2 = review_dir / "result-canonicalization.ttl"
    output_run3 = review_dir / "result-normalization-canonicalization.ttl"
    
    # Verificar existência
    files_to_check = {
        "input": input_path,
        "run1_normalized": output_run1,
        "run2_canonicalized": output_run2,
        "run3_combined": output_run3
    }
    
    missing_files = [k for k, v in files_to_check.items() if not v.exists()]
    if missing_files:
        print(f"ERRO: Arquivos não encontrados: {missing_files}", file=sys.stderr)
        sys.exit(1)
    
    print(f"[{timestamp}] Iniciando verificação de isomorfismo RDF...")
    print(f"Input: {input_path}")
    print(f"Run1 (normalize): {output_run1}")
    print(f"Run2 (canonicalize): {output_run2}")
    print(f"Run3 (combined): {output_run3}")
    
    # Calcular hashes
    hashes = {k: sha256_file(v) for k, v in files_to_check.items()}
    print("\nSHA256 hashes:")
    for k, h in hashes.items():
        print(f"  {k}: {h}")
    
    # Carregar grafos
    print("\nCarregando grafos...")
    try:
        g_input = load_graph(input_path)
        g_run1 = load_graph(output_run1)
        g_run2 = load_graph(output_run2)
        g_run3 = load_graph(output_run3)
        
        print(f"  Input: {len(g_input)} triplas")
        print(f"  Run1: {len(g_run1)} triplas")
        print(f"  Run2: {len(g_run2)} triplas")
        print(f"  Run3: {len(g_run3)} triplas")
    except Exception as e:
        print(f"ERRO ao carregar grafos: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Comparações
    print("\nExecutando comparações de isomorfismo...")
    comparisons = []
    
    # A vs B (input vs normalized)
    print("  [1/4] Input vs Run1 (normalized)...")
    comp1 = compare_graphs(g_input, g_run1, "input", "run1_normalized")
    comparisons.append(comp1)
    print(f"    Isomórfico: {comp1['isomorphic']}")
    
    # A vs C (input vs canonicalized)
    print("  [2/4] Input vs Run2 (canonicalized)...")
    comp2 = compare_graphs(g_input, g_run2, "input", "run2_canonicalized")
    comparisons.append(comp2)
    print(f"    Isomórfico: {comp2['isomorphic']}")
    
    # A vs D (input vs combined)
    print("  [3/4] Input vs Run3 (combined)...")
    comp3 = compare_graphs(g_input, g_run3, "input", "run3_combined")
    comparisons.append(comp3)
    print(f"    Isomórfico: {comp3['isomorphic']}")
    
    # C vs D (canonicalized vs combined)
    print("  [4/4] Run2 (canonicalized) vs Run3 (combined)...")
    comp4 = compare_graphs(g_run2, g_run3, "run2_canonicalized", "run3_combined")
    comparisons.append(comp4)
    print(f"    Isomórfico: {comp4['isomorphic']}")
    
    # Montar resultado final
    result = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "timezone": "UTC-3",
            "script": "scripts/isomorphism_check.py",
            "rdflib_version": "7.4.0",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        },
        "files": {
            "input": str(input_path),
            "run1_normalized": str(output_run1),
            "run2_canonicalized": str(output_run2),
            "run3_combined": str(output_run3)
        },
        "hashes_sha256": hashes,
        "comparisons": comparisons,
        "summary": {
            "total_comparisons": len(comparisons),
            "all_isomorphic": all(c["isomorphic"] for c in comparisons),
            "canonicalization_preserves_semantics": comp2["isomorphic"],
            "normalization_alters_graph": not comp1["isomorphic"]
        },
        "interpretation": {
            "canonicalization_gate": "PASS" if comp2["isomorphic"] else "FAIL",
            "normalization_gate": "EXPECTED_CHANGE" if not comp1["isomorphic"] else "NO_CHANGE",
            "notes": [
                "Canonização (Run2) DEVE preservar semântica (isomorfismo = True)",
                "Normalização (Run1) PODE alterar grafo (correções URIs/identifiers)",
                "Combined (Run3) reflete ambas operações"
            ]
        },
        "run_manifests": {
            "run1": "outputs/logs/run_manifest_patch-v4_run1_normalize_20260117-203334.json",
            "run2": "outputs/logs/run_manifest_patch-v4_run2_canonicalize_20260117-203742.json",
            "run3": "outputs/logs/run_manifest_patch-v4_run3_canon_normalize_20260117-203822.json"
        }
    }
    
    # Salvar resultado
    output_path = project_root / "outputs" / "logs" / f"isomorphism_check_{timestamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Resultado salvo em: {output_path}")
    print(f"\nResumo:")
    print(f"  Canonização preserva semântica: {result['summary']['canonicalization_preserves_semantics']}")
    print(f"  Normalização altera grafo: {result['summary']['normalization_alters_graph']}")
    print(f"  Gate de canonização: {result['interpretation']['canonicalization_gate']}")
    
    # Exit code baseado no gate de canonização
    if result['interpretation']['canonicalization_gate'] == "FAIL":
        print("\n❌ FALHA: Canonização alterou semântica do grafo!", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n✅ SUCESSO: Semantic Preservation Gate aprovado")
        sys.exit(0)

if __name__ == "__main__":
    main()
