"""Testes para audit_formatter.py — Formatação de audit logs (UC-110)"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestAuditLogFormatter:
    """Testes para AuditLogFormatter."""
    
    @pytest.fixture
    def sample_audit_log(self):
        """Cria arquivo de audit log temporário."""
        log_data = {
            "session_id": "test-session-123",
            "started_at": "2024-01-15T10:00:00",
            "ops": [
                {
                    "type": "load_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:00:01",
                    "triple": {
                        "subject": "edo:load",
                        "predicate": "edo:result",
                        "object": json.dumps({
                            "file": "/path/to/ontology.ttl",
                            "status": "success"
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            return f.name
    
    @pytest.fixture
    def normalize_audit_log(self):
        """Audit log com operação de normalização."""
        log_data = {
            "session_id": "normalize-session",
            "ops": [
                {
                    "type": "normalize_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:05:00",
                    "triple": {
                        "subject": "edo:normalize",
                        "predicate": "edo:result",
                        "object": json.dumps({
                            "status": "completed",
                            "auto_fix_applied": True,  # Modo auto_fix ativado
                            "warning_count": 2,
                            "warnings": [
                                {"type": "naming_convention", "severity": "error", "rule": "PascalCase", "subject": "http://example.org#myClass", "issue": "'myClass' should be PascalCase", "expected": "MyClass"},
                                {"type": "naming_convention", "severity": "warning", "rule": "camelCase", "subject": "http://example.org#MyProp", "issue": "'MyProp' should be camelCase", "expected": "myProp"}
                            ],
                            "fix_stats": {
                                "uri_corrections": {
                                    "http://example.org#wrongName": {
                                        "new_uri": "http://example.org#CorrectName",
                                        "occurrences": 5
                                    }
                                },
                                "identifier_corrections": {
                                    "http://example.org#Entity": {
                                        "old_value": "entity",
                                        "new_value": "Entity"
                                    }
                                },
                                "preflabel_corrections": {
                                    "http://example.org#Test": [
                                        {"old_value": "test", "new_value": "Test", "lang": "en"}
                                    ]
                                },
                                "definition_corrections": {
                                    "http://example.org#Item": [
                                        {"old_value": "An item", "new_value": "An item.", "lang": "en"}
                                    ]
                                }
                            },
                            "total_uri_corrections": 1,
                            "total_identifier_corrections": 1,
                            "total_preflabel_corrections": 1,
                            "total_definition_corrections": 1,
                            "total_triples_modified": 10,
                            "total_uri_replacements": 5,
                            "total_preflabel_fixes": 1,
                            "total_definition_fixes": 1
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            return f.name
    
    def test_format_to_markdown_creates_file(self, sample_audit_log):
        """Cria arquivo markdown."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(sample_audit_log)
        
        assert Path(result).exists()
        assert result.endswith('.md')
    
    def test_format_to_markdown_custom_output_path(self, sample_audit_log):
        """Usa output_path customizado."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as f:
            output_path = f.name
        
        result = AuditLogFormatter.format_to_markdown(sample_audit_log, output_path)
        
        assert result == output_path
        assert Path(result).exists()
    
    def test_format_to_markdown_contains_header(self, sample_audit_log):
        """Relatório contém header."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(sample_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "# 📋 Relatório de Normalização" in content
    
    def test_format_to_markdown_contains_load_info(self, sample_audit_log):
        """Relatório contém informações de load."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(sample_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Carregamento de Ontologia" in content
        assert "ontology.ttl" in content
    
    def test_format_normalize_includes_warnings(self, normalize_audit_log):
        """Relatório de normalização inclui warnings."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Normalização" in content
        assert "Total de Avisos" in content
        assert "⚠️" in content or "✅" in content
    
    def test_format_normalize_includes_fix_stats(self, normalize_audit_log):
        """Relatório inclui estatísticas de correções."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Correções Aplicadas" in content
        assert "IRIs corrigidas" in content
    
    def test_format_normalize_includes_iri_corrections_table(self, normalize_audit_log):
        """Relatório inclui tabela de correções de IRI."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Correções de IRI Aplicadas" in content
        assert "wrongName" in content
        assert "CorrectName" in content
    
    def test_format_normalize_includes_identifier_corrections(self, normalize_audit_log):
        """Relatório inclui correções de identifier."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "dcterms:identifier" in content
    
    def test_format_normalize_includes_preflabel_corrections(self, normalize_audit_log):
        """Relatório inclui correções de prefLabel."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "skos:prefLabel" in content
    
    def test_format_normalize_includes_definition_corrections(self, normalize_audit_log):
        """Relatório inclui correções de definition."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "skos:definition" in content
        assert "Ponto final adicionado" in content
    
    def test_format_includes_error_statistics(self, normalize_audit_log):
        """Relatório inclui estatísticas de erros."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Estatísticas de Erros" in content
        assert "ERROR" in content or "WARNING" in content
    
    def test_format_includes_rule_violations(self, normalize_audit_log):
        """Relatório inclui detalhamento de violações por regra."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(normalize_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Regras/Códigos Mais Violados" in content
    
    def test_format_includes_footer(self, sample_audit_log):
        """Relatório inclui rodapé com timestamp."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(sample_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Relatório gerado automaticamente" in content


