"""
Testes para OntologyGraph - Classe central CRUD de grafos RDF.

Cobre:
- Carregamento de arquivos TTL
- Salvamento de grafos
- Normalização via Normalizer
- Consultas SPARQL
- Operações CRUD (add_triple, remove_triple)
- Aplicação de lotes (batch_apply)
- Diff entre grafos
"""
import pytest
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

from onto_tools.domain.ontology.graph import OntologyGraph, OntologyMetadata
from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.normalizer import Normalizer


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


class TestOntologyGraphLoad:
    """Testes de carregamento de ontologias."""
    
    def test_load_valid_file(self, tmp_ttl_file):
        """Carrega arquivo TTL válido."""
        onto = OntologyGraph.load(tmp_ttl_file, RDFlibAdapter)
        
        assert onto.graph is not None
        assert onto.metadata is not None
        assert onto.metadata.triple_count > 0
    
    def test_load_creates_metadata(self, tmp_ttl_file):
        """Carregamento cria metadados corretos."""
        onto = OntologyGraph.load(tmp_ttl_file, RDFlibAdapter)
        
        assert onto.metadata.hash is not None
        assert onto.metadata.timestamp is not None
        assert onto.metadata.source_path is not None
    
    def test_load_extracts_prefixes(self, tmp_ttl_file):
        """Carregamento extrai prefixos do grafo."""
        onto = OntologyGraph.load(tmp_ttl_file, RDFlibAdapter)
        
        assert onto.prefixes is not None
        assert isinstance(onto.prefixes, dict)
    
    def test_load_nonexistent_raises(self):
        """Arquivo inexistente levanta FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            OntologyGraph.load("/nao/existe/ontology.ttl", RDFlibAdapter)
    
    def test_load_stores_source_path(self, tmp_ttl_file):
        """Carregamento armazena caminho de origem."""
        onto = OntologyGraph.load(tmp_ttl_file, RDFlibAdapter)
        
        assert onto.source_path == tmp_ttl_file


class TestOntologyGraphSave:
    """Testes de salvamento de ontologias."""
    
    def test_save_creates_file(self, tmp_path, minimal_class_graph):
        """Salvamento cria arquivo."""
        onto = OntologyGraph(graph=minimal_class_graph)
        output = tmp_path / "output.ttl"
        
        onto.save(str(output), RDFlibAdapter)
        
        assert output.exists()
    
    def test_save_without_graph_raises(self, tmp_path):
        """Salvamento sem grafo levanta ValueError."""
        onto = OntologyGraph()
        output = tmp_path / "output.ttl"
        
        with pytest.raises(ValueError, match="Nenhum grafo"):
            onto.save(str(output), RDFlibAdapter)
    
    def test_save_creates_parent_dirs(self, tmp_path, minimal_class_graph):
        """Salvamento cria diretórios pai se necessário."""
        onto = OntologyGraph(graph=minimal_class_graph)
        output = tmp_path / "subdir" / "output.ttl"
        
        onto.save(str(output), RDFlibAdapter)
        
        assert output.exists()


class TestOntologyGraphNormalize:
    """Testes de normalização de ontologias."""
    
    def test_normalize_returns_new_ontology(self, minimal_class_graph, normalizer):
        """Normalização retorna nova instância OntologyGraph."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        normalized = onto.normalize(normalizer)
        
        assert normalized is not onto
        assert normalized.graph is not onto.graph
    
    def test_normalize_preserves_metadata(self, minimal_class_graph, normalizer):
        """Normalização preserva metadados."""
        metadata = OntologyMetadata(
            hash="abc123",
            triple_count=5,
            timestamp="2024-01-01T00:00:00"
        )
        onto = OntologyGraph(graph=minimal_class_graph, metadata=metadata)
        
        normalized = onto.normalize(normalizer)
        
        assert normalized.metadata == onto.metadata
    
    def test_normalize_without_graph_raises(self, normalizer):
        """Normalização sem grafo levanta ValueError."""
        onto = OntologyGraph()
        
        with pytest.raises(ValueError, match="Nenhum grafo"):
            onto.normalize(normalizer)


