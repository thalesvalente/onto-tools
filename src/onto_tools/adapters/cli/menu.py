"""
Menu Interativo CLI para OntoTools
UC-000: Menu Principal com Navegação TUI
"""
import os
import sys
from pathlib import Path
from typing import Optional, Callable, List, Tuple

import click


def get_project_root() -> Path:
    """
    Detecta o diretório raiz do projeto.
    
    A partir do módulo onto_tools em src/onto_tools/, sobe 2 níveis.
    __file__ = src/onto_tools/adapters/cli/menu.py
    parent = src/onto_tools/adapters/cli/
    parent.parent = src/onto_tools/adapters/
    parent.parent.parent = src/onto_tools/
    parent.parent.parent.parent = src/
    parent.parent.parent.parent.parent = raiz/
    """
    return Path(__file__).parent.parent.parent.parent.parent


class MenuOption:
    """Representa uma opção de menu"""
    
    def __init__(
        self, 
        key: str, 
        label: str, 
        action: Optional[Callable] = None,
        submenu: Optional['InteractiveMenu'] = None,
        disabled: bool = False
    ):
        self.key = key
        self.label = label
        self.action = action
        self.submenu = submenu
        self.disabled = disabled


class InteractiveMenu:
    """Menu interativo com navegação"""
    
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.options: List[MenuOption] = []
        self.parent: Optional['InteractiveMenu'] = None
    
    def add_option(
        self, 
        key: str, 
        label: str, 
        action: Optional[Callable] = None,
        submenu: Optional['InteractiveMenu'] = None,
        disabled: bool = False
    ):
        """Adiciona uma opção ao menu"""
        option = MenuOption(key, label, action, submenu, disabled=disabled)
        if submenu:
            submenu.parent = self
        self.options.append(option)
        return self
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Exibe cabeçalho do menu"""
        click.echo("=" * 80)
        click.echo(f"  🚀 {self.title}")
        click.echo("=" * 80)
        if self.description:
            click.echo(f"\n{self.description}\n")
    
    def display_options(self):
        """Exibe opções do menu"""
        for option in self.options:
            if option.disabled:
                continue
            icon = "📁" if option.submenu else "⚡"
            click.echo(f"  [{option.key}] {icon} {option.label}")
        
        # Opções de navegação
        click.echo()
        if self.parent:
            click.echo("  [V] ⬅️  Voltar ao menu anterior")
        click.echo("  [S] 🚪 Sair")
    
    def get_input(self) -> str:
        """Obtém input do usuário"""
        click.echo()
        return click.prompt("➜ Escolha uma opção", type=str).strip().upper()
    
    def run(self):
        """Executa o menu interativo"""
        while True:
            self.clear_screen()
            self.display_header()
            self.display_options()
            
            choice = self.get_input()
            
            # Opções de navegação global
            if choice == 'S':
                click.echo("\n👋 Saindo... Até logo!")
                sys.exit(0)
            
            if choice == 'V' and self.parent:
                return  # Volta para menu pai
            
            # Procurar opção escolhida
            option = next((opt for opt in self.options if opt.key == choice), None)
            
            if option and not option.disabled:
                if option.submenu:
                    # Navegar para submenu
                    option.submenu.run()
                elif option.action:
                    # Executar ação
                    self.clear_screen()
                    try:
                        option.action()
                    except Exception as e:
                        click.echo(f"\n❌ Erro: {e}", err=True)
                    
                    click.echo("\n")
                    click.pause("Pressione qualquer tecla para continuar...")
            else:
                click.echo(f"\n❌ Opção inválida: {choice}")
                click.pause()


# ============================================================================
# AÇÕES DO MENU (UC-101 a UC-503)
# ============================================================================

# Facade global compartilhado para manter estado entre ações do menu
_menu_facade = None


def _get_or_create_facade():
    """
    Get or create global facade for menu.
    Mantém a mesma instância durante toda a sessão do menu,
    preservando ontologias carregadas e estado.
    """
    global _menu_facade
    
    if _menu_facade is None:
        from onto_tools.application.facade import OntoToolsFacade
        from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
        from onto_tools.adapters.logging.audit_logger import create_audit_logger
        import yaml
        
        project_root = get_project_root()
        config_path = project_root / "config" / "config.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        
        # Resolver log_dir relativo ao project_root
        log_dir_rel = config.get("outputs", {}).get("logs", "outputs/logs")
        log_dir = project_root / log_dir_rel if not Path(log_dir_rel).is_absolute() else Path(log_dir_rel)
        
        _menu_facade = OntoToolsFacade(
            rdf_adapter=RDFlibAdapter(),
            audit_logger=create_audit_logger(log_dir),
            config_path=str(config_path) if config_path.exists() else None
        )
    
    return _menu_facade


def action_ontology_load():
    """UC-101: Carregar Ontologia"""
    import yaml
    
    click.echo("📂 UC-101: Carregar Ontologia TTL\n")
    
    # Carregar config
    project_root = get_project_root()
    config_path = project_root / "config" / "config.yaml"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        click.echo(f"❌ Arquivo config.yaml não encontrado em {config_path}!")
        return
    
    # Obter ontologias configuradas
    ontologies_config = config.get("ontologies", {})
    
    if not ontologies_config:
        click.echo("❌ Nenhuma ontologia configurada em config.yaml!")
        return
    
    # Criar lista de ontologias disponíveis (buscar arquivos .ttl nos diretórios configurados)
    ontologies_list = []
    config_dir = project_root / "config"
    
    for key, onto_data in ontologies_config.items():
        if isinstance(onto_data, dict) and 'path' in onto_data:
            # Resolver caminho do diretório relativo a partir do diretório config
            onto_dir = (config_dir / onto_data['path']).resolve()
            description = onto_data.get('description', 'Sem descrição')
            
            # Verificar se o diretório existe
            if onto_dir.exists() and onto_dir.is_dir():
                # Listar arquivos .ttl no diretório
                ttl_files = sorted(onto_dir.glob("*.ttl"))
                for ttl_file in ttl_files:
                    ontologies_list.append({
                        'key': key,
                        'path': ttl_file,
                        'description': description,
                        'category': key,
                        'exists': True
                    })
            elif onto_dir.exists() and onto_dir.is_file() and onto_dir.suffix == '.ttl':
                # Se for um arquivo direto, usar ele
                ontologies_list.append({
                    'key': key,
                    'path': onto_dir,
                    'description': description,
                    'category': key,
                    'exists': True
                })
            else:
                # Diretório/arquivo não existe
                ontologies_list.append({
                    'key': key,
                    'path': onto_dir,
                    'description': description,
                    'category': key,
                    'exists': False
                })
    
    if not ontologies_list:
        click.echo("❌ Nenhuma ontologia válida encontrada em config.yaml!")
        return
    
    # Ordenar alfabeticamente por nome de arquivo
    ontologies_list.sort(key=lambda x: x['path'].name if x['exists'] else x['key'])
    
    # Exibir ontologias disponíveis
    click.echo("Ontologias disponíveis:\n")
    for i, onto in enumerate(ontologies_list, 1):
        status = "✅" if onto['exists'] else "❌"
        size_info = ""
        if onto['exists']:
            size_mb = onto['path'].stat().st_size / (1024 * 1024)
            size_info = f" ({size_mb:.2f} MB)"
        
        click.echo(f"  {i}. [{onto['category']}] {status} {onto['path'].name if onto['exists'] else onto['key']}{size_info}")
        click.echo(f"     📝 {onto['description']}")
        if not onto['exists']:
            click.echo(f"     ⚠️  Diretório/arquivo não encontrado!")
        click.echo()
    
    # Seleção do usuário
    choice = click.prompt("🔢 Selecione o número da ontologia", type=int)
    
    if choice < 1 or choice > len(ontologies_list):
        click.echo("❌ Seleção inválida!")
        return
    
    selected_onto = ontologies_list[choice - 1]
    
    if not selected_onto['exists']:
        click.echo(f"\n❌ Arquivo não encontrado: {selected_onto['path']}")
        return
    
    selected_file = selected_onto['path']
    validate = click.confirm("\n✅ Deseja validar encoding UTF-8?", default=True)
    
    # Criar facade usando helper
    facade = _get_or_create_facade()
    
    # Carregar ontologia
    click.echo(f"\n🔄 Carregando {selected_file.name}...")
    result = facade.load_ontology(str(selected_file), validate=validate)
    
    # Exibir resultado
    if result["status"] == "success":
        graph = result.get("graph")
        click.echo(f"\n✅ {result['message']}")
        if graph and hasattr(graph, 'metadata'):
            metadata = graph.metadata
            click.echo(f"   📊 Triplas: {metadata.triple_count}")
            click.echo(f"   🔐 Hash: {metadata.hash[:16]}...")
            click.echo(f"   ⏱️  Timestamp: {metadata.timestamp}")
    else:
        click.echo(f"\n❌ {result['message']}")


def action_ontology_reorder():
    """UC-103: Reordenar Ontologia (Canonizar) - Protégé compatible — DEPRECATED"""
    click.echo("🔄 UC-103: Canonizar Ontologia\n")
    click.echo("⚠️  Este menu foi renomeado. Use 'Canonizar' para ordenação determinística.")
    click.echo("   Use 'Normalizar' para correções semânticas.\n")
    
    action_ontology_canonicalize()


def action_ontology_canonicalize():
    """UC-103: Canonizar Ontologia — Ordenação determinística para diff"""
    import yaml
    
    click.echo("🔄 UC-103: Canonizar Ontologia (Ordenação Determinística)\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    # Mostrar informações antes da canonização
    graph = facade._ontology_graph
    click.echo(f"📊 Ontologia atual:")
    click.echo(f"   • Arquivo: {Path(graph.source_path).name if graph.source_path else 'N/A'}")
    click.echo(f"   • Triplas: {graph.metadata.triple_count}")
    click.echo(f"   • Hash atual: {graph.metadata.hash[:16]}...")
    
    click.echo("\n📋 Operações de canonização:")
    click.echo("   ✓ Ordenar prefixos alfabeticamente")
    click.echo("   ✓ Ordenar triplas por (subject, predicate, object)")
    click.echo("   ✓ Usar ordem de predicados do Protégé (rdf:type primeiro)")
    click.echo("   ✓ Vincular namespaces explicitamente (evita ns1/ns2)")
    click.echo("   ✗ NÃO modifica conteúdo semântico")
    
    click.echo("\n🔄 Canonizando ontologia...")
    
    try:
        result = facade.canonicalize_ontology()
        
        if result.get("status") == "success":
            click.echo(f"\n✅ {result.get('message', 'Ontologia canonizada com sucesso!')}")
            
            # Mostrar estatísticas (campos diretos no result)
            click.echo(f"\n📊 Estatísticas:")
            click.echo(f"   • Triplas: {result.get('triple_count', 'N/A')}")
            click.echo(f"   • Prefixos: {result.get('prefix_count', 'N/A')}")
            
            processing_time = result.get("processing_time_ms", 0)
            if processing_time:
                click.echo(f"   • Tempo: {processing_time:.1f}ms")
            
            if result.get("is_idempotent"):
                click.echo(f"   • Idempotência: ✅ (saída estável)")
            
            # Mostrar warnings se houver
            warnings = result.get("warnings", [])
            if warnings:
                click.echo(f"\n⚠️  Avisos ({len(warnings)}):")
                for w in warnings[:5]:
                    msg = w.get('message', str(w))
                    click.echo(f"   • {msg}")
                if len(warnings) > 5:
                    click.echo(f"   ... e mais {len(warnings) - 5} aviso(s)")
            
            # Perguntar se quer salvar com verificação
            click.echo("\n" + "─" * 50)
            save_now = click.confirm(
                "💾 Deseja salvar agora com verificações (isomorphism + idempotency)?",
                default=True
            )
            
            if save_now:
                # Carregar config para pegar o diretório de revisão
                project_root = get_project_root()
                config_path = project_root / "config" / "config.yaml"
                config_dir = project_root / "config"
                
                review_dir = None
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        edogov_config = config.get("ontologies", {}).get("edogov-review", {})
                        if edogov_config and 'path' in edogov_config:
                            review_dir = (config_dir / edogov_config['path']).resolve()
                except:
                    pass
                
                if review_dir is None:
                    review_dir = project_root / "data" / "edo" / "governance" / "review"
                
                # Sugerir nome baseado no arquivo original
                source_name = Path(graph.source_path).stem if graph.source_path else "ontology"
                default_filename = f"{source_name}-canonized.ttl"
                
                filename = click.prompt("Nome do arquivo de saída (.ttl)", default=default_filename, type=str)
                if not filename.endswith('.ttl'):
                    filename = filename + '.ttl'
                
                output_path = review_dir / filename
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                click.echo(f"\n🔄 Salvando com verificações...")
                
                save_result = facade.generate_review_output(
                    output_path=str(output_path),
                    sparql_filters=[],
                    canonized=True,
                    enable_verification=True
                )
                
                if save_result.get("status") == "success":
                    click.echo(f"\n✅ Arquivo canonizado salvo!")
                    
                    # Exibir caminhos dos arquivos gerados
                    ttl_path = save_result.get('ttl_path', 'N/A')
                    manifest_path = save_result.get('manifest_path')
                    
                    click.echo(f"\n📦 Artefatos gerados:")
                    click.echo(f"   📄 Ontologia TTL:  {ttl_path}")
                    if manifest_path:
                        click.echo(f"   📜 Run manifest:   {manifest_path}")
                    
                    # Exibir verificações
                    verifications = save_result.get('verifications', {})
                    if verifications:
                        click.echo(f"\n🔬 Verificações:")
                        iso = verifications.get('isomorphism', {})
                        if iso.get('passed'):
                            click.echo(f"   ✅ Isomorphism: PASS (equivalência semântica preservada)")
                        else:
                            click.echo(f"   ❌ Isomorphism: FAIL")
                            if iso.get('error'):
                                click.echo(f"      Erro: {iso.get('error')}")
                        # Mostrar nota explicativa se presente
                        if iso.get('note'):
                            click.echo(f"      ℹ️  {iso.get('note')}")
                        
                        idemp = verifications.get('idempotency', {})
                        if idemp.get('passed'):
                            click.echo(f"   ✅ Idempotency: PASS (f(f(x)) == f(x))")
                        else:
                            click.echo(f"   ❌ Idempotency: FAIL")
                else:
                    click.echo(f"\n❌ Erro ao salvar: {save_result.get('message')}")
            else:
                click.echo("\n💡 Use UC-104 para gerar arquivo TTL canonizado posteriormente.")
                click.echo("   A saída será igual ao Protégé, ideal para diff/revisão.")
        else:
            click.echo(f"\n❌ Erro: {result.get('message', 'Falha ao canonizar')}")
    except Exception as e:
        click.echo(f"\n❌ Erro ao canonizar: {e}")


def action_ontology_review():
    """UC-104: Gerar Pacote de Revisão"""
    import yaml
    
    click.echo("📦 UC-104: Gerar Pacote de Revisão\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    # Carregar config para pegar o diretório de revisão (edogov-review)
    project_root = get_project_root()
    config_path = project_root / "config" / "config.yaml"
    config_dir = project_root / "config"
    
    review_dir = None
    default_filename = "ontology-review.ttl"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
            # Pegar o diretório de revisão da configuração edogov-review
            edogov_config = config.get("ontologies", {}).get("edogov-review", {})
            if edogov_config and 'path' in edogov_config:
                # Resolver caminho relativo a partir do diretório config
                review_dir = (config_dir / edogov_config['path']).resolve()
    except:
        pass
    
    # Se não encontrou no config, usar padrão
    if review_dir is None:
        review_dir = project_root / "data" / "edo" / "governance" / "review"
    
    filename = click.prompt("Nome do arquivo de saída (.ttl)", default=default_filename, type=str)
    
    # Garantir que o nome tem extensão .ttl
    filename = Path(filename).name  # Pegar só o nome do arquivo, sem diretório
    if not filename.endswith('.ttl'):
        filename = filename + '.ttl'
    
    # Montar caminho completo
    output_path = review_dir / filename
    
    # Garantir que o diretório existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Perguntar sobre formatação
    click.echo("\n📋 Opções de formatação:")
    click.echo("   • Não canonizado: Mantém ordem atual do grafo")
    click.echo("   • Canonizado: Formato Protégé (ordenado, ideal para diff)")
    canonized = click.confirm("Aplicar formatação Protégé (canonizada)?", default=False)
    
    click.echo("\n🔄 Gerando pacote...")
    
    try:
        result = facade.generate_review_output(
            output_path=str(output_path),
            sparql_filters=[],
            canonized=canonized,
            enable_verification=True
        )
        
        if result.get("status") == "success":
            click.echo(f"\n✅ {result.get('message', 'Pacote gerado com sucesso!')}")
            
            # Exibir caminhos dos arquivos gerados
            ttl_path = result.get('ttl_path', 'N/A')
            log_path = result.get('log_path', 'N/A')
            md_path = result.get('md_path')
            manifest_path = result.get('manifest_path')
            
            click.echo(f"\n📦 Artefatos de execução:")
            click.echo(f"   📄 Ontologia TTL:        {ttl_path}")
            click.echo(f"   📋 Log de exportação:    {log_path}")
            if md_path:
                click.echo(f"   📝 Relatório auditoria:  {md_path}")
            if manifest_path:
                click.echo(f"   📜 Run manifest:         {manifest_path}")
            else:
                click.echo(f"   📜 Run manifest:         (not applicable - não canonizado)")
            
            # Exibir verificações se disponíveis
            verifications = result.get('verifications', {})
            if verifications:
                click.echo(f"\n🔬 Verificações:")
                iso = verifications.get('isomorphism', {})
                if iso.get('passed'):
                    click.echo(f"   ✅ Isomorphism: PASS (equivalência semântica preservada)")
                else:
                    click.echo(f"   ❌ Isomorphism: FAIL")
                    if iso.get('error'):
                        click.echo(f"      Erro: {iso.get('error')}")
                # Mostrar nota explicativa se presente
                if iso.get('note'):
                    click.echo(f"      ℹ️  {iso.get('note')}")
                
                idemp = verifications.get('idempotency', {})
                if idemp.get('passed'):
                    click.echo(f"   ✅ Idempotency: PASS (f(f(x)) == f(x))")
                else:
                    click.echo(f"   ❌ Idempotency: FAIL")
            
            # Estatísticas do log
            review_log = result.get('review_log', {})
            if review_log:
                metricas = review_log.get('metricas', {})
                contexto = review_log.get('contexto_execucao', {})
                click.echo(f"\n📊 Estatísticas:")
                click.echo(f"   • Triplas exportadas: {metricas.get('triples_exportadas', 'N/A')}")
                click.echo(f"   • Tempo de execução: {metricas.get('tempo_execucao_segundos', 0):.3f}s")
                click.echo(f"   • Arquivo entrada: {Path(contexto.get('entrada', '')).name}")
                click.echo(f"   • Data: {review_log.get('date', 'N/A')} {review_log.get('hour', 'N/A')}")
        else:
            click.echo(f"\n❌ Erro: {result.get('message', 'Falha ao gerar pacote')}")
    except Exception as e:
        click.echo(f"\n❌ Erro ao gerar pacote: {e}")


def action_ontology_query():
    """UC-105: Consultar Ontologia (linguagem natural via RDFLib)"""
    from rdflib.namespace import RDF, RDFS, OWL
    
    click.echo("🔍 UC-105: Consultar Ontologia\n")
    
    # Criar facade usando helper
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    # Menu de consultas
    click.echo("Tipos de consulta disponíveis:")
    click.echo("  1. Listar Classes")
    click.echo("  2. Listar Propriedades de Objeto")
    click.echo("  3. Listar Propriedades de Dados")
    click.echo("  4. Contar Triplas e Estatísticas")
    click.echo("  5. Listar Namespaces")
    
    choice = click.prompt("\nEscolha o tipo de consulta", type=int)
    
    graph = facade._ontology_graph.graph
    
    if choice == 1:
        # Listar Classes
        click.echo("\n📋 Classes na ontologia (OWL:Class):")
        classes = list(graph.subjects(RDF.type, OWL.Class))
        if classes:
            for i, cls in enumerate(classes[:30], 1):
                # Tentar obter label
                label = next(graph.objects(cls, RDFS.label), None)
                display = f"{cls}"
                if label:
                    display += f" ({label})"
                click.echo(f"  {i}. {display}")
            if len(classes) > 30:
                click.echo(f"\n  ✨ Total: {len(classes)} classes (mostrando primeiras 30)")
        else:
            click.echo("  ❌ Nenhuma classe OWL encontrada")
    
    elif choice == 2:
        # Listar Propriedades de Objeto
        click.echo("\n🔗 Propriedades de Objeto (OWL:ObjectProperty):")
        props = list(graph.subjects(RDF.type, OWL.ObjectProperty))
        if props:
            for i, prop in enumerate(props[:30], 1):
                label = next(graph.objects(prop, RDFS.label), None)
                display = f"{prop}"
                if label:
                    display += f" ({label})"
                click.echo(f"  {i}. {display}")
            if len(props) > 30:
                click.echo(f"\n  ✨ Total: {len(props)} propriedades (mostrando primeiras 30)")
        else:
            click.echo("  ❌ Nenhuma propriedade de objeto encontrada")
    
    elif choice == 3:
        # Listar Propriedades de Dados
        click.echo("\n📊 Propriedades de Dados (OWL:DatatypeProperty):")
        props = list(graph.subjects(RDF.type, OWL.DatatypeProperty))
        if props:
            for i, prop in enumerate(props[:30], 1):
                label = next(graph.objects(prop, RDFS.label), None)
                display = f"{prop}"
                if label:
                    display += f" ({label})"
                click.echo(f"  {i}. {display}")
            if len(props) > 30:
                click.echo(f"\n  ✨ Total: {len(props)} propriedades (mostrando primeiras 30)")
        else:
            click.echo("  ❌ Nenhuma propriedade de dados encontrada")
    
    elif choice == 4:
        # Contar Triplas
        triple_count = len(graph)
        click.echo(f"\n📊 Total de triplas no grafo: {triple_count:,}")
        
        # Estatísticas adicionais
        classes_count = len(list(graph.subjects(RDF.type, OWL.Class)))
        obj_props = len(list(graph.subjects(RDF.type, OWL.ObjectProperty)))
        data_props = len(list(graph.subjects(RDF.type, OWL.DatatypeProperty)))
        
        click.echo(f"   📋 Classes: {classes_count}")
        click.echo(f"   🔗 Object Properties: {obj_props}")
        click.echo(f"   📊 Datatype Properties: {data_props}")
    
    elif choice == 5:
        # Listar Namespaces
        click.echo("\n🏷️  Namespaces/Prefixos definidos:")
        namespaces = list(graph.namespaces())
        for i, (prefix, uri) in enumerate(namespaces, 1):
            click.echo(f"  {i}. {prefix}: {uri}")
        click.echo(f"\n  ✨ Total: {len(namespaces)} namespaces")
    
    else:
        click.echo("❌ Opção inválida!")


def action_ontology_edit():
    """UC-106: Editar Ontologia"""
    click.echo("✏️  UC-106: Editar Ontologia\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    operation = click.prompt(
        "Operação", 
        type=click.Choice(['add', 'remove', 'update']),
        default='add'
    )
    subject = click.prompt("Sujeito (URI ou prefixo)", type=str)
    predicate = click.prompt("Predicado (URI ou prefixo)", type=str)
    obj = click.prompt("Objeto (URI, literal ou prefixo)", type=str)
    
    click.echo(f"\n🔄 Executando {operation}...")
    
    try:
        result = facade.edit_ontology(
            operation=operation,
            subject=subject,
            predicate=predicate,
            obj=obj
        )
        
        if result.get("status") == "success":
            click.echo(f"\n✅ {result.get('message', 'Edição aplicada com sucesso!')}")
        else:
            click.echo(f"\n❌ Erro: {result.get('message', 'Falha na edição')}")
    except Exception as e:
        click.echo(f"\n❌ Erro ao editar: {e}")


def action_ontology_apply():
    """UC-107: Aplicar Lista de Alterações"""
    click.echo("📋 UC-107: Aplicar Lista de Alterações\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    # Listar arquivos update-list disponíveis
    project_root = get_project_root()
    update_dir = project_root / "data" / "examples"
    update_files = list(update_dir.glob("update-list*.json"))
    if update_files:
        click.echo("Arquivos disponíveis:")
        for i, f in enumerate(update_files, 1):
            click.echo(f"  {i}. {f.name}")
    
    default_update_path = str(update_dir / "update-list.json")
    update_list_path = click.prompt(
        "\nCaminho do update-list.json",
        default=default_update_path,
        type=str
    )
    
    if Path(update_list_path).exists():
        click.echo(f"\n🔄 Aplicando alterações de {update_list_path}...")
        
        try:
            result = facade.apply_changes(update_list_path)
            
            if result.get("status") in ["success", "partial"]:
                click.echo(f"\n✅ {result.get('message', 'Alterações aplicadas com sucesso!')}")
                
                # Exibir caminho do log gerado
                if 'log_path' in result:
                    click.echo(f"   📄 Log gerado: {result['log_path']}")
                
                # Exibir estatísticas do apply_log se disponível
                if 'apply_log' in result:
                    metrics = result['apply_log'].get('metrics', {})
                    click.echo(f"   📊 Operações aplicadas: {metrics.get('applied_ops', 0)}/{metrics.get('total_ops', 0)}")
                    if metrics.get('failed_ops', 0) > 0:
                        click.echo(f"   ⚠️  Operações falhas: {metrics['failed_ops']}")
            else:
                click.echo(f"\n❌ Erro: {result.get('message', 'Falha ao aplicar alterações')}")
        except Exception as e:
            click.echo(f"\n❌ Erro ao aplicar: {e}")
    else:
        click.echo(f"❌ Arquivo não encontrado: {update_list_path}")


def action_ontology_normalize():
    """UC-108: Normalizar Ontologia — Correções semânticas"""
    click.echo("🔧 UC-108: Normalizar Ontologia (Correções Semânticas)\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    click.echo("📋 Correções semânticas aplicadas:")
    click.echo("   ✓ Classes OWL: PascalCase (ex: basicDesign → BasicDesign)")
    click.echo("   ✓ Propriedades OWL: lowerCamelCase (ex: HasAttribute → hasAttribute)")
    click.echo("   ✓ skos:prefLabel: Title Case por idioma")
    click.echo("   ✓ skos:definition: Ponto final se ausente")
    click.echo("   ✓ dcterms:identifier: Match com local name")
    click.echo("   ✗ NÃO ordena triplas (use Canonizar para isso)")
    
    # Perguntar sobre auto_fix
    auto_fix = click.confirm("\n🔧 Aplicar correções automáticas?", default=True)
    
    click.echo("\n🔄 Normalizando ontologia...")
    
    try:
        result = facade.normalize_ontology(auto_fix=auto_fix)
        
        if result.get("status") == "success":
            click.echo(f"\n✅ {result.get('message', 'Normalização concluída!')}")
            
            # Mostrar se auto_fix foi aplicado
            if result.get("auto_fix_applied"):
                click.echo("\n📊 Correções aplicadas:")
                
                fix_stats = result.get("fix_stats", {})
                if fix_stats:
                    uri_fixes = len(fix_stats.get("uri_corrections", {}))
                    id_fixes = len(fix_stats.get("identifier_corrections", {}))
                    preflabel_fixes = len(fix_stats.get("preflabel_corrections", {}))
                    def_fixes = len(fix_stats.get("definition_corrections", {}))
                    
                    if uri_fixes:
                        click.echo(f"   • URIs corrigidas: {uri_fixes}")
                    if id_fixes:
                        click.echo(f"   • Identifiers corrigidos: {id_fixes}")
                    if preflabel_fixes:
                        click.echo(f"   • PrefLabels corrigidos: {fix_stats.get('total_preflabel_fixes', preflabel_fixes)}")
                    if def_fixes:
                        click.echo(f"   • Definitions corrigidas: {fix_stats.get('total_definition_fixes', def_fixes)}")
                    
                    total_modified = fix_stats.get("total_triples_modified", 0)
                    if total_modified:
                        click.echo(f"   • Total triplas modificadas: {total_modified}")
            
            # Mostrar warnings de normalização se houver
            warnings = result.get("warnings", [])
            if warnings:
                click.echo(f"\n⚠️  Avisos de normalização ({len(warnings)}):")
                for i, warning in enumerate(warnings[:5], 1):
                    msg = warning.get("issue", warning.get("message", str(warning)))
                    click.echo(f"   {i}. {msg}")
                if len(warnings) > 5:
                    click.echo(f"   ... e mais {len(warnings) - 5} aviso(s)")
            
            # Mostrar quality issues (validações sem correção)
            quality_issues = result.get("quality_issues", [])
            quality_report = result.get("quality_report", {})
            
            if quality_issues:
                errors = [i for i in quality_issues if i.get("severity") == "ERROR"]
                warnings_q = [i for i in quality_issues if i.get("severity") == "WARNING"]
                
                click.echo(f"\n🔍 Validação de Qualidade ({quality_report.get('total_classes_checked', 0)} classes verificadas):")
                
                if errors:
                    click.echo(f"\n   ❌ ERROS que requerem atenção ({len(errors)}):")
                    for issue in errors:
                        subject = issue.get("subject", "").rsplit("#", 1)[-1].rsplit("/", 1)[-1]
                        msg = issue.get("message", "")
                        code = issue.get("code", "")
                        click.echo(f"      • [{code}] {subject}: {msg}")
                
                if warnings_q:
                    click.echo(f"\n   ⚠️  AVISOS para revisão do especialista ({len(warnings_q)}):")
                    for issue in warnings_q:
                        subject = issue.get("subject", "").rsplit("#", 1)[-1].rsplit("/", 1)[-1]
                        msg = issue.get("message", "")
                        code = issue.get("code", "")
                        click.echo(f"      • [{code}] {subject}: {msg}")
                
                click.echo("\n   📝 Nota: Issues de qualidade não são corrigidos automaticamente.")
                click.echo("      Eles requerem decisão do especialista em ontologias.")
            else:
                click.echo(f"\n✅ Validação de qualidade: Nenhum issue encontrado")
            
            click.echo("\n💡 Use UC-103 (Canonizar) para ordenar as triplas")
            click.echo("   Use UC-104 para gerar o arquivo TTL final")
        else:
            click.echo(f"\n❌ Erro: {result.get('message', 'Falha na normalização')}")
    except Exception as e:
        click.echo(f"\n❌ Erro ao normalizar: {e}")


def action_ontology_normalize_and_canonicalize():
    """UC-108 + UC-103: Normalizar E Canonizar — Operação combinada"""
    click.echo("🔧🔄 UC-108 + UC-103: Normalizar e Canonizar Ontologia\n")
    
    # Usar facade global do menu
    facade = _get_or_create_facade()
    
    # Verificar se ontologia está carregada
    if not hasattr(facade, '_ontology_graph') or facade._ontology_graph is None:
        click.echo("❌ Nenhuma ontologia carregada! Execute UC-101 primeiro.")
        return
    
    click.echo("📋 Esta operação combinada:")
    click.echo("   1️⃣  Aplica correções semânticas (UC-108 Normalizar)")
    click.echo("   2️⃣  Ordena de forma determinística (UC-103 Canonizar)")
    click.echo("\n✨ Resultado: Ontologia pronta para commit/diff/revisão")
    
    # Perguntar sobre auto_fix
    auto_fix = click.confirm("\n🔧 Aplicar correções automáticas?", default=True)
    
    click.echo("\n🔄 Normalizando e canonizando ontologia...")
    
    try:
        result = facade.normalize_and_canonicalize(auto_fix=auto_fix)
        
        if result.get("status") == "success":
            click.echo(f"\n✅ {result.get('message', 'Operação concluída!')}")
            
            # Mostrar resultados da normalização
            norm_result = result.get("normalize_result", {})
            if norm_result.get("auto_fix_applied"):
                fix_stats = norm_result.get("fix_stats", {})
                total_modified = fix_stats.get("total_triples_modified", 0)
                if total_modified:
                    click.echo(f"\n📊 Normalização: {total_modified} triplas corrigidas")
            
            # Mostrar resultados da canonização
            canon_result = result.get("canonicalize_result", {})
            if canon_result.get("is_idempotent"):
                click.echo("✅ Canonização: saída idempotente/estável")
            
            click.echo("\n💡 Use UC-104 para gerar o arquivo TTL final")
        else:
            click.echo(f"\n❌ Erro: {result.get('message', 'Falha na operação')}")
    except Exception as e:
        click.echo(f"\n❌ Erro: {e}")


def action_query_execute():
    """UC-201: Executar Consulta SPARQL
    
    Conforme UC-201:
    Pré-condição: Grafo RDF carregado em memória (UC-101)
    
    Fluxo:
    1. Lista categorias disponíveis (via UC-202)
    2. Usuário seleciona categoria
    3. Lista queries da categoria
    4. Usuário seleciona query
    5. Processa parâmetros se houver (UC-203)
    6. Executa e exibe resultados
    """
    click.echo("⚡ UC-201: Executar Consulta SPARQL\n")
    
    try:
        facade = _get_or_create_facade()
        
        # Verificar pré-condição: Ontologia carregada (UC-101)
        if not facade.has_loaded_ontology():
            click.echo("⚠️  Nenhuma ontologia carregada!")
            if click.confirm("💡 Deseja carregar uma ontologia agora?", default=True):
                action_ontology_load()
                # Verificar novamente após carregar
                if not facade.has_loaded_ontology():
                    click.echo("\n❌ Ontologia não foi carregada. Operação cancelada.")
                    return
                click.echo("\n" + "="*60 + "\n")
            else:
                return
        
        # Passo 1: Listar categorias (UC-202)
        cat_result = facade.list_sparql_categories()
        
        if cat_result["status"] != "success":
            click.echo(f"❌ Erro ao listar categorias: {cat_result['message']}")
            return
        
        categories = cat_result["categories"]
        if not categories:
            click.echo("⚠️  Nenhuma categoria encontrada em data/RQ/")
            return
        
        # Exibir categorias
        click.echo("📂 Categorias disponíveis:\n")
        cat_list = list(categories.keys())
        for i, (cat_name, count) in enumerate(categories.items(), 1):
            click.echo(f"  [{i}] {cat_name} ({count})")
        
        # Passo 2: Selecionar categoria
        cat_choice = click.prompt("\n➔ Selecione a categoria", type=int, default=1)
        if cat_choice < 1 or cat_choice > len(cat_list):
            click.echo("❌ Opção inválida")
            return
        
        selected_category = cat_list[cat_choice - 1]
        click.echo(f"\n📁 Categoria: {selected_category}")
        
        # Passo 3: Listar queries da categoria
        queries_result = facade.list_sparql_queries(category=selected_category)
        
        if queries_result["status"] != "success":
            click.echo(f"❌ Erro ao listar queries: {queries_result['message']}")
            return
        
        queries = queries_result["queries"].get(selected_category, [])
        if not queries:
            click.echo(f"⚠️  Nenhuma query encontrada em {selected_category}/")
            return
        
        click.echo("\n📝 Queries disponíveis:\n")
        for i, query_name in enumerate(queries, 1):
            click.echo(f"  [{i}] {query_name}")
        
        # Passo 4: Selecionar query
        query_choice = click.prompt("\n➔ Selecione a query", type=int, default=1)
        if query_choice < 1 or query_choice > len(queries):
            click.echo("❌ Opção inválida")
            return
        
        selected_query = queries[query_choice - 1]
        
        # Passo 4b: Exibir pré-visualização e parâmetros
        info_result = facade.get_sparql_query_info(selected_category, selected_query)
        if info_result["status"] == "success":
            info = info_result["info"]
            click.echo(f"\n🔍 Query: {selected_query}")
            if info.get("has_params"):
                click.echo(f"📋 Parâmetros: {', '.join(info['param_names'])}")
            click.echo(f"📖 Preview:\n{info.get('preview', '')}")
        
        # Passo 5: Processar parâmetros (UC-203)
        params = {}
        if info_result["status"] == "success" and info_result["info"].get("has_params"):
            click.echo("\n⚙️  Informe os parâmetros:")
            for param_name in info_result["info"]["param_names"]:
                value = click.prompt(f"  {param_name}", type=str)
                params[param_name] = value
        
        # Confirmar execução
        if not click.confirm("\n▶️  Executar query?", default=True):
            click.echo("❌ Cancelado")
            return
        
        # Passo 6: Executar query
        timeout = click.prompt("Timeout (segundos)", default=30, type=int)
        click.echo(f"\n🔄 Executando {selected_query} (timeout: {timeout}s)...")
        
        exec_result = facade.execute_sparql_from_file(
            category=selected_category,
            query_name=selected_query,
            params=params if params else None,
            timeout=timeout
        )
        
        if exec_result["status"] == "success":
            results = exec_result.get("results", [])
            row_count = exec_result.get("row_count", len(results))
            
            click.echo(f"\n✅ {row_count} resultados encontrados")
            
            # Exibir preview dos primeiros resultados
            if results:
                click.echo("\n📊 Preview (primeiros 5 resultados):")
                for i, row in enumerate(results[:5], 1):
                    click.echo(f"  {i}. {row}")
                if row_count > 5:
                    click.echo(f"  ... e mais {row_count - 5} resultados")
            
            # Exportação automática baseada na configuração
            from datetime import datetime
            from pathlib import Path
            import json
            import csv
            import yaml
            
            # Carregar configuração
            project_root = get_project_root()
            config_path = project_root / "config" / "config.yaml"
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            except FileNotFoundError:
                config = {}
            
            # Obter formato de exportação da config
            # Formatos suportados: json, xlsx
            export_format = config.get("sparql", {}).get("export_format", "json")
            
            # Obter diretório de saída baseado no formato
            # json -> outputs.json, xlsx -> outputs.xlsx
            outputs_config = config.get("outputs", {})
            if export_format == "json":
                output_dir = outputs_config.get("json", "./outputs/exports/json")
            else:  # xlsx
                output_dir = outputs_config.get("xlsx", "./outputs/exports/xlsx")
            
            # Resolver caminho relativo ao project_root
            output_dir_path = project_root / output_dir if not Path(output_dir).is_absolute() else Path(output_dir)
            
            # Gerar nome do arquivo com timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"query-{selected_query}-{timestamp}.{export_format}"
            output_path = output_dir_path / output_filename
            
            # Garantir que o diretório existe
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            click.echo(f"\n💾 Exportando para {output_path}...")
            
            if export_format == 'json':
                export_data = {
                    "metadata": {
                        "query": selected_query,
                        "category": selected_category,
                        "row_count": row_count,
                        "timestamp": timestamp,
                        "ontology": facade._ontology_graph.source_path if facade._ontology_graph else None
                    },
                    "results": results
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
            else:  # xlsx
                import openpyxl
                from openpyxl import Workbook
                
                wb = Workbook()
                ws = wb.active
                ws.title = selected_query[:31]  # Excel limita nome da sheet a 31 chars
                
                if results:
                    # Cabeçalhos
                    headers = list(results[0].keys()) if isinstance(results[0], dict) else []
                    if headers:
                        ws.append(headers)
                        # Dados
                        for row in results:
                            ws.append([row.get(h, '') for h in headers])
                    else:
                        for row in results:
                            ws.append(row if isinstance(row, (list, tuple)) else [row])
                
                wb.save(output_path)
            
            click.echo(f"✅ Resultados exportados: {output_path}")
        else:
            click.echo(f"\n❌ Erro: {exec_result.get('message', 'Falha na execução')}")
            
    except Exception as e:
        click.echo(f"\n❌ Erro: {e}")


# UC-202 é chamado internamente pelo UC-201, não é uma opção de menu separada


def action_export_json():
    """UC-302/303: Exportar JSON"""
    click.echo("📄 UC-302/303: Exportar JSON\n")
    
    export_type = click.prompt(
        "Tipo de exportação",
        type=click.Choice(['structural', 'hierarchical']),
        default='structural'
    )
    output = click.prompt("Arquivo de saída", default=f"outputs/json/export-{export_type}.json")
    
    click.echo(f"\n🔄 Exportando JSON {export_type}...")
    
    from onto_tools.adapters.cli.commands import export_json_structural, export_json_hierarchical
    from click.testing import CliRunner
    
    runner = CliRunner()
    if export_type == 'structural':
        result = runner.invoke(export_json_structural, [output])
    else:
        result = runner.invoke(export_json_hierarchical, [output])
    
    click.echo(result.output)


def action_export_xlsx():
    """UC-304/305/306: Exportar XLSX"""
    click.echo("📊 UC-304/305/306: Exportar XLSX\n")
    
    export_type = click.prompt(
        "Tipo de exportação",
        type=click.Choice(['catalog', 'comments', 'bsdd']),
        default='catalog'
    )
    output = click.prompt("Arquivo de saída", default=f"outputs/xlsx/{export_type}.xlsx")
    
    click.echo(f"\n🔄 Exportando XLSX {export_type}...")
    
    from onto_tools.adapters.cli.commands import export_xlsx_catalog, export_xlsx_comments, export_xlsx_bsdd
    from click.testing import CliRunner
    
    runner = CliRunner()
    if export_type == 'catalog':
        result = runner.invoke(export_xlsx_catalog, [output])
    elif export_type == 'comments':
        result = runner.invoke(export_xlsx_comments, [output])
    else:
        result = runner.invoke(export_xlsx_bsdd, [output])
    
    click.echo(result.output)


def action_comparison_compare():
    """UC-501: Comparar Artefatos"""
    from onto_tools.adapters.cli.commands import comparison_compare
    from click.testing import CliRunner
    
    click.echo("⚖️  UC-501: Comparar Artefatos\n")
    
    artifact_kind = click.prompt(
        "Tipo de artefato",
        type=click.Choice(['icd', 'mda', 'xls_comments', 'ttl']),
        default='ttl'
    )
    project_root = get_project_root()
    default_config = str(project_root / "config" / "config.yaml")
    config = click.prompt("Arquivo de config", default=default_config, type=str)
    
    click.echo(f"\n🔄 Comparando {artifact_kind.upper()}...")
    runner = CliRunner()
    result = runner.invoke(comparison_compare, [artifact_kind, '--config', config])
    click.echo(result.output)


def action_view_logs():
    """Visualizar logs de auditoria"""
    click.echo("📋 Visualizar Logs de Auditoria\n")
    
    log_dir = Path("outputs/logs")
    if not log_dir.exists():
        click.echo("❌ Diretório de logs não encontrado!")
        return
    
    log_files = list(log_dir.glob("*.json"))
    if not log_files:
        click.echo("❌ Nenhum log encontrado!")
        return
    
    click.echo("Logs disponíveis:")
    for i, log_file in enumerate(log_files, 1):
        size = log_file.stat().st_size / 1024  # KB
        click.echo(f"  {i}. {log_file.name} ({size:.1f} KB)")
    
    choice = click.prompt("\nEscolha um log para visualizar", type=int)
    
    if 1 <= choice <= len(log_files):
        selected_log = log_files[choice - 1]
        click.echo(f"\n📄 {selected_log.name}:\n")
        with open(selected_log, 'r', encoding='utf-8') as f:
            content = f.read()
            click.echo(content)


def action_view_outputs():
    """Visualizar arquivos de saída"""
    click.echo("📁 Visualizar Arquivos de Saída\n")
    
    output_dir = Path("outputs")
    if not output_dir.exists():
        click.echo("❌ Diretório de saída não encontrado!")
        return
    
    # Listar estrutura de diretórios
    for subdir in ['ttl', 'json', 'xlsx', 'logs']:
        full_path = output_dir / subdir
        if full_path.exists():
            files = list(full_path.glob("*"))
            click.echo(f"\n📂 {subdir}/ ({len(files)} arquivos)")
            for f in files[:5]:  # Mostrar primeiros 5
                size = f.stat().st_size / 1024  # KB
                click.echo(f"   - {f.name} ({size:.1f} KB)")
            if len(files) > 5:
                click.echo(f"   ... e mais {len(files) - 5} arquivos")


def action_about():
    """Sobre o OntoTools"""
    click.echo("ℹ️  Sobre o OntoTools\n")
    click.echo("=" * 60)
    click.echo("  ONTO-TOOLS - Sistema de Gerenciamento de Ontologias")
    click.echo("  Versão: 4.0")
    click.echo("  Data: Novembro 2025")
    click.echo("=" * 60)
    click.echo("\n📚 Casos de Uso Implementados:\n")
    click.echo("  • UC-101 a UC-108: Ontology Domain (8 UCs)")
    click.echo("  • UC-201 a UC-203: Query Domain (3 UCs)")
    click.echo("  • UC-301 a UC-306: Export Domain (6 UCs)")
    click.echo("  • UC-401 a UC-403: Data-Input Domain (3 UCs)")
    click.echo("  • UC-501 a UC-503: Comparison Domain (3 UCs)")
    click.echo("\n  Total: 23 Casos de Uso")
    click.echo("\n📊 Cobertura de Testes:\n")
    click.echo("  • UC-Ontology Domain: 100% ✅")
    click.echo("  • Overall Project: 61%")
    click.echo("\n🔗 Documentação: docs/")
    click.echo("🐛 Issues: GitHub Issues")


# ============================================================================
# CONSTRUÇÃO DO MENU
# ============================================================================

def build_menu() -> InteractiveMenu:
    """Constrói a estrutura completa do menu"""
    
    # Menu principal
    main_menu = InteractiveMenu(
        title="ONTO-TOOLS - Menu Principal",
        description="Sistema de Gerenciamento de Ontologias v4.0"
    )
    
    # Submenu: Ontology Domain (UC-101 a UC-108)
    ontology_menu = InteractiveMenu(
        title="Ontology Domain (UC-101 a UC-108)",
        description="Gerenciamento de ontologias TTL"
    )
    ontology_menu.add_option("1", "UC-101: Carregar Ontologia", action_ontology_load)
    ontology_menu.add_option("2", "UC-103: Canonizar Ontologia (Ordenar p/ Diff)", action_ontology_reorder)
    ontology_menu.add_option("3", "UC-104: Gerar Pacote de Revisão", action_ontology_review)
    ontology_menu.add_option("4", "UC-105: Consultar Ontologia SPARQL", action_ontology_query, disabled=True)
    ontology_menu.add_option("5", "UC-106: Editar Ontologia", action_ontology_edit, disabled=True)
    ontology_menu.add_option("6", "UC-107: Aplicar Lista de Alterações", action_ontology_apply, disabled=True)
    ontology_menu.add_option("7", "UC-108: Normalizar Ontologia (Correções)", action_ontology_normalize)
    ontology_menu.add_option("8", "UC-108+103: Normalizar E Canonizar", action_ontology_normalize_and_canonicalize, disabled=True)
    
    # Submenu: Query Domain (UC-201)
    # Nota: UC-202 e UC-203 são chamados internamente pelo UC-201
    query_menu = InteractiveMenu(
        title="Query Domain (UC-201)",
        description="Consultas SPARQL"
    )
    query_menu.add_option("1", "UC-201: Executar Consulta SPARQL", action_query_execute)
    
    # Submenu: Export Domain (UC-301 a UC-306)
    export_menu = InteractiveMenu(
        title="Export Domain (UC-301 a UC-306)",
        description="Exportação para múltiplos formatos"
    )
    export_menu.add_option("1", "UC-302/303: Exportar JSON (Structural/Hierarchical)", action_export_json)
    export_menu.add_option("2", "UC-304/305/306: Exportar XLSX (Catalog/Comments/BSDD)", action_export_xlsx)
    
    # Submenu: Comparison Domain (UC-501 a UC-503)
    comparison_menu = InteractiveMenu(
        title="Comparison Domain (UC-501 a UC-503)",
        description="Comparação de artefatos"
    )
    comparison_menu.add_option("1", "UC-501: Comparar Artefatos", action_comparison_compare)
    
    # Submenu: Utilitários
    utils_menu = InteractiveMenu(
        title="Utilitários",
        description="Ferramentas auxiliares"
    )
    utils_menu.add_option("1", "Visualizar Logs de Auditoria", action_view_logs)
    utils_menu.add_option("2", "Visualizar Arquivos de Saída", action_view_outputs)
    utils_menu.add_option("3", "Sobre o OntoTools", action_about)
    
    # Adicionar submenus ao menu principal
    main_menu.add_option("1", "Ontology Domain (UC-101 a UC-108)", submenu=ontology_menu)
    main_menu.add_option("2", "Query Domain (UC-201 a UC-203)", submenu=query_menu)
    main_menu.add_option("3", "Export Domain (UC-301 a UC-306)", submenu=export_menu)
    main_menu.add_option("4", "Comparison Domain (UC-501 a UC-503)", submenu=comparison_menu)
    main_menu.add_option("9", "Utilitários e Informações", submenu=utils_menu)
    
    return main_menu


# ============================================================================
# ENTRY POINT
# ============================================================================

def start_interactive_menu():
    """Inicia o menu interativo"""
    menu = build_menu()
    # Entrar direto no submenu de Ontology (sem menu de seleção de domínio)
    ontology_option = next(opt for opt in menu.options if opt.key == "1")
    ontology_menu = ontology_option.submenu
    ontology_menu.parent = None  # Remove opção de voltar ao menu de domínios
    ontology_menu.run()


if __name__ == "__main__":
    start_interactive_menu()
