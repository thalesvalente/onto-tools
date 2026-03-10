"""
Testes de alinhamento de colunas para o serializador estilo Protégé.

Verifica que predicados e objetos estão alinhados nas colunas corretas.
"""
import pytest
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, DCTERMS

from onto_tools.adapters.rdf.protege_serializer import (
    ProtegeStyleTurtleSerializer,
    serialize_protege_style,
)


class TestPredicateColumnAlignment:
    """Testes para verificar alinhamento de predicados."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        return graph

    def test_predicates_aligned_with_rdf_type(self, edo_namespace):
        """
        Testa que todos os predicados começam na mesma coluna que rdf:type.
        
        Requisito:
        edo:GrooveHeight rdf:type owl:Class ;
                         rdfs:subClassOf edo:DomainAttribute ;
                         ^-- mesma coluna
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.GrooveHeight, RDF.type, OWL.Class))
        graph.add((edo.GrooveHeight, RDFS.subClassOf, edo.DomainAttribute))
        graph.add((edo.GrooveHeight, DCTERMS.identifier, Literal("GrooveHeight")))
        graph.add((edo.GrooveHeight, SKOS.prefLabel, Literal("Groove Height", lang="en")))
        graph.add((edo.GrooveHeight, SKOS.definition, Literal("The height.", lang="en")))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        # Encontrar linha com rdf:type
        rdf_type_line = None
        rdf_type_col = None
        for line in lines:
            if "rdf:type" in line and "edo:GrooveHeight" in line:
                rdf_type_line = line
                rdf_type_col = line.index("rdf:type")
                break

        assert rdf_type_line is not None, "Linha com rdf:type não encontrada"
        assert rdf_type_col is not None, "Coluna de rdf:type não encontrada"

        # Verificar que outros predicados começam na mesma coluna
        predicates_to_check = ["rdfs:subClassOf", "dcterms:identifier", "skos:prefLabel", "skos:definition"]
        
        for pred in predicates_to_check:
            for line in lines:
                if pred in line and not line.startswith("@prefix"):
                    # Linha de continuação (não contém sujeito)
                    if line.strip().startswith(pred):
                        pred_col = line.index(pred)
                        assert pred_col == rdf_type_col, \
                            f"Predicado '{pred}' na coluna {pred_col}, esperado {rdf_type_col}\nLinha: {line}"

    def test_first_predicate_after_subject_with_single_space(self, edo_namespace):
        """
        Testa que o primeiro predicado vem após o sujeito com um único espaço.
        
        Requisito:
        edo:GrooveHeight rdf:type owl:Class ;
        ^subject        ^single space before predicate
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        for line in lines:
            if "edo:TestClass" in line and "rdf:type" in line:
                # Deve ser "edo:TestClass rdf:type"
                assert "edo:TestClass rdf:type" in line, \
                    f"Sujeito e predicado não separados por espaço único:\n{line}"
                break
        else:
            pytest.fail("Linha com edo:TestClass não encontrada")


class TestObjectColumnAlignment:
    """Testes para verificar alinhamento de objetos múltiplos."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("dcterms", DCTERMS)
        return graph

    def test_multiple_objects_aligned_under_first(self, edo_namespace):
        """
        Testa que objetos adicionais são alinhados sob o primeiro objeto.
        
        Requisito:
        skos:prefLabel "Groove Height"@en ,
                       "Altura do Groove"@pt-br ;
                       ^-- alinhado com primeiro objeto
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test Class", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Classe de Teste", lang="pt-br")))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        # Encontrar linha com primeiro prefLabel
        first_obj_col = None
        for i, line in enumerate(lines):
            if 'skos:prefLabel' in line:
                # Encontrar posição do primeiro "
                first_obj_col = line.index('"')
                
                # Próxima linha deve ter segundo objeto alinhado
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if '"' in next_line and "@pt-br" in next_line:
                        second_obj_col = next_line.index('"')
                        assert second_obj_col == first_obj_col, \
                            f"Segundo objeto na coluna {second_obj_col}, esperado {first_obj_col}"
                break

    def test_multiple_subclassof_aligned(self, edo_namespace):
        """
        Testa alinhamento de múltiplos rdfs:subClassOf.
        
        Requisito:
        rdfs:subClassOf edo:DomainElement ,
                        edo:IfcInstanciableElement ;
                        ^-- alinhado com primeiro
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.DomainElement))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.IfcInstanciableElement))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        # Encontrar linha com primeiro subClassOf
        first_obj_col = None
        for i, line in enumerate(lines):
            if 'rdfs:subClassOf' in line:
                # Encontrar posição do primeiro objeto (edo:...)
                idx = line.find("edo:", line.find("rdfs:subClassOf"))
                if idx >= 0:
                    first_obj_col = idx
                    
                    # Próxima linha deve ter segundo objeto alinhado
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if "edo:" in next_line:
                            second_obj_col = next_line.index("edo:")
                            assert second_obj_col == first_obj_col, \
                                f"Segundo subClassOf na coluna {second_obj_col}, esperado {first_obj_col}"
                break


