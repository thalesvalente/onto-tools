"""
Formatador de audit log para relatórios markdown legíveis
"""
import json
from pathlib import Path
from collections import Counter
from datetime import datetime


class AuditLogFormatter:
    """Formata audit log JSON em relatório markdown"""
    
    @staticmethod
    def format_to_markdown(log_path: str, output_path: str = None) -> str:
        """
        Formata audit log JSON em relatório markdown legível
        
        Args:
            log_path: Caminho para audit-log-session-*.json
            output_path: Caminho para salvar relatório (default: mesmo diretório com .md)
            
        Returns:
            str: Caminho do arquivo markdown gerado
        """
        # Carregar log
        with open(log_path, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        # Determinar output path
        if not output_path:
            output_path = Path(log_path).with_suffix('.md')
        
        # Processar operações
        ops = log_data.get("ops", [])
        
        # Criar relatório
        report = []
        report.append("# 📋 Relatório de Normalização de Ontologia\n")
        report.append(f"**Arquivo:** `{Path(log_path).name}`\n")
        
        # Sumário Executivo
        report.append("## 📊 Sumário Executivo\n")
        
        for op in ops:
            op_type = op.get("type")
            status = op.get("status")
            applied_at = op.get("applied_at", "unknown")
            
            if op_type == "load_ontology":
                triple_obj = json.loads(op["triple"]["object"])
                file_loaded = triple_obj.get("file", "unknown")
                report.append(f"- **Operação:** Carregamento de Ontologia")
                report.append(f"- **Arquivo:** `{Path(file_loaded).name}`")
                report.append(f"- **Status:** ✅ {status}")
                report.append(f"- **Data/Hora:** {applied_at}\n")
            
            elif op_type == "normalize_ontology":
                triple_obj = json.loads(op["triple"]["object"])
                # Manter warnings como lista para uso posterior no relatório (tabelas de erros)
                quality_issues = triple_obj.get("quality_issues", [])
                warnings = quality_issues if quality_issues else triple_obj.get("warnings", [])
                # Usar detected.warnings_count do novo schema para exibir contagem correta
                detected = triple_obj.get("detected", {})
                if detected:
                    warning_count = detected.get("warnings_count", 0)
                else:
                    warning_count = len(warnings)
                fix_stats = triple_obj.get("fix_stats")
                auto_fix_applied = triple_obj.get("auto_fix_applied", False)
                
                # Extrair erros e total do schema detected
                errors_count = detected.get("errors_count", 0) if detected else 0
                issues_total = detected.get("issues_total", warning_count + errors_count) if detected else (warning_count + errors_count)
                classes_checked = detected.get("total_classes_checked", 0) if detected else 0

                report.append(f"\n- **Operação:** Normalização")
                report.append(f"- **Status:** {'⚠️' if warning_count > 0 else '✅'} {triple_obj.get('status')}")
                report.append(f"- **Modo:** {'🔧 Auto-fix (correções aplicadas)' if auto_fix_applied else '👁️ Validate-only (sem modificações)'}")
                report.append(f"- **Total de Issues:** {issues_total}")
                report.append(f"- **Erros:** {errors_count}")
                report.append(f"- **Total de Avisos:** {warning_count}")
                
                # Adicionar estatísticas de correções se existirem
                if fix_stats:
                    # Buscar valores de fix_stats (onde os valores realmente estão)
                    total_iri_corrections = len(fix_stats.get("uri_corrections", {}))
                    total_identifier_corrections = len(fix_stats.get("identifier_corrections", {}))
                    total_triples_modified = fix_stats.get("total_triples_modified", 0)
                    total_iri_replacements = fix_stats.get("total_uri_replacements", 0)
                    
                    # RF-01: Usar campos corretos baseado no modo
                    # Quando auto_fix=True: usar preflabel_corrections/definition_corrections
                    # Quando auto_fix=False: usar pending_preflabel_corrections/pending_definition_corrections
                    if auto_fix_applied:
                        total_preflabel_fixes = fix_stats.get("total_preflabel_fixes", 0)
                        total_definition_fixes = fix_stats.get("total_definition_fixes", 0)
                        total_preflabel_entities = len(fix_stats.get("preflabel_corrections", {}))
                        total_definition_entities = len(fix_stats.get("definition_corrections", {}))
                    else:
                        # Em validate-only, usar pending_* que contém as correções propostas
                        total_preflabel_fixes = fix_stats.get("total_pending_preflabel_fixes", 0)
                        total_definition_fixes = fix_stats.get("total_pending_definition_fixes", 0)
                        total_preflabel_entities = len(fix_stats.get("pending_preflabel_corrections", {}))
                        total_definition_entities = len(fix_stats.get("pending_definition_corrections", {}))
                    
                    # RF-01: Diferenciar texto entre modo auto_fix e validate_only
                    if auto_fix_applied:
                        report.append(f"- **Correções Aplicadas:**")
                        verb = "corrigidas"
                        verb_plural = "corrigidos"
                        verb_trip = "modificadas"
                    else:
                        report.append(f"- **Correções Propostas (não aplicadas):**")
                        verb = "a corrigir"
                        verb_plural = "a corrigir"
                        verb_trip = "a modificar"
                    
                    report.append(f"  - 🔧 IRIs {verb}: {total_iri_corrections} entidades ({total_iri_replacements} ocorrências/operações)")
                    report.append(f"  - 📝 Identificadores {verb_plural}: {total_identifier_corrections} entidades")
                    report.append(f"  - 🏷️ PrefLabels {verb_plural}: {total_preflabel_fixes} ({total_preflabel_entities} entidades)")
                    report.append(f"  - 📖 Definitions {verb}: {total_definition_fixes} ({total_definition_entities} entidades)")
                    report.append(f"  - 📊 Total de triplas {verb_trip}: {total_triples_modified}")

                    # --- Tabela V do artigo ---
                    mechanical_ops = total_iri_replacements + fix_stats.get("total_identifier_fixes", 0)
                    # Pendentes (validate_only) ou aplicados (auto_fix)
                    pending_preflabel = fix_stats.get("total_pending_preflabel_fixes", 0)
                    pending_definition = fix_stats.get("total_pending_definition_fixes", 0)
                    # Sempre usa pending: "propostas" = detectadas, independente do modo
                    semantic_triples = pending_preflabel + pending_definition
                    applied_mech = triple_obj.get("applied", {}).get("triples_modified", 0)

                    if auto_fix_applied:
                        applied_mech_disabled = "0"
                        applied_mech_enabled  = f"{applied_mech:,}"
                    else:
                        applied_mech_disabled = "0"
                        applied_mech_enabled  = "–"

                    if auto_fix_applied:
                        col_label = "Auto-fix habilitado (mec.)"
                        triples_mod_val = applied_mech_enabled
                    else:
                        col_label = "Auto-fix desabilitado"
                        triples_mod_val = applied_mech_disabled

                    report.append(f"\n### 📋 Tabela V — Métricas de Normalização (Referência Artigo)\n")
                    report.append(f"| Métrica | {col_label} |\n")
                    report.append(f"|---------|----------------------|\n")
                    report.append(f"| Total de issues detectados | {issues_total:,} |\n")
                    report.append(f"| Erros | {errors_count:,} |\n")
                    report.append(f"| Avisos | {warning_count:,} |\n")
                    report.append(f"| Correções mecânicas propostas (IRI + id.) | {mechanical_ops:,} operações |\n")
                    report.append(f"| ↳ IRI: {total_iri_replacements:,} ocorrências ({total_iri_corrections} entidades) + id.: {fix_stats.get('total_identifier_fixes',0):,} | |\n")
                    report.append(f"| Correções semânticas propostas (prefLabel + def.) | {semantic_triples:,} triplas |\n")
                    report.append(f"| Triplas modificadas por correções mecânicas | {triples_mod_val} |\n")
                    report.append(f"| Correções semânticas aplicadas | 0 (bloqueado) |\n")

                report.append(f"- **Data/Hora:** {applied_at}\n")
                
                # Exibir detalhes das correções de IRI se existirem
                if fix_stats and fix_stats.get("uri_corrections"):
                    section_suffix = "Aplicadas" if auto_fix_applied else "Propostas"
                    col_header = "Corrigido" if auto_fix_applied else "Proposto"
                    report.append(f"\n### 🔧 Correções de IRI {section_suffix}\n")
                    report.append(f"\n> **Formato:** Número sequencial, nome original, nome {'corrigido' if auto_fix_applied else 'proposto'}, e quantas vezes a IRI aparece na ontologia\n\n")
                    report.append(f"| # | **Original** | **{col_header}** | **Ocorrências** |\n")
                    report.append("|:-:|--------------|---------------|:---------------:|\n")
                    
                    # Ordenar por nome da IRI antiga
                    sorted_iri_corrections = sorted(
                        fix_stats["uri_corrections"].items(),
                        key=lambda x: (x[0].split("#")[-1] if "#" in x[0] else x[0].split("/")[-1]).lower()
                    )
                    
                    for idx, (old_iri, correction_info) in enumerate(sorted_iri_corrections, 1):
                        old_name = old_iri.split("#")[-1] if "#" in old_iri else old_iri.split("/")[-1]
                        new_iri = correction_info["new_uri"]
                        new_name = new_iri.split("#")[-1] if "#" in new_iri else new_iri.split("/")[-1]
                        occurrences = correction_info["occurrences"]
                        
                        report.append(f"| {idx} | {old_name} | {new_name} | {occurrences} |\n")
                
                # Exibir detalhes das correções de identifier se existirem
                if fix_stats and fix_stats.get("identifier_corrections"):
                    section_suffix = "Aplicadas" if auto_fix_applied else "Propostas"
                    value_label = "corrigido" if auto_fix_applied else "proposto"
                    report.append(f"\n### 📝 Correções de dcterms:identifier {section_suffix}\n")
                    report.append(f"\n> **Total:** {len(fix_stats['identifier_corrections'])} correções\n")
                    report.append(f"\n> **Formato:** Nome da entidade, seguido do valor incorreto (❌) e valor {value_label} (✅)\n\n")
                    
                    # Ordenar por nome da entidade
                    sorted_identifier_corrections = sorted(
                        fix_stats["identifier_corrections"].items(),
                        key=lambda x: (x[0].split("#")[-1] if "#" in x[0] else x[0].split("/")[-1]).lower()
                    )
                    
                    for subject_uri, correction_info in sorted_identifier_corrections:
                        entity_name = subject_uri.split("#")[-1] if "#" in subject_uri else subject_uri.split("/")[-1]
                        old_value = correction_info["old_value"]
                        new_value = correction_info["new_value"]
                        
                        report.append(f"**{entity_name}**\n")
                        report.append(f"- ❌ `{old_value}`\n")
                        report.append(f"- ✅ `{new_value}`\n\n")
                
                # Exibir detalhes das correções de skos:prefLabel se existirem
                # RF-01: Usar pending_* quando auto_fix=False
                if fix_stats:
                    preflabel_data = fix_stats.get("preflabel_corrections", {}) if auto_fix_applied else fix_stats.get("pending_preflabel_corrections", {})
                    if preflabel_data:
                        total_fixes = sum(len(v) for v in preflabel_data.values())
                        section_suffix = "Aplicadas" if auto_fix_applied else "Propostas"
                        value_label = "corrigido" if auto_fix_applied else "proposto"
                        report.append(f"\n### 🏷️ Correções de skos:prefLabel {section_suffix}\n")
                        report.append(f"\n> **Total:** {total_fixes} correções\n")
                        report.append(f"\n> **Formato:** Nome da entidade, seguido do idioma [en/pt-br], valor incorreto (❌) e valor {value_label} (✅)\n\n")
                        
                        # Ordenar por nome da entidade
                        sorted_preflabel_corrections = sorted(
                            preflabel_data.items(),
                            key=lambda x: (x[0].split("#")[-1] if "#" in x[0] else x[0].split("/")[-1]).lower()
                        )
                        
                        for subject_uri, corrections_list in sorted_preflabel_corrections:
                            entity_name = subject_uri.split("#")[-1] if "#" in subject_uri else subject_uri.split("/")[-1]
                            report.append(f"**{entity_name}**\n")
                            # Ordenar correções por idioma
                            sorted_corrections = sorted(corrections_list, key=lambda x: x.get("lang", ""))
                            for correction_info in sorted_corrections:
                                old_value = correction_info["old_value"]
                                new_value = correction_info["new_value"]
                                lang = correction_info.get("lang", "")
                                
                                report.append(f"- [{lang}] ❌ `{old_value}`\n")
                                report.append(f"- [{lang}] ✅ `{new_value}`\n")
                            report.append("\n")
                
                # Exibir detalhes das correções de skos:definition se existirem
                # RF-01: Usar pending_* quando auto_fix=False
                if fix_stats:
                    definition_data = fix_stats.get("definition_corrections", {}) if auto_fix_applied else fix_stats.get("pending_definition_corrections", {})
                    if definition_data:
                        section_suffix = "Aplicadas" if auto_fix_applied else "Propostas"
                        report.append(f"\n### 📖 Correções de skos:definition {section_suffix}\n")
                        report.append("| **Entidade** | **Idioma** | **Correção** |\n")
                        report.append("|--------------|------------|---------------|\n")
                        
                        # Ordenar por nome da entidade
                        sorted_definition_corrections = sorted(
                            definition_data.items(),
                            key=lambda x: (x[0].split("#")[-1] if "#" in x[0] else x[0].split("/")[-1]).lower()
                        )
                        
                        for subject_uri, corrections_list in sorted_definition_corrections:
                            entity_name = subject_uri.split("#")[-1] if "#" in subject_uri else subject_uri.split("/")[-1]
                            # Ordenar correções por idioma
                            sorted_corrections = sorted(corrections_list, key=lambda x: x.get("lang", ""))
                            for correction_info in sorted_corrections:
                                old_value = correction_info["old_value"]
                                new_value = correction_info["new_value"]
                                lang = correction_info.get("lang", "")
                                
                                # Mostrar apenas que ponto foi adicionado (resumido)
                                if new_value.endswith(".") and not old_value.endswith("."):
                                    correction_desc = "Ponto final adicionado"
                                else:
                                    correction_desc = "Texto normalizado"
                                
                                report.append(f"| `{entity_name}` | `{lang}` | {correction_desc} |\n")
                
                # Quality Issues (validações que requerem decisão do especialista)
                quality_issues = triple_obj.get("quality_issues", [])
                if quality_issues:
                    report.append("\n## 🔍 Issues de Qualidade (Requerem Decisão do Especialista)\n")
                    report.append("\n*Estes issues NÃO são corrigidos automaticamente. Requerem análise do especialista em ontologias.*\n")
                    
                    # Separar issues por categoria
                    domain_attr_issues = [i for i in quality_issues if i.get("code", "").startswith("DOMAINATTR_")]
                    ifc_issues = [i for i in quality_issues if i.get("code", "").startswith("IFC_")]
                    general_issues = [i for i in quality_issues 
                                     if not i.get("code", "").startswith("DOMAINATTR_") 
                                     and not i.get("code", "").startswith("IFC_")]
                    
                    # Helper para agrupar issues por (subject, code)
                    def _group_issues_by_entity_code(issues: list) -> dict:
                        """Agrupa issues por (subject, code) para consolidar mensagens."""
                        from collections import defaultdict
                        grouped = defaultdict(list)
                        for issue in issues:
                            subject = issue.get("subject", "").rsplit("#", 1)[-1].rsplit("/", 1)[-1]
                            code = issue.get("code", "UNKNOWN")
                            message = issue.get("message", "")
                            grouped[(subject, code)].append(message)
                        return grouped
                    
                    # Helper para ordenar e formatar issues
                    def _format_issues_table(issues: list, title: str, emoji: str) -> None:
                        if not issues:
                            return
                        
                        errors = sorted(
                            [i for i in issues if i.get("severity") == "ERROR"],
                            key=lambda x: (x.get("subject", "").rsplit("#", 1)[-1].rsplit("/", 1)[-1].lower(), x.get("code", ""))
                        )
                        warnings = sorted(
                            [i for i in issues if i.get("severity") == "WARNING"],
                            key=lambda x: (x.get("subject", "").rsplit("#", 1)[-1].rsplit("/", 1)[-1].lower(), x.get("code", ""))
                        )
                        
                        report.append(f"\n### {emoji} {title}\n")
                        report.append("\n> **Formato de cada item:**\n")
                        report.append("> - **`Nome da Entidade`** — `CÓDIGO_DO_ERRO`\n")
                        report.append(">   - Descrição detalhada do problema encontrado\n")
                        
                        if errors:
                            grouped_errors = _group_issues_by_entity_code(errors)
                            report.append(f"\n#### ❌ Erros Críticos ({len(errors)})\n\n")
                            
                            for (subject, code), messages in sorted(grouped_errors.items(), key=lambda x: (x[0][0].lower(), x[0][1])):
                                report.append(f"- **`{subject}`** — `{code}`\n")
                                for msg in messages:
                                    report.append(f"  - {msg}\n")
                        
                        if warnings:
                            grouped_warnings = _group_issues_by_entity_code(warnings)
                            report.append(f"\n#### ⚠️ Avisos para Revisão ({len(warnings)})\n\n")
                            
                            for (subject, code), messages in sorted(grouped_warnings.items(), key=lambda x: (x[0][0].lower(), x[0][1])):
                                report.append(f"- **`{subject}`** — `{code}`\n")
                                for msg in messages:
                                    report.append(f"  - {msg}\n")
                    
                    # Seção 1: DomainAttribute Issues
                    _format_issues_table(
                        domain_attr_issues, 
                        "Issues de DomainAttribute", 
                        "🏷️"
                    )
                    
                    # Seção 2: IFC Constraints Issues
                    _format_issues_table(
                        ifc_issues,
                        "Issues de Classes IFC",
                        "🏗️"
                    )
                    
                    # Seção 3: General/DomainElement Issues
                    _format_issues_table(
                        general_issues,
                        "Issues Gerais (Classes/Propriedades)",
                        "📋"
                    )
                    
                    # Legenda dos códigos - organizada por categoria
                    report.append("\n#### 📖 Legenda dos Códigos\n")
                    
                    # DomainAttribute codes
                    if domain_attr_issues:
                        report.append("\n**DomainAttribute:**\n")
                        report.append("| **Código** | **Descrição** |\n")
                        report.append("|------------|---------------|\n")
                        report.append("| `DOMAINATTR_ACCESSRIGHTS_MISSING` | DomainAttribute não possui dcterms:accessRights |\n")
                        report.append("| `DOMAINATTR_IDENTIFIER_MISSING` | DomainAttribute não possui dcterms:identifier |\n")
                        report.append("| `DOMAINATTR_IDENTIFIER_MISMATCH` | dcterms:identifier não corresponde ao local name |\n")
                        report.append("| `DOMAINATTR_DEFINITION_MISSING_EN` | Falta skos:definition em inglês (@en) |\n")
                        report.append("| `DOMAINATTR_DEFINITION_MISSING_PT_BR` | Falta skos:definition em português (@pt-br) |\n")
                        report.append("| `DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG` | Múltiplos skos:definition no mesmo idioma |\n")
                        report.append("| `DOMAINATTR_PREFLABEL_MISSING_EN` | Falta skos:prefLabel em inglês (@en) |\n")
                        report.append("| `DOMAINATTR_PREFLABEL_MISSING_PT_BR` | Falta skos:prefLabel em português (@pt-br) |\n")
                        report.append("| `DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG` | Múltiplos skos:prefLabel no mesmo idioma |\n")
                        report.append("| `DOMAINATTR_PROPERTY_MISSING` | Propriedade obrigatória ausente (hasAttributeScope, etc.) |\n")
                    
                    # IFC codes
                    if ifc_issues:
                        report.append("\n**Classes IFC:**\n")
                        report.append("| **Código** | **Descrição** |\n")
                        report.append("|------------|---------------|\n")
                        report.append("| `IFC_REQUIRED_PROPERTY_MISSING` | Classe IFC sem propriedade obrigatória |\n")
                        report.append("| `IFC_BASE_CLASS_MISSING` | Classe IFC não herda da classe base esperada |\n")
                    
                    # General codes
                    if general_issues:
                        report.append("\n**Geral:**\n")
                        report.append("| **Código** | **Descrição** |\n")
                        report.append("|------------|---------------|\n")
                        report.append("| `CLASS_IDENTIFIER_MISSING` | Classe não possui dcterms:identifier |\n")
                        report.append("| `CLASS_IDENTIFIER_MISMATCH` | dcterms:identifier não corresponde ao local name |\n")
                        report.append("| `MULTIPLE_PREFLABEL_SAME_LANG` | Múltiplos skos:prefLabel no mesmo idioma |\n")
                        report.append("| `MULTIPLE_DEFINITION` | Múltiplos skos:definition no mesmo idioma |\n")
                        report.append("| `ALTLABEL_TITLECASE_VIOLATION` | skos:altLabel não segue Title Case |\n")
                        report.append("| `PREFLABEL_FORMAT_INVALID` | skos:prefLabel não corresponde ao padrão esperado |\n")
                        report.append("| `PREFLABEL_NEEDS_CORRECTION` | skos:prefLabel precisa correção (capitalização, acrônimos) |\n")
                        report.append("| `DEFINITION_NEEDS_CORRECTION` | skos:definition precisa correção (ponto final, acrônimos) |\n")
                
                # Estatísticas por tipo de erro
                if warnings:
                    report.append("\n### 📈 Estatísticas de Erros por Categoria\n")
                    
                    # Contar por tipo de erro - suportar ambos os formatos (legado: type/rule, novo: code/severity)
                    error_types = Counter()
                    severity_counts = Counter()
                    rule_counts = Counter()
                    
                    for warning in warnings:
                        # Novo formato: quality_issues com code/severity
                        if "code" in warning:
                            severity = warning.get("severity", "UNKNOWN").lower()
                            code = warning.get("code", "UNKNOWN")
                            severity_counts[severity] += 1
                            rule_counts[code] += 1
                        # Formato legado: type/rule
                        elif warning.get("type") == "naming_convention":
                            severity = warning.get("severity", "unknown")
                            rule = warning.get("rule", "unknown")
                            severity_counts[severity] += 1
                            rule_counts[rule] += 1
                        else:
                            error_types[warning.get("type", "unknown")] += 1
                    
                    # Resumo por severidade
                    if severity_counts:
                        report.append("#### Por Severidade:\n")
                        for severity, count in severity_counts.most_common():
                            emoji = "🔴" if severity in ("error", "ERROR") else "🟡"
                            report.append(f"- {emoji} **{severity.upper()}:** {count} ocorrências\n")
                    
                    # Top 10 regras mais violadas
                    if rule_counts:
                        report.append("\n#### Top 10 Regras/Códigos Mais Violados:\n")
                        for rule, count in rule_counts.most_common(10):
                            report.append(f"- `{rule}`: {count} ocorrências\n")
                    
                    # Outros tipos de erro
                    if error_types:
                        report.append("\n#### Outros Erros:\n")
                        for error_type, count in error_types.items():
                            report.append(f"- `{error_type}`: {count} ocorrências\n")
                    
                    # Detalhamento dos erros
                    report.append("\n---\n\n## 🔍 Detalhamento de Erros\n")
                    
                    # Agrupar por regra/código
                    errors_by_rule = {}
                    for warning in warnings:
                        # Novo formato: code
                        if "code" in warning:
                            rule = warning.get("code", "UNKNOWN")
                        # Formato legado: type/rule
                        elif warning.get("type") == "naming_convention":
                            rule = warning.get("rule", "unknown")
                        else:
                            continue
                        
                        if rule not in errors_by_rule:
                            errors_by_rule[rule] = []
                        errors_by_rule[rule].append(warning)
                    
                    # Imprimir por regra
                    for rule, rule_errors in sorted(errors_by_rule.items()):
                        # Limitar a 20 exemplos por regra
                        sample_size = min(20, len(rule_errors))
                        report.append(f"\n### 📏 Regra: **`{rule}`** ({len(rule_errors)} ocorrências)\n")
                        
                        if len(rule_errors) > sample_size:
                            report.append(f"*Mostrando {sample_size} de {len(rule_errors)} exemplos*\n")
                        
                        for error in rule_errors[:sample_size]:
                            # Novo formato: subject é URI completo
                            subject_raw = error.get("subject", "")
                            subject = subject_raw.split("#")[-1] if "#" in subject_raw else subject_raw.split("/")[-1]
                            
                            # Novo formato: message | Legado: issue
                            issue = error.get("message") or error.get("issue", "")
                            # Novo formato: extra.expected | Legado: expected
                            extra = error.get("extra", {})
                            expected = extra.get("expected") or error.get("expected", "")
                            
                            report.append(f"- **`{subject}`**\n")
                            report.append(f"  - Problema: {issue}\n")
                            if expected:
                                report.append(f"  - Correção: `{expected}`\n")
            
            elif op_type == "generate_review_output":
                triple_obj = json.loads(op["triple"]["object"])
                output_file = triple_obj.get("output", "unknown")
                report.append(f"\n- **Operação:** Geração de Arquivo de Revisão")
                report.append(f"- **Arquivo Gerado:** `{Path(output_file).name}`")
                report.append(f"- **Status:** ✅ {status}")
                report.append(f"- **Data/Hora:** {applied_at}\n")
        
        # Rodapé
        report.append("\n---\n")
        report.append(f"*Relatório gerado automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        # Salvar relatório
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(report)
        
        return str(output_path)


# Função de compatibilidade para código existente
def format_audit_log(log_path: str, output_path: str = None) -> str:
    """Compatibilidade com código existente"""
    return AuditLogFormatter.format_to_markdown(log_path, output_path)