class TestGenerateReviewOutput:
    """Testes para operação generate_review_output."""
    
    @pytest.fixture
    def review_audit_log(self):
        """Audit log com operação de review."""
        log_data = {
            "session_id": "review-session",
            "ops": [
                {
                    "type": "generate_review_output",
                    "status": "success",
                    "applied_at": "2024-01-15T10:10:00",
                    "triple": {
                        "subject": "edo:review",
                        "predicate": "edo:result",
                        "object": json.dumps({
                            "output": "/path/to/review.xlsx",
                            "status": "success"
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            return f.name
    
    def test_format_includes_review_output_info(self, review_audit_log):
        """Relatório inclui informações de review output."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(review_audit_log)
        
        content = Path(result).read_text(encoding='utf-8')
        assert "Geração de Arquivo de Revisão" in content
        assert "review.xlsx" in content


class TestFormatAuditLogFunction:
    """Testes para função de compatibilidade format_audit_log."""
    
    def test_format_audit_log_calls_formatter(self):
        """format_audit_log delega para AuditLogFormatter."""
        from onto_tools.adapters.reporting.audit_formatter import format_audit_log, AuditLogFormatter
        
        log_data = {"ops": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            log_path = f.name
        
        result = format_audit_log(log_path)
        
        assert Path(result).exists()
        assert result.endswith('.md')


class TestEdgeCases:
    """Testes para casos de borda."""
    
    def test_empty_ops_list(self):
        """Lida com lista de operações vazia."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        log_data = {"ops": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            log_path = f.name
        
        result = AuditLogFormatter.format_to_markdown(log_path)
        
        assert Path(result).exists()
        content = Path(result).read_text(encoding='utf-8')
        assert "Relatório" in content
    
    def test_normalize_without_fix_stats(self):
        """Lida com normalização sem fix_stats."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        log_data = {
            "ops": [
                {
                    "type": "normalize_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:00:00",
                    "triple": {
                        "object": json.dumps({
                            "status": "completed",
                            "warning_count": 0,
                            "warnings": []
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            log_path = f.name
        
        result = AuditLogFormatter.format_to_markdown(log_path)
        
        assert Path(result).exists()
    
    def test_long_subject_name_preserved(self):
        """Nomes de subject longos são preservados integralmente (sem truncamento)."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        long_name = "A" * 100
        log_data = {
            "ops": [
                {
                    "type": "normalize_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:00:00",
                    "triple": {
                        "object": json.dumps({
                            "status": "completed",
                            "warning_count": 1,
                            "warnings": [
                                {
                                    "type": "naming_convention",
                                    "severity": "error",
                                    "rule": "PascalCase",
                                    "subject": f"http://example.org#{long_name}",
                                    "issue": "Test issue",
                                    "expected": "Test"
                                }
                            ]
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            log_path = f.name
        
        result = AuditLogFormatter.format_to_markdown(log_path)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar que o nome completo está preservado (sem truncamento)
        assert long_name in content


class TestMultipleOperations:
    """Testes para múltiplas operações."""
    
    def test_multiple_ops_all_included(self):
        """Todas as operações são incluídas no relatório."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        log_data = {
            "ops": [
                {
                    "type": "load_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:00:00",
                    "triple": {"object": json.dumps({"file": "test.ttl"})}
                },
                {
                    "type": "normalize_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:01:00",
                    "triple": {"object": json.dumps({"status": "done", "warning_count": 0, "warnings": []})}
                },
                {
                    "type": "generate_review_output",
                    "status": "success",
                    "applied_at": "2024-01-15T10:02:00",
                    "triple": {"object": json.dumps({"output": "review.xlsx"})}
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            log_path = f.name
        
        result = AuditLogFormatter.format_to_markdown(log_path)
        content = Path(result).read_text(encoding='utf-8')
        
        assert "Carregamento" in content
        assert "Normalização" in content
        assert "Revisão" in content


class TestQualityIssuesCategorization:
    """Testes para categorização de quality issues no relatório."""
    
    @pytest.fixture
    def quality_issues_audit_log(self):
        """Audit log com quality issues de diferentes categorias."""
        log_data = {
            "session_id": "quality-session",
            "ops": [
                {
                    "type": "normalize_ontology",
                    "status": "success",
                    "applied_at": "2024-01-15T10:05:00",
                    "triple": {
                        "subject": "edo:normalize",
                        "predicate": "edo:result",
                        "object": json.dumps({
                            "status": "completed",
                            "warning_count": 0,
                            "warnings": [],
                            "quality_issues": [
                                # DomainAttribute issues
                                {
                                    "code": "DOMAINATTR_ACCESSRIGHTS_MISSING",
                                    "severity": "WARNING",
                                    "subject": "http://example.org#AbsoluteInsidePressure",
                                    "message": "DomainAttribute não possui dcterms:accessRights"
                                },
                                {
                                    "code": "DOMAINATTR_DEFINITION_MISSING_EN",
                                    "severity": "WARNING",
                                    "subject": "http://example.org#FlowRate",
                                    "message": "Falta skos:definition em inglês"
                                },
                                {
                                    "code": "DOMAINATTR_PROPERTY_MISSING",
                                    "severity": "WARNING",
                                    "subject": "http://example.org#Temperature",
                                    "message": "Propriedade obrigatória ausente: edo:hasAttributeScope"
                                },
                                # IFC issues
                                {
                                    "code": "IFC_REQUIRED_PROPERTY_MISSING",
                                    "severity": "ERROR",
                                    "subject": "http://example.org#IfcPipe",
                                    "message": "Classe IFC sem propriedade obrigatória: edo:ifc_class"
                                },
                                {
                                    "code": "IFC_BASE_CLASS_MISSING",
                                    "severity": "ERROR",
                                    "subject": "http://example.org#IfcValve",
                                    "message": "Classe IFC não herda de IfcInstanciableElement"
                                },
                                # General issues
                                {
                                    "code": "CLASS_IDENTIFIER_MISSING",
                                    "severity": "ERROR",
                                    "subject": "http://example.org#RegularClass",
                                    "message": "Classe não possui dcterms:identifier"
                                },
                                {
                                    "code": "MULTIPLE_PREFLABEL_SAME_LANG",
                                    "severity": "WARNING",
                                    "subject": "http://example.org#AnotherClass",
                                    "message": "Múltiplos skos:prefLabel em inglês"
                                }
                            ]
                        })
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(log_data, f)
            return f.name
    
    def test_quality_issues_separated_by_category(self, quality_issues_audit_log):
        """Quality issues são separados por categoria: DomainAttribute, IFC, Geral."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar seções por categoria
        assert "Issues de DomainAttribute" in content
        assert "Issues de Classes IFC" in content
        assert "Issues Gerais" in content
    
    def test_domain_attribute_issues_have_own_section(self, quality_issues_audit_log):
        """Issues de DomainAttribute aparecem em seção própria."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar que entidades DomainAttribute estão na seção correta
        assert "AbsoluteInsidePressure" in content
        assert "FlowRate" in content
        assert "Temperature" in content
        assert "DOMAINATTR_" in content
    
    def test_ifc_issues_have_own_section(self, quality_issues_audit_log):
        """Issues de IFC aparecem em seção própria."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar que entidades IFC estão na seção correta
        assert "IfcPipe" in content
        assert "IfcValve" in content
        assert "IFC_" in content
    
    def test_general_issues_have_own_section(self, quality_issues_audit_log):
        """Issues gerais aparecem em seção própria."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar que entidades gerais estão na seção correta
        assert "RegularClass" in content
        assert "AnotherClass" in content
    
    def test_issues_sorted_alphabetically_by_entity(self, quality_issues_audit_log):
        """Issues são ordenados alfabeticamente por entidade dentro de cada categoria."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar ordem (AbsoluteInsidePressure deve vir antes de FlowRate e Temperature)
        pos_absolute = content.find("AbsoluteInsidePressure")
        pos_flow = content.find("FlowRate")
        pos_temp = content.find("Temperature")
        
        # Todos devem ser encontrados
        assert pos_absolute > 0
        assert pos_flow > 0
        assert pos_temp > 0
        
        # AbsoluteInsidePressure < FlowRate < Temperature (ordem alfabética)
        assert pos_absolute < pos_flow < pos_temp
    
    def test_legend_includes_category_sections(self, quality_issues_audit_log):
        """Legenda é organizada por categoria."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar que legenda tem seções por categoria
        assert "**DomainAttribute:**" in content
        assert "**Classes IFC:**" in content
        assert "**Geral:**" in content
    
    def test_entity_column_before_code_column(self, quality_issues_audit_log):
        """Entidade aparece antes do código no formato de lista."""
        from onto_tools.adapters.reporting.audit_formatter import AuditLogFormatter
        
        result = AuditLogFormatter.format_to_markdown(quality_issues_audit_log)
        content = Path(result).read_text(encoding='utf-8')
        
        # Verificar formato de lista: entidade em negrito seguido de código
        # Novo formato: - **`Entidade`** — `CODIGO`
        assert "**`" in content  # Entidade em negrito e código
        assert "` —" in content or "`**" in content  # Separador ou fim do nome