class TestPunctuationRules:
    """Testes para verificar pontuação correta."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        return graph

    def test_last_predicate_ends_with_period(self, edo_namespace):
        """
        Testa que o último predicado termina com ponto.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.label, Literal("Test", lang="en")))

        result = serialize_protege_style(graph)
        
        # Remover linhas vazias do final
        lines = [l for l in result.strip().split("\n") if l.strip()]
        
        # Última linha deve terminar com .
        last_line = lines[-1]
        assert last_line.rstrip().endswith(" ."), \
            f"Última linha não termina com ' .':\n{last_line}"

    def test_intermediate_predicates_end_with_semicolon(self, edo_namespace):
        """
        Testa que predicados intermediários terminam com ponto-e-vírgula.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, RDFS.subClassOf, edo.Parent))
        graph.add((edo.TestClass, RDFS.label, Literal("Test", lang="en")))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        # Encontrar linhas de predicados (não prefixos, não vazias)
        subject_lines = []
        in_subject_block = False
        for line in lines:
            if line.startswith("@prefix"):
                continue
            if not line.strip():
                in_subject_block = False
                continue
            if "edo:TestClass" in line:
                in_subject_block = True
            if in_subject_block:
                subject_lines.append(line)

        # Todas exceto a última devem terminar com ;
        for line in subject_lines[:-1]:
            assert line.rstrip().endswith(" ;"), \
                f"Linha intermediária não termina com ' ;':\n{line}"

    def test_multiple_objects_use_comma(self, edo_namespace):
        """
        Testa que múltiplos objetos são separados por vírgula.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Test", lang="en")))
        graph.add((edo.TestClass, SKOS.prefLabel, Literal("Teste", lang="pt-br")))

        result = serialize_protege_style(graph)
        lines = result.split("\n")

        # Encontrar linha com primeiro prefLabel
        for i, line in enumerate(lines):
            if 'skos:prefLabel' in line and '"Test"@en' in line:
                assert line.rstrip().endswith(" ,"), \
                    f"Primeiro objeto de múltiplos deve terminar com ',':\n{line}"
                break


class TestSubjectBlockSeparation:
    """Testes para verificar separação de blocos de sujeitos."""

    @pytest.fixture
    def edo_namespace(self):
        """Namespace EDO para testes."""
        return Namespace("https://w3id.org/energy-domain/edo#")

    def _create_graph_with_prefixes(self, edo: Namespace) -> Graph:
        """Cria grafo com prefixos padrão."""
        graph = Graph()
        graph.bind("edo", edo)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)
        return graph

    def test_subjects_separated_by_blank_line(self, edo_namespace):
        """
        Testa que blocos de sujeitos são separados por linha em branco.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.ClassA, RDF.type, OWL.Class))
        graph.add((edo.ClassB, RDF.type, OWL.Class))

        result = serialize_protege_style(graph)
        
        # Deve haver linha em branco entre ClassA e ClassB
        assert "\n\n" in result or "\r\n\r\n" in result, \
            f"Blocos de sujeitos não separados por linha em branco:\n{result}"

    def test_prefix_block_separated_from_subjects(self, edo_namespace):
        """
        Testa que bloco de prefixos é separado dos sujeitos por linha em branco.
        """
        edo = edo_namespace
        graph = self._create_graph_with_prefixes(edo)

        graph.add((edo.TestClass, RDF.type, OWL.Class))

        result = serialize_protege_style(graph)
        lines = result.split("\n")
        
        # Encontrar última linha de prefixo
        last_prefix_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("@prefix"):
                last_prefix_idx = i
        
        # Próxima linha deve ser vazia
        assert last_prefix_idx >= 0, "Nenhum prefixo encontrado"
        assert last_prefix_idx + 1 < len(lines), "Não há linhas após prefixos"
        assert lines[last_prefix_idx + 1].strip() == "", \
            "Deve haver linha em branco após prefixos"