class TestOntologyGraphAddTriple:
    """Testes de adição de triplas."""
    
    def test_add_triple_basic(self, minimal_class_graph):
        """Adiciona tripla básica."""
        onto = OntologyGraph(graph=minimal_class_graph)
        initial_count = len(onto.graph)
        
        onto.add_triple(
            "edo:NewClass",
            "rdf:type", 
            "owl:Class"
        )
        
        assert len(onto.graph) == initial_count + 1
    
    def test_add_triple_with_literal(self, minimal_class_graph):
        """Adiciona tripla com literal."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        onto.add_triple(
            "edo:TestClass",
            "rdfs:comment",
            "This is a comment",
            obj_is_literal=True
        )
        
        comments = list(onto.graph.objects(EDO.TestClass, RDFS.comment))
        assert len(comments) == 1
        assert str(comments[0]) == "This is a comment"
    
    def test_add_triple_updates_metadata(self, minimal_class_graph):
        """Adição atualiza contagem de triplas nos metadados."""
        metadata = OntologyMetadata(
            hash="abc123",
            triple_count=len(minimal_class_graph),
            timestamp="2024-01-01"
        )
        onto = OntologyGraph(graph=minimal_class_graph, metadata=metadata)
        
        onto.add_triple("edo:NewClass", "rdf:type", "owl:Class")
        
        assert onto.metadata.triple_count == len(onto.graph)
    
    def test_add_triple_without_graph_raises(self):
        """Adição sem grafo levanta ValueError."""
        onto = OntologyGraph()
        
        with pytest.raises(ValueError, match="Nenhum grafo"):
            onto.add_triple("edo:A", "rdf:type", "owl:Class")


class TestOntologyGraphRemoveTriple:
    """Testes de remoção de triplas."""
    
    def test_remove_triple_basic(self, minimal_class_graph):
        """Remove tripla básica."""
        onto = OntologyGraph(graph=minimal_class_graph)
        initial_count = len(onto.graph)
        
        onto.remove_triple(
            "edo:TestClass",
            "rdf:type",
            "owl:Class"
        )
        
        assert len(onto.graph) == initial_count - 1
    
    def test_remove_triple_updates_metadata(self, minimal_class_graph):
        """Remoção atualiza contagem de triplas nos metadados."""
        metadata = OntologyMetadata(
            hash="abc123",
            triple_count=len(minimal_class_graph),
            timestamp="2024-01-01"
        )
        onto = OntologyGraph(graph=minimal_class_graph, metadata=metadata)
        
        onto.remove_triple("edo:TestClass", "rdf:type", "owl:Class")
        
        assert onto.metadata.triple_count == len(onto.graph)
    
    def test_remove_triple_without_graph_raises(self):
        """Remoção sem grafo levanta ValueError."""
        onto = OntologyGraph()
        
        with pytest.raises(ValueError, match="Nenhum grafo"):
            onto.remove_triple("edo:A", "rdf:type", "owl:Class")


class TestOntologyGraphBatchApply:
    """Testes de aplicação de lotes (UC-107)."""
    
    def test_batch_apply_insert(self, minimal_class_graph):
        """Aplica operação de inserção em lote."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-001",
            "onto_name": "test",
            "onto_version": "1.0",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:NewClass",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"
        assert result["metrics"]["applied_ops"] == 1
        assert result["metrics"]["failed_ops"] == 0
    
    def test_batch_apply_delete(self, minimal_class_graph):
        """Aplica operação de remoção em lote."""
        onto = OntologyGraph(graph=minimal_class_graph)
        initial_count = len(onto.graph)
        
        update_list = {
            "batch_id": "test-002",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "delete",
                    "triple": {
                        "subject": "edo:TestClass",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"
        assert len(onto.graph) == initial_count - 1
    
    def test_batch_apply_rollback_on_error(self, minimal_class_graph):
        """Lote com erro faz rollback (tudo-ou-nada)."""
        onto = OntologyGraph(graph=minimal_class_graph)
        initial_triples = set(onto.graph)
        
        update_list = {
            "batch_id": "test-003",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:Valid",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                },
                {
                    "op_id": 2,
                    "type": "invalid_type",  # Tipo inválido causa erro
                    "triple": {
                        "subject": "edo:X",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "failed"
        # Grafo deve permanecer inalterado
        assert set(onto.graph) == initial_triples
    
    def test_batch_apply_processes_all_operations(self, minimal_class_graph):
        """Lote processa todas as operações mesmo com erros."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-004",
            "ordered_ops": [
                {"op_id": 1, "type": "insert", "triple": {"subject": "edo:A", "predicate": "rdf:type", "object": "owl:Class"}},
                {"op_id": 2, "type": "bad_type", "triple": {"subject": "edo:B", "predicate": "rdf:type", "object": "owl:Class"}},
                {"op_id": 3, "type": "insert", "triple": {"subject": "edo:C", "predicate": "rdf:type", "object": "owl:Class"}},
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        # Todas foram processadas
        assert result["metrics"]["total_ops"] == 3
        assert result["metrics"]["applied_ops"] == 2
        assert result["metrics"]["failed_ops"] == 1


class TestOntologyGraphDiff:
    """Testes de diff entre grafos."""
    
    def test_diff_added_triples(self, minimal_class_graph):
        """Detecta triplas adicionadas."""
        onto1 = OntologyGraph(graph=minimal_class_graph)
        
        # Criar grafo com tripla extra
        g2 = Graph()
        for triple in minimal_class_graph:
            g2.add(triple)
        g2.add((EDO.NewClass, RDF.type, OWL.Class))
        
        onto2 = OntologyGraph(graph=g2)
        
        diff = onto1.diff(onto2)
        
        assert diff["added_count"] == 1
        assert len(diff["added"]) == 1
    
    def test_diff_removed_triples(self, minimal_class_graph):
        """Detecta triplas removidas."""
        onto1 = OntologyGraph(graph=minimal_class_graph)
        
        # Criar grafo com menos triplas
        g2 = Graph()
        for triple in minimal_class_graph:
            g2.add(triple)
        g2.remove((EDO.TestClass, RDF.type, OWL.Class))
        
        onto2 = OntologyGraph(graph=g2)
        
        diff = onto1.diff(onto2)
        
        assert diff["removed_count"] == 1
    
    def test_diff_identical_graphs(self, minimal_class_graph):
        """Grafos idênticos não têm diferenças."""
        onto1 = OntologyGraph(graph=minimal_class_graph)
        onto2 = OntologyGraph(graph=minimal_class_graph)
        
        diff = onto1.diff(onto2)
        
        assert diff["added_count"] == 0
        assert diff["removed_count"] == 0
    
    def test_diff_without_graph_raises(self):
        """Diff sem grafos levanta ValueError."""
        onto1 = OntologyGraph()
        onto2 = OntologyGraph()
        
        with pytest.raises(ValueError, match="Ambos os grafos"):
            onto1.diff(onto2)


class TestOntologyGraphReviewLog:
    """Testes de geração de log de revisão."""
    
    def test_generate_review_log(self, minimal_class_graph):
        """Gera log de revisão com campos obrigatórios."""
        onto = OntologyGraph(graph=minimal_class_graph, source_path="/path/to/ont.ttl")
        
        log = onto.generate_review_log(
            sparql_filters=["?s rdf:type owl:Class"],
            input_file="/input.ttl",
            output_file="/output.ttl"
        )
        
        assert "onto_name" in log
        assert "date" in log
        assert "hour" in log
        assert "metricas" in log
        assert "contexto_execucao" in log
    
    def test_review_log_contains_metrics(self, minimal_class_graph):
        """Log contém métricas de exportação."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        log = onto.generate_review_log()
        
        assert "triples_exportadas" in log["metricas"]
        assert log["metricas"]["triples_exportadas"] == len(minimal_class_graph)


# =============================================================================
# TESTES ADICIONAIS DE COBERTURA - graph.py
# =============================================================================

class TestOntologyGraphLoadExceptions:
    """Testes para exceções no load() - linhas 38-43."""
    
    def test_load_invalid_encoding_raises_valueerror(self, tmp_path):
        """Arquivo com encoding inválido levanta ValueError."""
        bad_file = tmp_path / "bad_encoding.ttl"
        # Escrever bytes que não são UTF-8 válido
        bad_file.write_bytes(b"@prefix edo: <http://test#> .\nedo:Test \xff\xfe a owl:Class .")
        
        # O adapter pode lançar ValueError ou RuntimeError dependendo de como processa
        with pytest.raises((ValueError, RuntimeError)):
            OntologyGraph.load(str(bad_file), RDFlibAdapter)
    
    def test_load_invalid_turtle_raises_error(self, tmp_path):
        """Arquivo com Turtle inválido levanta ValueError ou RuntimeError."""
        bad_file = tmp_path / "invalid.ttl"
        # Usar conteúdo ASCII puro para evitar problema de encoding
        bad_file.write_text("this is not valid turtle { [ } ]", encoding="utf-8")
        
        with pytest.raises((ValueError, RuntimeError)):
            OntologyGraph.load(str(bad_file), RDFlibAdapter)


class TestOntologyGraphAddTripleErrors:
    """Testes para erros em add_triple() - linhas 122-132."""
    
    def test_add_triple_literal_subject_raises(self, minimal_class_graph):
        """Subject como literal deve gerar erro."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="Subject deve ser URI"):
            onto.add_triple('"literal-subject"', "rdf:type", "owl:Class")
    
    def test_add_triple_literal_predicate_raises(self, minimal_class_graph):
        """Predicate como literal deve gerar erro."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="Predicate deve ser URI"):
            onto.add_triple("edo:NewClass", '"not-a-uri"', "owl:Class")
    
    def test_add_triple_invalid_subject_prefix_raises(self, minimal_class_graph):
        """Prefixo inválido no subject deve gerar erro."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="(Erro ao resolver|Subject)"):
            onto.add_triple("unknown_prefix:Class", "rdf:type", "owl:Class")


class TestOntologyGraphRemoveTripleErrors:
    """Testes para erros em remove_triple() - linhas 172-188."""
    
    def test_remove_triple_literal_subject_raises(self, minimal_class_graph):
        """Subject como literal em remove deve gerar erro."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="Subject deve ser URI"):
            onto.remove_triple('"literal-subject"', "rdf:type", "owl:Class")
    
    def test_remove_triple_literal_predicate_raises(self, minimal_class_graph):
        """Predicate como literal em remove deve gerar erro."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="Predicate deve ser URI"):
            onto.remove_triple("edo:TestClass", '"not-uri"', "owl:Class")
    
    def test_remove_triple_with_none_object(self, minimal_class_graph):
        """Remove_triple com object=None remove todas triplas com s,p."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        # Adicionar múltiplos prefLabels (grafo pode já ter alguns)
        onto.graph.add((EDO.TestClass, SKOS.prefLabel, Literal("Label 1", lang="en")))
        onto.graph.add((EDO.TestClass, SKOS.prefLabel, Literal("Label 2", lang="pt")))
        
        labels_before = list(onto.graph.objects(EDO.TestClass, SKOS.prefLabel))
        assert len(labels_before) >= 2  # Pode ter mais se fixture já tinha
        
        # Remover todos os prefLabels de uma vez
        onto.remove_triple("edo:TestClass", "skos:prefLabel", None)
        
        labels_after = list(onto.graph.objects(EDO.TestClass, SKOS.prefLabel))
        assert len(labels_after) == 0
    
    def test_remove_triple_with_literal_object(self, minimal_class_graph):
        """Remove_triple com obj_is_literal=True remove literal específico."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        # Adicionar um comentário
        onto.graph.add((EDO.TestClass, RDFS.comment, Literal("To be removed")))
        
        onto.remove_triple("edo:TestClass", "rdfs:comment", "To be removed", obj_is_literal=True)
        
        comments = list(onto.graph.objects(EDO.TestClass, RDFS.comment))
        assert len(comments) == 0


class TestOntologyGraphBatchApplyExtended:
    """Testes adicionais para batch_apply() - linhas 250-334."""
    
    def test_batch_apply_without_graph_raises(self):
        """Batch_apply sem grafo levanta ValueError."""
        onto = OntologyGraph()
        
        with pytest.raises(ValueError, match="Nenhum grafo carregado"):
            onto.batch_apply({"ordered_ops": []})
    
    def test_batch_apply_literal_subject_fails(self, minimal_class_graph):
        """Batch_apply com literal no subject registra falha."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-err-001",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": '"literal-subject"',
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["metrics"]["failed_ops"] == 1
    
    def test_batch_apply_literal_predicate_fails(self, minimal_class_graph):
        """Batch_apply com literal no predicate registra falha."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-err-002",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:NewClass",
                        "predicate": '"not-uri"',
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["metrics"]["failed_ops"] == 1
    
    def test_batch_apply_update_operation(self, minimal_class_graph):
        """Batch_apply com operação update substitui valor."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        # Adicionar um label original
        onto.graph.add((EDO.TestClass, SKOS.prefLabel, Literal("Old Label", lang="en")))
        
        update_list = {
            "batch_id": "test-update-001",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "update",
                    "triple": {
                        "subject": "edo:TestClass",
                        "predicate": "skos:prefLabel",
                        "object": "New Label",
                        "language": "en"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"
        # Verifica que o label foi atualizado
        labels = [str(l) for l in onto.graph.objects(EDO.TestClass, SKOS.prefLabel)]
        assert "New Label" in labels
    
    def test_batch_apply_explicit_literal_with_quotes(self, minimal_class_graph):
        """Batch_apply com literal explícito entre aspas."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-literal-001",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:TestClass",
                        "predicate": "rdfs:comment",
                        "object": '"This is a literal value"'
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"
        comments = list(onto.graph.objects(EDO.TestClass, RDFS.comment))
        assert len(comments) == 1
        assert str(comments[0]) == "This is a literal value"
    
    def test_batch_apply_with_language_tag(self, minimal_class_graph):
        """Batch_apply com language tag cria literal correto."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        update_list = {
            "batch_id": "test-lang-001",
            "ordered_ops": [
                {
                    "op_id": 1,
                    "type": "insert",
                    "triple": {
                        "subject": "edo:TestClass",
                        "predicate": "skos:prefLabel",
                        "object": "Test Class",
                        "language": "en"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        assert result["overall_result"] == "success"


class TestOntologyGraphDiffExtended:
    """Testes adicionais para diff() - linha 376."""
    
    def test_diff_with_first_graph_none_raises(self, minimal_class_graph):
        """Diff com primeiro grafo None levanta ValueError."""
        onto1 = OntologyGraph()  # graph=None
        onto2 = OntologyGraph(graph=minimal_class_graph)
        
        with pytest.raises(ValueError, match="Ambos os grafos"):
            onto1.diff(onto2)
    
    def test_diff_with_second_graph_none_raises(self, minimal_class_graph):
        """Diff com segundo grafo None levanta ValueError."""
        onto1 = OntologyGraph(graph=minimal_class_graph)
        onto2 = OntologyGraph()  # graph=None
        
        with pytest.raises(ValueError, match="Ambos os grafos"):
            onto1.diff(onto2)


class TestOntologyGraphQueryExtended:
    """Testes adicionais para query() - linha 90."""
    
    def test_query_executes_sparql(self, minimal_class_graph):
        """Query executa SPARQL e retorna resultados."""
        from unittest.mock import Mock
        
        onto = OntologyGraph(graph=minimal_class_graph)
        
        # Mock do query engine com método execute
        mock_engine = Mock()
        mock_engine.execute.return_value = [{"s": str(EDO.TestClass)}]
        
        results = onto.query("SELECT ?s WHERE { ?s a owl:Class }", mock_engine)
        
        assert results is not None
        assert isinstance(results, list)
        mock_engine.execute.assert_called_once()


class TestOntologyGraphFullCoverage:
    """Testes para 100% de cobertura em graph.py."""
    
    def test_load_with_utf8_error_raises_encoding_message(self, tmp_path):
        """Load com erro UTF-8 retorna mensagem sobre encoding (linhas 40-41)."""
        from unittest.mock import MagicMock, patch
        
        # Criar um adapter mock que levanta ValueError com "UTF-8" na mensagem
        mock_adapter = MagicMock()
        mock_adapter.load_ttl.side_effect = ValueError("Erro de encoding UTF-8 no arquivo")
        
        with pytest.raises(ValueError, match="Encoding inválido"):
            OntologyGraph.load("qualquer.ttl", mock_adapter)
    
    def test_load_with_generic_exception_raises_runtime_error(self, tmp_path):
        """Load com exceção genérica levanta RuntimeError (linhas 42-43)."""
        from unittest.mock import MagicMock
        
        # Criar um adapter mock que levanta exceção genérica
        mock_adapter = MagicMock()
        mock_adapter.load_ttl.side_effect = RuntimeError("Erro inesperado no adapter")
        
        with pytest.raises(RuntimeError, match="Erro ao carregar ontologia"):
            OntologyGraph.load("qualquer.ttl", mock_adapter)
    
    def test_batch_apply_skips_empty_prefix(self, minimal_class_graph):
        """batch_apply ignora prefixos vazios (linha 272->271)."""
        onto = OntologyGraph(graph=minimal_class_graph)
        
        # Update list com prefix vazio que deve ser ignorado
        update_list = {
            "prefixes": {
                "edo": str(EDO),
                "": "http://should-be-ignored/",  # Prefixo vazio
                "owl": str(OWL)
            },
            "changes": [
                {
                    "action": "add",
                    "triple": {
                        "subject": "edo:TestClass2",
                        "predicate": "rdf:type",
                        "object": "owl:Class"
                    }
                }
            ]
        }
        
        result = onto.batch_apply(update_list)
        
        # Deve funcionar sem erro
        assert result is not None
        
        # Verificar que o prefixo vazio não foi vinculado
        prefixes = dict(onto.graph.namespaces())
        assert "" not in prefixes or prefixes.get("") != "http://should-be-ignored/"
    
    def test_load_nonexistent_file_raises(self, tmp_path):
        """Load levanta exceção para arquivo inexistente."""
        with pytest.raises(FileNotFoundError):
            OntologyGraph.load(str(tmp_path / "nonexistent.ttl"), RDFlibAdapter)
