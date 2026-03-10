"""
CLI Commands - RES-116 Interface Única

ADR-0001: CLI exclusiva com framework click
Structure: ontotools <domain> <command>

Comandos habilitados:
- ontology (3 comandos): UC-101 load, UC-104 review, UC-108 normalize
- verify: hash, isomorphism, idempotency, rc, canonicalize

RNF-116: Progress bars via tqdm
RES-115: Todos os comandos passam pela Façade
"""

import sys
from pathlib import Path
from typing import Optional

import click
import yaml
from tqdm import tqdm

# Adapters (Hexagonal Architecture)
from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.adapters.logging.audit_logger import create_audit_logger

# Application Layer
from onto_tools.application.facade import OntoToolsFacade


# Global config
_config = None
_facade = None


def get_project_root() -> Path:
    """
    Detecta o diretório raiz do projeto.
    
    A partir do módulo onto_tools em src/onto_tools/, sobe 2 níveis.
    __file__ = src/onto_tools/adapters/cli/commands.py
    parent = src/onto_tools/adapters/cli/
    parent.parent = src/onto_tools/adapters/
    parent.parent.parent = src/onto_tools/
    parent.parent.parent.parent = src/
    parent.parent.parent.parent.parent = raiz/
    """
    return Path(__file__).parent.parent.parent.parent.parent


def load_config() -> dict:
    """Load config.yaml from config/ folder in project root."""
    global _config
    if _config is None:
        project_root = get_project_root()
        config_path = project_root / "config" / "config.yaml"
        if not config_path.exists():
            click.echo(f"❌ Erro: config.yaml não encontrado em {config_path}!", err=True)
            sys.exit(1)
        with open(config_path, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f)
    return _config


def get_facade() -> OntoToolsFacade:
    """
    Initialize and return Façade instance.
    
    RES-115: Single orchestration point.
    Dependency Injection (Hexagonal Architecture).
    """
    global _facade
    if _facade is None:
        config = load_config()
        
        # Initialize adapters
        rdf_adapter = RDFlibAdapter()
        
        # Audit logger (BR-09)
        log_dir = Path(config.get("outputs", {}).get("logs", "outputs/logs"))
        audit_logger = create_audit_logger(log_dir)
        
        # Config path
        config_path = Path("config/config.yaml")
        
        # Instantiate Façade
        _facade = OntoToolsFacade(
            rdf_adapter=rdf_adapter,
            audit_logger=audit_logger,
            config_path=str(config_path) if config_path.exists() else None
        )
    
    return _facade


# ============================================================================
# MAIN CLI GROUP
# ============================================================================

@click.group()
@click.version_option(version="3.0.0", prog_name="ontotools")
def cli():
    """
    ONTO-TOOLS - Sistema de Gerenciamento de Ontologias
    
    Domínios habilitados:
    
    - ontology: Gerenciar ontologia TTL (UC-101, UC-104, UC-108)
    - verify: Verificação e reprodutibilidade (RC Protocol)
    
    Use 'ontotools <domínio> --help' para mais informações.
    """
    pass


# ============================================================================
# ONTOLOGY DOMAIN (UC-101 to UC-108)
# ============================================================================

@cli.group()
def ontology():
    """Gerenciar ontologia TTL (UC-101 a UC-108)."""
    pass


@ontology.command("load")
@click.argument("ontology_file", required=False)
@click.option("--validate/--no-validate", default=True, help="Validar ontologia após carregamento")
def ontology_load(ontology_file: str, validate: bool):
    """
    UC-101: Carregar Ontologia TTL
    
    Carrega ontologia do diretório configurado em config.yaml
    
    Args:
        ontology_file: Nome do arquivo TTL (opcional - se não fornecido, exibe menu)
        validate: Validar encoding UTF-8
    """
    facade = get_facade()
    config = load_config()
    
    # Get ontology directory from config
    onto_dir = Path(config["ontologies"]["directory"])
    
    # List available TTL files
    ttl_files = sorted(onto_dir.glob("*.ttl"))
    
    if not ttl_files:
        click.echo(f"❌ Nenhuma ontologia encontrada em {onto_dir}", err=True)
        sys.exit(1)
    
    # Se arquivo foi fornecido, usar diretamente
    if ontology_file:
        selected_file = onto_dir / ontology_file
        if not selected_file.exists():
            click.echo(f"❌ Arquivo não encontrado: {ontology_file}", err=True)
            sys.exit(1)
    else:
        # Display menu (modo interativo)
        click.echo("\n📂 Ontologias disponíveis:\n")
        for idx, ttl_file in enumerate(ttl_files, 1):
            click.echo(f"  {idx}. {ttl_file.name}")
        
        # User selection
        choice = click.prompt("\n🔢 Selecione o número da ontologia", type=int)
        
        if choice < 1 or choice > len(ttl_files):
            click.echo("❌ Seleção inválida!", err=True)
            sys.exit(1)
        
        selected_file = ttl_files[choice - 1]
    
    # Load with progress bar
    with tqdm(total=100, desc="Carregando ontologia", unit="%") as pbar:
        result = facade.load_ontology(str(selected_file), validate=validate)
        pbar.update(100)
    
    # Display result
    if result["status"] == "success":
        click.echo(f"\n✅ {result['message']}")
        click.echo(f"   📊 Triplas: {result.get('triples_count', 0)}")
        click.echo(f"   🔐 SHA-256: {result.get('sha256', 'N/A')}")
        sys.exit(0)
    else:
        click.echo(f"\n❌ {result['message']}", err=True)
        sys.exit(1)



