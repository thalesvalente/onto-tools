"""OntoToolsFacade — Ponto único de entrada (RES-115)"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


class OntoToolsFacade:
    """
    RES-115: Façade de orquestração (ponto único)
    
    Orquestra os UCs habilitados através de um único ponto de entrada.
    Injeta adapters via DI, valida RNF-112 (domain não importa adapters).
    
    Mapeamento UC → Método:
    - UC-101: load_ontology()
    - UC-103: canonicalize_ontology()
    - UC-104: generate_review_output()
    - UC-108: normalize_ontology()
    
    Separação de responsabilidades:
    - canonicalize_ontology() (UC-103): Ordenação determinística para diff/revisão
    - normalize_ontology() (UC-108): Correções semânticas (PascalCase, Title Case, etc.)
    """
    
    def __init__(
        self,
        rdf_adapter,
        audit_logger,
        config_path: Optional[str] = None
    ):
        """
        Injeção de dependências (Hexagonal Architecture)
        
        Args:
            rdf_adapter: Adapter para rdflib (OntologyPort)
            audit_logger: Logger de auditoria (BR-09)
            config_path: Caminho para config.yaml (opcional)
        """
        # Adapters (Ports & Adapters)
        self._rdf_adapter = rdf_adapter
        self._audit_logger = audit_logger
        
        # Carregar configuração
        self._config = self._load_config(config_path)
        
        # Domain Services (lazy initialization)
        self._ontology_graph = None
        self._normalizer = None
        
        # Cache
        self._loaded_graphs: dict[str, object] = {}
    
    def _load_config(self, config_path: Optional[str] = None) -> dict:
        """Carregar configuração do config.yaml"""
        import yaml
        
        if config_path is None:
            # Procurar config.yaml na raiz do projeto
            possible_paths = [
                Path("config/config.yaml"),
                Path("../config/config.yaml"),
                Path("../../config/config.yaml"),
            ]
            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    break
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # Configuração padrão se não encontrar o arquivo
        return {
            "outputs": {
                "logs": "./outputs/logs",
                "json": "./outputs/exports/json",
                "xlsx": "./outputs/exports/xlsx",
                "reports": "./outputs/reports"
            }
        }
    
    def has_loaded_ontology(self) -> bool:
        """Verifica se há uma ontologia carregada em memória.
        
        Útil para verificar pré-condições de operações que dependem
        de um grafo RDF carregado (UC-101).
        
        Returns:
            bool: True se há ontologia carregada, False caso contrário.
        """
        return self._ontology_graph is not None
    
    def _generate_audit_report(self) -> Optional[str]:
        """
        Gera relatório markdown a partir do audit log JSON atual.
        
        Chama AuditLogFormatter para converter o JSON em MD legível.
        
        Returns:
            str: Caminho do arquivo MD gerado, ou None se houver erro
        """
        try:
            from onto_tools.adapters.reporting import format_audit_log
            
            # Obter caminho do audit log atual
            audit_json_path = self._audit_logger.get_log_path()
            
            # Gerar path do MD (mesmo nome, extensão .md)
            audit_md_path = audit_json_path.with_suffix('.md')
            
            # Chamar formatador
            format_audit_log(str(audit_json_path), str(audit_md_path))
            
            return str(audit_md_path)
            
        except Exception as e:
            # Não falhar a operação principal se a geração do MD falhar
            print(f"⚠️  Aviso: Não foi possível gerar relatório MD: {e}")
            return None

    
    # ========================================================================
    # DOMAIN: ONTOLOGY (UC-101 a UC-108)
    # ========================================================================
    
    def load_ontology(self, file_path: str, validate: bool = True) -> dict:
        """
        UC-101: Carregar Ontologia TTL
        
        Args:
            file_path: Caminho do arquivo .ttl
            validate: Se True, valida encoding UTF-8
        
        Returns:
            dict: {"status": "success"|"error", "graph": OntologyGraph, "message": str}
        """
        from onto_tools.domain.ontology.graph import OntologyGraph
        from onto_tools.domain.ontology.normalizer import Normalizer
        
        try:
            # Validar encoding se solicitado
            if validate:
                normalizer = Normalizer()
                if not normalizer.validate_encoding(file_path):
                    return {
                        "status": "error",
                        "message": "Encoding inválido (esperado UTF-8)"
                    }
            
            # UC-101: Carregar TTL
            graph = OntologyGraph.load(file_path, self._rdf_adapter)
            
            # Cache para reuso
            self._loaded_graphs[file_path] = graph
            self._ontology_graph = graph
            
            self._audit_logger.log("load_ontology", {"file": file_path, "status": "success"})
            
            return {
                "status": "success",
                "graph": graph,
                "message": f"Ontologia carregada: {Path(file_path).name}"
            }
            
        except Exception as e:
            self._audit_logger.log("load_ontology", {"file": file_path, "status": "error", "error": str(e)})
            return {
                "status": "error",
                "message": f"Erro ao carregar ontologia: {e}"
            }
    
    def canonicalize_ontology(self, graph=None) -> dict:
        """
        UC-103: Canonizar Ontologia TTL
        
        Serializa TTL de forma determinística e compatível com Protégé:
        - Ordena prefixos alfabeticamente
        - Ordena triplas por subject, predicate, object
        - Usa ordem de predicados do Protégé (rdf:type primeiro)
        - Vincula todos os namespaces explicitamente (evita ns1, ns2)
        
        NÃO modifica conteúdo semântico (use normalize_ontology para isso).
        
        Benefício principal: diffs limpos e revisão facilitada.
        
        Args:
            graph: OntologyGraph (usa self._ontology_graph se None)
        
        Returns:
            dict: {
                "status": "success"|"error",
                "message": str,
                "is_idempotent": bool,  # True se saída é estável
                "statistics": dict      # Estatísticas de ordenação
            }
        """
        from onto_tools.domain.ontology.canonicalizer import Canonicalizer
        
        try:
            target_graph = graph or self._ontology_graph
            if target_graph is None:
                return {"status": "error", "message": "Nenhuma ontologia carregada"}
            
            # UC-103: Canonizar
            canonicalizer = Canonicalizer()
            result = canonicalizer.canonicalize(target_graph.graph)
            
            # Atualizar grafo com versão canonizada
            target_graph.graph = result.graph
            
            self._audit_logger.log("canonicalize_ontology", {
                "status": "success",
                "is_idempotent": result.is_idempotent,
                "triple_count": result.triple_count,
                "prefix_count": result.prefix_count,
                "processing_time_ms": result.processing_time_ms
            })
            
            return {
                "status": "success",
                "message": "Ontologia canonizada com sucesso (Protégé-compatible)",
                "is_idempotent": result.is_idempotent,
                "triple_count": result.triple_count,
                "prefix_count": result.prefix_count,
                "processing_time_ms": result.processing_time_ms,
                "warnings": result.warnings
            }
            
        except Exception as e:
            self._audit_logger.log("canonicalize_ontology", {"status": "error", "error": str(e)})
            return {"status": "error", "message": f"Erro ao canonizar: {e}"}
    
    def generate_review_output(
        self,
        output_path: str,
        sparql_filters: list[str] = None,
        graph=None,
        canonized: bool = False,
        enable_verification: bool = True
    ) -> dict:
        """
        UC-104: Gerar Saída para Revisão
        
        Quando canonized=True e enable_verification=True:
        1. Salva snapshot do grafo atual (antes de canonizar) como *_pre-canon.ttl
        2. Canoniza e salva como output final
        3. Verifica isomorfismo entre snapshot e output canonizado
        4. Gera manifest com todos os artefatos e hashes
        
        Isso garante que a verificação de isomorfismo sempre compare o estado atual
        do grafo (independente de edições, normalizações, etc.) com o output final.
        
        Args:
            output_path: Caminho do arquivo de saída .ttl
            sparql_filters: Filtros SPARQL aplicados (opcional)
            graph: OntologyGraph (usa self._ontology_graph se None)
            canonized: Se True, aplica formatação Protégé (ordenada) na saída.
                      Se False (padrão), mantém ordem atual do grafo.
            enable_verification: Se True e canonized=True, executa verificações
                      de isomorphism e idempotency, gerando run_manifest.json.
        
        Returns:
            dict: {
                "status": "success"|"error",
                "review_log": dict,
                "message": str,
                "ttl_path": str,
                "pre_canon_path": str (if canonized with verification),
                "log_path": str,
                "md_path": str,
                "manifest_path": str (if verification enabled),
                "verifications": dict (if verification enabled)
            }
        """
        import json
        import time
        
        try:
            start_time = time.time()
            target_graph = graph or self._ontology_graph
            if target_graph is None:
                return {"status": "error", "message": "Nenhuma ontologia carregada"}
            
            output_path = Path(output_path)
            original_input_path = target_graph.source_path
            
            # Paths for verification artifacts
            pre_canon_path = None
            
            # When canonizing with verification, first save current in-memory graph
            # as a pre-canonization snapshot. This captures ALL changes (normalization,
            # insertions, edits, etc.) that happened since the original was loaded.
            if canonized and enable_verification:
                # Save pre-canonization snapshot (current graph state, not canonized)
                pre_canon_path = output_path.parent / f"{output_path.stem}_pre-canon.ttl"
                target_graph.save(str(pre_canon_path), self._rdf_adapter, canonized=False)
            
            # UC-104: Salvar TTL (com ou sem canonização)
            target_graph.save(str(output_path), self._rdf_adapter, canonized=canonized)
            
            # Gerar export-log.json
            review_log = target_graph.generate_review_log(
                sparql_filters=sparql_filters,
                input_file=original_input_path,
                output_file=str(output_path)
            )
            
            # Salvar log (append mode - adicionar ao arquivo existente)
            log_path = output_path.parent / "export-log.json"
            
            # Carregar logs existentes se o arquivo já existe
            existing_logs = []
            if log_path.exists():
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        # Se for uma lista, usar diretamente; se for dict, colocar em lista
                        existing_logs = content if isinstance(content, list) else [content]
                except:
                    existing_logs = []
            
            # Adicionar novo log
            existing_logs.append(review_log)
            
            # Salvar todos os logs
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(existing_logs, f, indent=2, ensure_ascii=False)
            
            # Verification and Manifest generation (when canonized)
            manifest_path = None
            verifications = {}
            
            if canonized and enable_verification and pre_canon_path:
                from onto_tools.application.verification import (
                    sha256_file,
                    compare_isomorphism,
                    check_full_idempotency,
                    RunManifest,
                    write_manifest_append
                )
                from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
                from rdflib import Graph
                
                # Compute hashes for all artifacts
                original_hash = sha256_file(original_input_path) if original_input_path else None
                pre_canon_hash = sha256_file(pre_canon_path)
                output_hash = sha256_file(output_path)
                
                # Isomorphism check: compare current in-memory graph with canonized output
                # This verifies that canonization preserved semantic equivalence.
                # We use the in-memory graph directly (not pre_canon file) to avoid
                # any serialization differences (comments, order, etc.)
                output_graph = Graph()
                output_graph.parse(str(output_path), format='turtle')
                
                iso_passed = target_graph.graph.isomorphic(output_graph)
                
                # Check if graph was semantically modified from original
                # We must use isomorphism (not hash) because:
                # - Comments in original file are not loaded into RDF graph
                # - Serialization order may differ
                # - Hash comparison would always show "modified" falsely
                graph_modified_from_original = False
                if original_input_path:
                    original_graph = Graph()
                    original_graph.parse(original_input_path, format='turtle')
                    graph_modified_from_original = not target_graph.graph.isomorphic(original_graph)
                
                verifications["isomorphism"] = {
                    "passed": iso_passed,
                    "pre_canon_path": str(pre_canon_path),
                    "pre_canon_hash": pre_canon_hash,
                    "output_path": str(output_path),
                    "output_hash": output_hash,
                    "input_triples": len(target_graph.graph),
                    "output_triples": len(output_graph),
                    "error": None,
                    "graph_modified_from_original": graph_modified_from_original,
                }
                
                # Add note only if graph was actually semantically modified
                if graph_modified_from_original:
                    verifications["isomorphism"]["note"] = (
                        "O grafo foi modificado desde o carregamento original. "
                        "A verificação de isomorfismo compara o estado atual do grafo "
                        "(pré-canonização) com o output canonizado, confirmando que "
                        "a canonização preservou a equivalência semântica."
                    )
                    verifications["isomorphism"]["original_hash"] = original_hash
                    verifications["isomorphism"]["original_path"] = original_input_path
                
                # Full idempotency check (stability + consistency)
                # Verifies: saved_hash == f(saved) AND f(f(saved)) == f(saved)
                from onto_tools.adapters.rdf.protege_serializer import serialize_protege_style
                def canonical_transform(inp, out):
                    g = Graph()
                    g.parse(str(inp), format='turtle')
                    canon_result = canonicalize_graph(g)
                    # Use same serializer as save_ttl(canonized=True)
                    serialized = serialize_protege_style(canon_result.graph)
                    Path(out).write_bytes(serialized.encode("utf-8"))
                
                idemp_report = check_full_idempotency(str(output_path), canonical_transform)
                verifications["idempotency"] = {
                    "passed": idemp_report.is_idempotent and idemp_report.is_fully_consistent,
                    "is_idempotent": idemp_report.is_idempotent,
                    "is_fully_consistent": idemp_report.is_fully_consistent,
                    "saved_matches_first": idemp_report.saved_matches_first,
                    "hashes_match": idemp_report.hashes_match,
                    "first_result_hash": idemp_report.first_result_hash,
                    "second_result_hash": idemp_report.second_result_hash
                }
                
                # Create and write manifest with all artifacts
                duration = time.time() - start_time
                run_manifest = RunManifest.create(command="generate_review_output")
                
                # Input: original file that was loaded
                if original_input_path:
                    run_manifest.add_input(original_input_path)
                
                # Outputs: pre-canon snapshot + canonized
                run_manifest.add_output(str(pre_canon_path), artifact_type="pre_canon_snapshot")
                run_manifest.add_output(str(output_path), artifact_type="canonical_ontology")
                
                run_manifest.set_duration(duration)
                
                # Add artifact hashes to verification details
                verifications["isomorphism"]["artifacts"] = {
                    "original": {
                        "path": original_input_path,
                        "sha256": original_hash
                    } if original_input_path else None,
                    "pre_canon_snapshot": {
                        "path": str(pre_canon_path),
                        "sha256": pre_canon_hash,
                        "description": "Estado do grafo antes da canonização"
                    },
                    "canonical_output": {
                        "path": str(output_path),
                        "sha256": output_hash,
                        "description": "Ontologia canonizada (formato Protégé)"
                    }
                }
                
                run_manifest.add_verification(
                    "isomorphism",
                    iso_passed,
                    verifications["isomorphism"]
                )
                run_manifest.add_verification(
                    "idempotency",
                    idemp_report.is_idempotent and idemp_report.is_fully_consistent,
                    verifications["idempotency"]
                )
                
                manifest_path = output_path.parent / "run_manifest.json"
                write_manifest_append(run_manifest, manifest_path)
            
            self._audit_logger.log("generate_review_output", {
                "output": str(output_path),
                "pre_canon_path": str(pre_canon_path) if pre_canon_path else None,
                "status": "success",
                "canonized": canonized,
                "verification_enabled": enable_verification and canonized,
                "manifest_generated": manifest_path is not None
            })
            
            # Auto-generate markdown report from audit log
            md_path = self._generate_audit_report()
            
            result = {
                "status": "success",
                "review_log": review_log,
                "ttl_path": str(output_path),
                "log_path": str(log_path),
                "md_path": md_path,
                "message": f"Saída gerada: {output_path.name}"
            }
            
            # Add pre-canon path if verification was enabled
            if pre_canon_path:
                result["pre_canon_path"] = str(pre_canon_path)
            
            if manifest_path:
                result["manifest_path"] = str(manifest_path)
                result["verifications"] = verifications
            
            return result
            
        except Exception as e:
            self._audit_logger.log("generate_review_output", {"status": "error", "error": str(e)})
            return {"status": "error", "message": f"Erro ao gerar saída: {e}"}
    
    def normalize_ontology(self, graph=None, auto_fix: bool = None) -> dict:
        """
        UC-108: Normalizar Ontologia TTL (Correções Semânticas)
        
        Aplica correções semânticas de nomenclatura:
        - Classes OWL: PascalCase
        - Propriedades OWL: lowerCamelCase
        - skos:prefLabel: Title Case por idioma
        - skos:definition: Ponto final
        - dcterms:identifier: Match com local name
        
        NÃO ordena triplas (use canonicalize_ontology para isso).
        
        Args:
            graph: OntologyGraph (usa self._ontology_graph se None)
            auto_fix: Forçar auto_fix (None = usar valor de rules.json)
        
        Returns:
            dict: {
                "status": "success"|"error",
                "message": str,
                "warnings": list[dict],   # Avisos de validação
                "fix_stats": dict | None, # Estatísticas de correções
                "auto_fix_applied": bool  # Se correções foram aplicadas
            }
        """
        from onto_tools.domain.ontology.normalizer import Normalizer
        from onto_tools.domain.ontology.quality_validator import OntologyQualityValidator
        
        try:
            target_graph = graph or self._ontology_graph
            if target_graph is None:
                return {"status": "error", "message": "Nenhuma ontologia carregada"}
            
            normalizer = Normalizer(auto_fix=auto_fix)
            
            # UC-108: Normalizar (correções semânticas apenas)
            result = normalizer.normalize(target_graph.graph)
            
            # RF-01: Só atualizar o grafo se correções foram efetivamente aplicadas
            # Quando auto_fix=False (validate_only), o grafo original permanece intacto
            if result.auto_fix_applied:
                target_graph.graph = result.graph
            
            # Executar validação de qualidade (apenas warnings, não modifica)
            quality_validator = OntologyQualityValidator()
            quality_report = quality_validator.validate(target_graph.graph)
            
            # Combinar warnings de normalização com issues de qualidade
            all_warnings = list(result.warnings)  # Copy para não modificar original
            quality_issues = [issue.to_dict() for issue in quality_report.issues]
            
            # Adicionar warnings para correções pendentes de prefLabels (quando auto_fix=false)
            # Agrupa todas as correções por entidade para mostrar lista completa de problemas
            if result.fix_stats and result.fix_stats.get("pending_preflabel_corrections"):
                for subject_uri, corrections_list in result.fix_stats["pending_preflabel_corrections"].items():
                    # Criar uma mensagem consolidada por entidade com todos os idiomas
                    details = []
                    for correction in sorted(corrections_list, key=lambda x: x.get("lang", "")):
                        lang = correction.get("lang", "")
                        old_value = correction.get("old_value", "")
                        new_value = correction.get("new_value", "")
                        
                        # Detectar o tipo de correção (causa)
                        causas = []
                        
                        if old_value != new_value:
                            import re
                            # Acrônimos no novo valor (UPPERCASE com letras/números, ex: CO2, H2S, API)
                            new_acronyms = set(re.findall(r'\b[A-Z][A-Z0-9]+\b', new_value))
                            
                            # Se o conteúdo é igual ignorando case, é problema de capitalização
                            if old_value.lower() == new_value.lower():
                                # Encontrar quais acrônimos estavam em minúsculo
                                acronyms_fixed = []
                                for acr in new_acronyms:
                                    if acr.lower() in old_value.lower() and acr not in old_value:
                                        acronyms_fixed.append(acr)
                                
                                if acronyms_fixed:
                                    causas.append(f"acrônimos: {', '.join(sorted(acronyms_fixed))}")
                                
                                # Verificar Title Case - palavras que deveriam estar capitalizadas
                                old_words = old_value.split()
                                new_words = new_value.split()
                                wrong_caps = []
                                for ow, nw in zip(old_words, new_words):
                                    if ow != nw and ow.lower() == nw.lower():
                                        wrong_caps.append(f"'{ow}'→'{nw}'")
                                if wrong_caps and not acronyms_fixed:
                                    # Mostrar até 3 exemplos
                                    causas.append(f"Title Case: {', '.join(wrong_caps[:3])}")
                            else:
                                # Conteúdo diferente mesmo ignorando case
                                causas.append("formatação de texto")
                        
                        causa_str = "; ".join(causas) if causas else "formatação"
                        details.append(f"[{lang}] {causa_str}")
                    
                    if details:
                        quality_issues.append({
                            "code": "PREFLABEL_NEEDS_CORRECTION",
                            "subject": subject_uri,
                            "severity": "WARNING",
                            "message": f"skos:prefLabel precisa correção. Causa: {'; '.join(details)}"
                        })
            
            # Adicionar warnings para correções pendentes de definitions (quando auto_fix=false)
            # Agrupa todas as correções por entidade para mostrar lista completa de problemas
            if result.fix_stats and result.fix_stats.get("pending_definition_corrections"):
                for subject_uri, corrections_list in result.fix_stats["pending_definition_corrections"].items():
                    # Criar uma mensagem consolidada por entidade com todos os idiomas
                    details = []
                    for correction in sorted(corrections_list, key=lambda x: x.get("lang", "")):
                        lang = correction.get("lang", "")
                        old_value = correction.get("old_value", "")
                        new_value = correction.get("new_value", "")
                        
                        # Detectar o tipo de correção (causa)
                        causas = []
                        
                        # 1. Ponto final
                        if not old_value.rstrip().endswith(('.', '!', '?')) and new_value.rstrip().endswith(('.', '!', '?')):
                            causas.append("falta ponto final")
                        
                        # 2. Whitespace (trim)
                        if old_value != old_value.strip():
                            causas.append("whitespace extra")
                        
                        # 3. Comparar conteúdo para outras diferenças
                        old_content = old_value.strip().rstrip('.!?')
                        new_content = new_value.strip().rstrip('.!?')
                        
                        if old_content != new_content:
                            import re
                            # Acrônimos no novo valor (UPPERCASE com letras/números, ex: CO2, H2S, API)
                            new_acronyms = set(re.findall(r'\b[A-Z][A-Z0-9]+\b', new_content))
                            
                            # Se o conteúdo é igual ignorando case, é problema de capitalização/acrônimos
                            if old_content.lower() == new_content.lower():
                                if new_acronyms:
                                    # Encontrar quais acrônimos estavam em minúsculo
                                    acronyms_fixed = []
                                    for acr in new_acronyms:
                                        if acr.lower() in old_content.lower() and acr not in old_content:
                                            acronyms_fixed.append(acr)
                                    if acronyms_fixed:
                                        causas.append(f"acrônimos em minúsculo: {', '.join(sorted(acronyms_fixed))}")
                                    else:
                                        causas.append("capitalização incorreta")
                                else:
                                    causas.append("capitalização incorreta")
                            else:
                                # Conteúdo diferente mesmo ignorando case
                                causas.append("texto alterado")
                        
                        causa_str = "; ".join(causas) if causas else "formatação"
                        details.append(f"[{lang}] {causa_str}")
                    
                    if details:
                        quality_issues.append({
                            "code": "DEFINITION_NEEDS_CORRECTION",
                            "subject": subject_uri,
                            "severity": "WARNING",
                            "message": f"skos:definition precisa correção. Causa: {'; '.join(details)}"
                        })
            
            # Preparar detalhes para audit log - RF-03: Schema estável
            pending_preflabel_count = len(result.fix_stats.get("pending_preflabel_corrections", {})) if result.fix_stats else 0
            pending_definition_count = len(result.fix_stats.get("pending_definition_corrections", {})) if result.fix_stats else 0
            
            # T5: Calcular rulebook snapshot para rastreabilidade
            import hashlib
            rulebook_snapshot = {
                "path": str(normalizer.rules_path),
                "sha256": None,
                "version": None
            }
            try:
                with open(normalizer.rules_path, "rb") as rb_file:
                    rulebook_snapshot["sha256"] = hashlib.sha256(rb_file.read()).hexdigest()
                # Tentar extrair versão do rules.json se existir
                if normalizer.rules.get("version"):
                    rulebook_snapshot["version"] = normalizer.rules.get("version")
                elif normalizer.rules.get("metadata", {}).get("version"):
                    rulebook_snapshot["version"] = normalizer.rules.get("metadata", {}).get("version")
            except Exception:
                pass  # Manter sha256 como None se falhar
            
            # RF-03: Estrutura de audit-log com separação detect/propose/apply
            log_details = {
                "status": "success",
                # Modo de operação (validate_only ou auto_fix)
                "mode": result.fix_stats.get("mode", "validate_only") if result.fix_stats else "validate_only",
                "auto_fix_applied": result.auto_fix_applied,
                # T5: Rulebook snapshot para auditoria
                "rulebook": rulebook_snapshot,
                
                # Seção: DETECTED (issues identificadas)
                "detected": {
                    "issues_total": quality_report.total_issues + len(result.warnings),
                    "errors_count": len(quality_report.get_errors()),
                    "warnings_count": len(quality_report.get_warnings()) + len(result.warnings),
                    "total_classes_checked": quality_report.total_classes_checked,
                },
                
                # Seção: PROPOSED (correções propostas - sempre presente)
                "proposed": {
                    "corrections_total": (
                        (result.fix_stats.get("total_pending_preflabel_fixes", 0) if result.fix_stats else 0) +
                        (result.fix_stats.get("total_pending_definition_fixes", 0) if result.fix_stats else 0) +
                        (result.fix_stats.get("total_preflabel_fixes", 0) if result.fix_stats else 0) +
                        (result.fix_stats.get("total_definition_fixes", 0) if result.fix_stats else 0)
                    ),
                    "preflabel_count": (
                        pending_preflabel_count + 
                        len(result.fix_stats.get("preflabel_corrections", {})) if result.fix_stats else 0
                    ),
                    "definition_count": (
                        pending_definition_count +
                        len(result.fix_stats.get("definition_corrections", {})) if result.fix_stats else 0
                    ),
                    "iri_count": len(result.fix_stats.get("uri_corrections", {})) if result.fix_stats else 0,
                    "identifier_count": len(result.fix_stats.get("identifier_corrections", {})) if result.fix_stats else 0,
                },
                
                # Seção: APPLIED (correções aplicadas - 0 em validate_only)
                "applied": {
                    "corrections_total": result.fix_stats.get("total_triples_modified", 0) if (result.fix_stats and result.auto_fix_applied) else 0,
                    "triples_modified": result.fix_stats.get("total_triples_modified", 0) if (result.fix_stats and result.auto_fix_applied) else 0,
                    "preflabel_fixes": result.fix_stats.get("total_preflabel_fixes", 0) if result.fix_stats else 0,
                    "definition_fixes": result.fix_stats.get("total_definition_fixes", 0) if result.fix_stats else 0,
                    "iri_replacements": result.fix_stats.get("total_uri_replacements", 0) if (result.fix_stats and result.auto_fix_applied) else 0,
                    "identifier_fixes": result.fix_stats.get("total_identifier_fixes", 0) if (result.fix_stats and result.auto_fix_applied) else 0,
                },
            }
            
            # Adicionar estatísticas detalhadas de correções se existirem
            if result.fix_stats:
                log_details["fix_stats"] = result.fix_stats
            
            # Adicionar quality issues ao log
            if quality_issues:
                log_details["quality_issues"] = quality_issues
            
            # Registrar no audit log
            self._audit_logger.log("normalize_ontology", log_details)
            
            return {
                "status": "success",
                "message": "Ontologia normalizada com sucesso (correções semânticas)",
                "warnings": all_warnings,
                "fix_stats": result.fix_stats,
                "auto_fix_applied": result.auto_fix_applied,
                "quality_report": quality_report.to_dict(),
                "quality_issues": quality_issues
            }
            
        except Exception as e:
            self._audit_logger.log("normalize_ontology", {"status": "error", "error": str(e)})
            return {"status": "error", "message": f"Erro ao normalizar: {e}"}
    
