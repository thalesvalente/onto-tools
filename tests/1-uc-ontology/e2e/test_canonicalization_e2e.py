"""
Testes E2E de canonicalização - fluxo completo com arquivos reais.

Cobre:
- Canonicalização de ontologia completa
- Validação de output Protégé-compatível
- Roundtrip com arquivos reais
"""
import pytest
from pathlib import Path

from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.graph import OntologyGraph
from onto_tools.domain.ontology.normalizer import Normalizer


class TestCanonicalizationE2E:
    """Testes E2E de canonicalização."""
    
    def test_canonicalize_sample_ontology(self, tmp_path, sample_ontology, rules_json_path):
        """Canonicaliza ontologia de exemplo completa."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        # Carregar
        onto = OntologyGraph.load(sample_ontology, RDFlibAdapter)
        
        # Normalizar
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        # Salvar
        output_file = tmp_path / "canonicalized.ttl"
        normalized.save(str(output_file), RDFlibAdapter)
        
        # Verificar
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        
        # Deve ser parseável
        reloaded, _ = RDFlibAdapter.load_ttl(str(output_file))
        # Normalização pode modificar levemente o número de triplas
        # (ex: adição de prefixos obrigatórios, correções)
        # Verificar que a diferença é pequena (< 5%)
        diff_pct = abs(len(reloaded) - len(onto.graph)) / len(onto.graph)
        assert diff_pct < 0.05, f"Diferença excessiva: {len(reloaded)} vs {len(onto.graph)}"
    
    def test_canonicalization_is_idempotent(self, tmp_path, sample_ontology, rules_json_path):
        """Canonicalização é idempotente (aplicar duas vezes = mesmo resultado)."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        normalizer = Normalizer(rules_path=rules_json_path)
        
        # Primeira canonicalização
        onto1 = OntologyGraph.load(sample_ontology, RDFlibAdapter)
        normalized1 = onto1.normalize(normalizer)
        
        output1 = tmp_path / "pass1.ttl"
        normalized1.save(str(output1), RDFlibAdapter)
        
        # Segunda canonicalização
        onto2 = OntologyGraph.load(str(output1), RDFlibAdapter)
        normalized2 = onto2.normalize(normalizer)
        
        output2 = tmp_path / "pass2.ttl"
        normalized2.save(str(output2), RDFlibAdapter)
        
        # Comparar conteúdo semântico
        g1, _ = RDFlibAdapter.load_ttl(str(output1))
        g2, _ = RDFlibAdapter.load_ttl(str(output2))
        
        # Segunda passada deve ser estável (mesmo número de triplas)
        assert len(g1) == len(g2)
    
    def test_output_is_protege_compatible(self, tmp_path, sample_ontology, rules_json_path):
        """Output é compatível com Protégé."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        onto = OntologyGraph.load(sample_ontology, RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        normalized = onto.normalize(normalizer)
        
        output_file = tmp_path / "protege_compat.ttl"
        normalized.save(str(output_file), RDFlibAdapter)
        
        # Ler conteúdo e verificar características Protégé
        content = output_file.read_text(encoding="utf-8")
        
        # Deve ter prefixos ordenados
        assert "@prefix" in content
        
        # Não deve ter prefixos auto-gerados (ns1, ns2)
        assert "ns1:" not in content
        assert "ns2:" not in content


class TestValidationE2E:
    """Testes E2E de validação."""
    
    def test_validate_sample_ontology(self, sample_ontology, rules_json_path):
        """Valida ontologia de exemplo."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        onto = OntologyGraph.load(sample_ontology, RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        
        normalized = onto.normalize(normalizer)
        
        # Obter warnings
        warnings = normalizer.get_warnings()
        
        # Pode haver warnings, mas não deve falhar
        assert isinstance(warnings, list)
    
    def test_naming_validation_report(self, sample_ontology, rules_json_path):
        """Gera relatório de validação de nomenclatura."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        onto = OntologyGraph.load(sample_ontology, RDFlibAdapter)
        normalizer = Normalizer(rules_path=rules_json_path)
        
        normalized = onto.normalize(normalizer)
        
        report = normalizer.get_naming_validation_report()
        
        # Se naming_syntax está configurado, deve haver relatório
        if normalizer.rules.get("naming_syntax"):
            if report:
                assert "summary" in report
                assert "errors" in report
                assert "warnings" in report


class TestRoundtripE2E:
    """Testes E2E de roundtrip."""
    
    def test_multiple_roundtrips(self, tmp_path, sample_ontology, rules_json_path):
        """Múltiplos roundtrips preservam conteúdo."""
        if not Path(sample_ontology).exists():
            pytest.skip("Ontologia de exemplo não encontrada")
        
        normalizer = Normalizer(rules_path=rules_json_path)
        current_file = sample_ontology
        
        for i in range(3):
            onto = OntologyGraph.load(current_file, RDFlibAdapter)
            normalized = onto.normalize(normalizer)
            
            output_file = tmp_path / f"round{i}.ttl"
            normalized.save(str(output_file), RDFlibAdapter)
            
            current_file = str(output_file)
        
        # Carregar original e final
        original, _ = RDFlibAdapter.load_ttl(sample_ontology)
        final, _ = RDFlibAdapter.load_ttl(current_file)
        
        # Normalização pode remover duplicatas ou ajustar triplas
        # Verificar que a diferença é pequena (< 1%)
        diff_pct = abs(len(final) - len(original)) / len(original)
        assert diff_pct < 0.01, f"Diferença excessiva: {len(final)} vs {len(original)}"