@ontology.command("review")
@click.option("--output", "-o", type=click.Path(), help="Arquivo de saída (.ttl)")
@click.option("--filters", "-f", multiple=True, help="Filtros SPARQL (pode repetir)")
def ontology_review(output: Optional[str], filters: tuple):
    """
    UC-104: Gerar Saída para Revisão
    
    Exporta TTL canônico + export-log.json
    """
    facade = get_facade()
    
    # Usar arquivo padrão se não especificado
    if not output:
        config = load_config()
        output_dir = config["outputs"].get("review", "outputs/review")
        output = f"{output_dir}/ontology-review.ttl"
    
    # Garantir extensão .ttl
    output_path = Path(output)
    if output_path.suffix != '.ttl':
        output_path = output_path.with_suffix('.ttl')
    
    # Criar diretório se não existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tqdm(total=100, desc="Gerando revisão", unit="%") as pbar:
        result = facade.generate_review_output(
            output_path=str(output_path),
            sparql_filters=list(filters) if filters else []
        )
        pbar.update(100)
    
    if result["status"] == "success":
        click.echo(f"\n✅ {result['message']}")
        click.echo(f"   📄 TTL: {result.get('ttl_path', 'N/A')}")
        click.echo(f"   📋 Log: {result.get('log_path', 'N/A')}")
        sys.exit(0)
    else:
        click.echo(f"\n❌ {result['message']}", err=True)
        sys.exit(1)





@ontology.command("normalize")
def ontology_normalize():
    """
    UC-108: Normalizar Ontologia TTL
    
    Aplica regras de normalização (rules.json)
    """
    facade = get_facade()
    
    with tqdm(total=100, desc="Normalizando ontologia", unit="%") as pbar:
        result = facade.normalize_ontology()
        pbar.update(100)
    
    # Exibir warnings se houver
    if result.get("warnings"):
        click.echo()  # Linha em branco
        for warning in result["warnings"]:
            click.echo(f"⚠️  Aviso: {warning['message']}")
    
    # Verificar status (success ou success_with_warnings)
    if result["status"] in ["success", "success_with_warnings"]:
        click.echo(f"\n✅ {result['message']}")
        sys.exit(0)
    else:
        click.echo(f"\n❌ {result['message']}", err=True)
        sys.exit(1)


# ============================================================================
# VERIFICATION DOMAIN (RC Protocol)
# ============================================================================

@cli.group()
def verify():
    """Verificação e reprodutibilidade (RC Protocol)."""
    pass


@verify.command("hash")
@click.argument("file_path", type=click.Path(exists=True))
def verify_hash(file_path: str):
    """
    Compute SHA256 hash of a file.
    
    Example: ontotools verify hash outputs/ontology.ttl
    """
    from onto_tools.application.verification import sha256_file
    
    file_hash = sha256_file(file_path)
    click.echo(f"{file_hash}  {file_path}")


@verify.command("isomorphism")
@click.argument("file_a", type=click.Path(exists=True))
@click.argument("file_b", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output JSON report path")
def verify_isomorphism(file_a: str, file_b: str, output: Optional[str]):
    """
    Compare two RDF files for graph isomorphism.
    
    Example: ontotools verify isomorphism original.ttl canonicalized.ttl
    """
    import json
    from onto_tools.application.verification import compare_isomorphism
    
    with tqdm(total=100, desc="Checking isomorphism", unit="%") as pbar:
        report = compare_isomorphism(file_a, file_b)
        pbar.update(100)
    
    if report.are_isomorphic:
        click.echo(f"\n✅ Graphs are ISOMORPHIC")
        click.echo(f"   📊 Graph A: {report.graph_a_triple_count} triples")
        click.echo(f"   📊 Graph B: {report.graph_b_triple_count} triples")
    else:
        click.echo(f"\n❌ Graphs are NOT isomorphic", err=True)
        click.echo(f"   📊 Graph A: {report.graph_a_triple_count} triples")
        click.echo(f"   📊 Graph B: {report.graph_b_triple_count} triples")
        click.echo(f"   🔴 Only in A: {report.triples_only_in_a}")
        click.echo(f"   🔴 Only in B: {report.triples_only_in_b}")
        if report.error:
            click.echo(f"   ⚠️ Error: {report.error}")
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        click.echo(f"\n   📄 Report: {output}")
    
    sys.exit(0 if report.are_isomorphic else 1)


@verify.command("idempotency")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output JSON report path")
def verify_idempotency(input_file: str, output: Optional[str]):
    """
    Check if canonicalization is idempotent on a file.
    
    Applies canonicalization twice and verifies f(f(x)) == f(x).
    
    Example: ontotools verify idempotency ontology.ttl
    """
    import json
    from rdflib import Graph
    from onto_tools.application.verification import check_idempotency
    from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
    
    def canonical_transform(input_path, output_path):
        """Wrapper for canonicalization."""
        g = Graph()
        g.parse(str(input_path), format='turtle')
        canon_result = canonicalize_graph(g)
        canon_result.graph.serialize(destination=str(output_path), format='turtle')
    
    with tqdm(total=100, desc="Checking idempotency", unit="%") as pbar:
        report = check_idempotency(input_file, canonical_transform)
        pbar.update(100)
    
    if report.is_idempotent:
        click.echo(f"\n✅ Canonicalization is IDEMPOTENT")
        if report.hashes_match:
            click.echo(f"   🔐 Byte-identical: YES")
        else:
            click.echo(f"   🔐 Byte-identical: NO (but semantically equivalent)")
        click.echo(f"   📊 Hash f(x):   {report.first_result_hash[:32]}...")
        click.echo(f"   📊 Hash f(f(x)): {report.second_result_hash[:32]}...")
    else:
        click.echo(f"\n❌ Canonicalization is NOT idempotent", err=True)
        if report.error:
            click.echo(f"   ⚠️ Error: {report.error}")
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        click.echo(f"\n   📄 Report: {output}")
    
    sys.exit(0 if report.is_idempotent else 1)


@verify.command("rc")
@click.option("--coverage-threshold", "-c", type=float, default=90.0, help="Required coverage %")
@click.option("--skip-tests", is_flag=True, help="Skip pytest execution")
@click.option("--skip-rc-v8-check", is_flag=True, help="Skip RC_v8 immutability check")
@click.option("--output-dir", "-o", type=click.Path(), default="outputs/logs", help="Output directory")
def verify_rc(coverage_threshold: float, skip_tests: bool, skip_rc_v8_check: bool, output_dir: str):
    """
    Run full RC (Reproducibility Certification) workflow.
    
    Executes:
    1. pytest with coverage measurement
    2. RC_v8_CANON immutability check
    3. Evidence bundle generation
    
    Example: ontotools verify rc --coverage-threshold 90
    """
    from onto_tools.application.verification.rc_workflow import RCWorkflow
    
    workspace_root = get_project_root()
    rc_v8_path = workspace_root / "outputs" / "logs" / "RC_v8_CANON"
    
    click.echo("\n🔬 RC Workflow v9 - Reproducibility Certification\n")
    click.echo(f"   📂 Workspace: {workspace_root}")
    click.echo(f"   📊 Coverage threshold: {coverage_threshold}%")
    click.echo(f"   🔒 RC_v8 path: {rc_v8_path}")
    click.echo("")
    
    workflow = RCWorkflow(
        workspace_root=workspace_root,
        output_dir=workspace_root / output_dir,
        rc_v8_path=rc_v8_path,
        coverage_threshold=coverage_threshold
    )
    
    with tqdm(total=100, desc="Running RC workflow", unit="%") as pbar:
        result = workflow.run(
            skip_tests=skip_tests,
            skip_rc_v8_check=skip_rc_v8_check
        )
        pbar.update(100)
    
    # Display results
    click.echo("\n" + "=" * 60)
    if result.success:
        click.echo("✅ RC WORKFLOW: PASS")
    else:
        click.echo("❌ RC WORKFLOW: FAIL", err=True)
    click.echo("=" * 60)
    
    click.echo(f"\n   🔒 RC_v8 Immutable:    {'✅' if result.rc_v8_immutable else '❌'}")
    click.echo(f"   📊 Coverage Passed:    {'✅' if result.coverage_passed else '❌'}")
    click.echo(f"   🧪 All Tests Passed:   {'✅' if result.all_tests_passed else '❌'}")
    
    if result.errors:
        click.echo(f"\n   ⚠️ Errors:")
        for err in result.errors:
            click.echo(f"      - {err}")
    
    if result.warnings:
        click.echo(f"\n   ⚡ Warnings:")
        for warn in result.warnings:
            click.echo(f"      - {warn}")
    
    if result.evidence_path:
        click.echo(f"\n   📁 Evidence: {result.evidence_path}")
    
    sys.exit(0 if result.success else 1)


@verify.command("canonicalize")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--verify/--no-verify", default=True, help="Run verification checks")
@click.option("--manifest", "-m", type=click.Path(), help="Output manifest JSON path")
def verify_canonicalize(input_file: str, output_file: str, verify: bool, manifest: Optional[str]):
    """
    Canonicalize an ontology with optional verification.
    
    Produces deterministic, reproducible TTL output with:
    - Sorted triples
    - Normalized blank nodes
    - Consistent formatting
    
    Example: ontotools verify canonicalize input.ttl output.ttl --manifest run.json
    """
    import json
    import time
    from pathlib import Path
    from rdflib import Graph
    from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
    from onto_tools.application.verification import (
        sha256_file,
        compare_isomorphism,
        check_idempotency,
        RunManifest,
        write_manifest_atomic
    )
    
    start_time = time.time()
    
    # Step 1: Canonicalize
    click.echo(f"\n📄 Input:  {input_file}")
    click.echo(f"📄 Output: {output_file}")
    
    with tqdm(total=100, desc="Canonicalizing", unit="%") as pbar:
        # Load graph
        g = Graph()
        g.parse(input_file, format='turtle')
        # Canonicalize
        canon_result = canonicalize_graph(g)
        # Serialize to output
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        canon_result.graph.serialize(destination=str(output_path), format='turtle')
        result = {
            "status": "success",
            "triple_count": canon_result.triple_count,
            "is_idempotent": canon_result.is_idempotent
        }
        pbar.update(100)
    
    if result.get("status") != "success":  # pragma: no cover
        click.echo(f"\n❌ Canonicalization failed: {result.get('message')}", err=True)  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    
    click.echo(f"\n✅ Canonicalization complete")
    click.echo(f"   📊 Triples: {result.get('triple_count', 'N/A')}")
    click.echo(f"   🔐 SHA256:  {sha256_file(output_file)[:32]}...")
    
    # Step 2: Verification (if enabled)
    if verify:
        click.echo("\n🔬 Running verification checks...")
        
        # Isomorphism check
        iso_report = compare_isomorphism(input_file, output_file)
        if iso_report.are_isomorphic:
            click.echo(f"   ✅ Isomorphism: PASS (semantic equivalence preserved)")
        else:
            click.echo(f"   ❌ Isomorphism: FAIL", err=True)
            if iso_report.error:
                click.echo(f"      Error: {iso_report.error}")
        
        # Idempotency check - uses canonicalize_graph properly
        def canonical_transform(inp, out):
            g = Graph()
            g.parse(str(inp), format='turtle')
            canon_result = canonicalize_graph(g)
            canon_result.graph.serialize(destination=str(out), format='turtle')
        
        idemp_report = check_idempotency(input_file, canonical_transform)
        if idemp_report.is_idempotent:
            click.echo(f"   ✅ Idempotency: PASS (f(f(x)) == f(x))")
        else:
            click.echo(f"   ❌ Idempotency: FAIL", err=True)
    
    # Step 3: Generate manifest (if requested)
    if manifest:
        duration = time.time() - start_time
        run_manifest = RunManifest.create(command="canonicalize")
        run_manifest.add_input(input_file)
        run_manifest.add_output(output_file, artifact_type="canonical_ontology")
        run_manifest.set_duration(duration)
        
        if verify:
            run_manifest.add_verification("isomorphism", iso_report.are_isomorphic, {
                "input_triples": iso_report.graph_a_triple_count,
                "output_triples": iso_report.graph_b_triple_count
            })
            run_manifest.add_verification("idempotency", idemp_report.is_idempotent, {
                "hashes_match": idemp_report.hashes_match
            })
        
        write_manifest_atomic(run_manifest, manifest)
        click.echo(f"\n   📄 Manifest: {manifest}")
    
    click.echo("")
    sys.exit(0)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    cli()
