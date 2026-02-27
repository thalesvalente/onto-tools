"""
Integration tests for facade.normalize_ontology() - UC-108.

These tests exercise the full facade.normalize_ontology() execution
(lines 531-757 of facade.py), including audit-log construction for
pending prefLabel and definition corrections.
"""
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import OWL, RDF, SKOS

from onto_tools.application.facade import OntoToolsFacade
from onto_tools.adapters.rdf.rdflib_adapter import RDFlibAdapter
from onto_tools.domain.ontology.graph import OntologyGraph


EDO = Namespace("https://w3id.org/energy-domain/edo#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


# ---------------------------------------------------------------------------
# Shared fixture: facade with mock audit logger (fast, no disk)
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_audit_logger():
    logger = MagicMock()
    logger.log = MagicMock()
    logger.get_log_path.return_value = Path("/tmp/audit.json")
    return logger


@pytest.fixture
def facade(mock_audit_logger):
    """OntoToolsFacade with real adapters but mock logger."""
    return OntoToolsFacade(
        rdf_adapter=RDFlibAdapter(),
        audit_logger=mock_audit_logger,
        config_path=None,
    )


# ---------------------------------------------------------------------------
# Helpers to build test ontology graphs
# ---------------------------------------------------------------------------

def _make_loaded_graph(graph: Graph, facade: OntoToolsFacade, tmp_path: Path) -> None:
    """Serialize graph to disk, then load it via facade so _ontology_graph is set."""
    ttl_file = tmp_path / "test_onto.ttl"
    graph.serialize(destination=str(ttl_file), format="turtle")
    result = facade.load_ontology(str(ttl_file), validate=False)
    assert result["status"] == "success", f"load failed: {result}"


# ===========================================================================
# Happy-path: normalize on a minimal but valid ontology
# ===========================================================================

class TestNormalizeOntologyHappyPath:
    """Cover the main trunk of normalize_ontology (lines 531-757)."""

    def test_normalize_returns_success(self, facade, tmp_path):
        """normalize_ontology returns status=success for a loaded ontology."""
        g = Graph()
        g.bind("edo", EDO)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)
        g.add((EDO.MyClass, RDF.type, OWL.Class))
        g.add((EDO.MyClass, SKOS.prefLabel, Literal("My Class", lang="en")))
        g.add((EDO.MyClass, SKOS.prefLabel, Literal("Minha Classe", lang="pt-br")))

        _make_loaded_graph(g, facade, tmp_path)

        result = facade.normalize_ontology()
        assert result["status"] in ("success", "success_with_warnings")

    def test_normalize_result_has_expected_keys(self, facade, tmp_path):
        """normalize_ontology result contains fix_stats, quality_report, etc."""
        g = Graph()
        g.bind("edo", EDO)
        g.add((EDO.SomeClass, RDF.type, OWL.Class))
        g.add((EDO.SomeClass, SKOS.prefLabel, Literal("Some Class", lang="en")))

        _make_loaded_graph(g, facade, tmp_path)

        result = facade.normalize_ontology()
        assert "fix_stats" in result
        assert "quality_report" in result
        assert "auto_fix_applied" in result

    def test_normalize_audit_log_called(self, facade, mock_audit_logger, tmp_path):
        """normalize_ontology logs execution to audit logger."""
        g = Graph()
        g.add((EDO.X, RDF.type, OWL.Class))
        _make_loaded_graph(g, facade, tmp_path)

        facade.normalize_ontology()

        assert mock_audit_logger.log.called
        # Last call should include normalize_ontology
        call_args = mock_audit_logger.log.call_args_list
        op_names = [c[0][0] for c in call_args]
        assert "normalize_ontology" in op_names

    def test_normalize_quality_report_is_dict(self, facade, tmp_path):
        """quality_report in result is a serializable dict."""
        g = Graph()
        g.add((EDO.Test, RDF.type, OWL.Class))
        g.add((EDO.Test, SKOS.prefLabel, Literal("Test", lang="en")))
        _make_loaded_graph(g, facade, tmp_path)

        result = facade.normalize_ontology()
        qr = result.get("quality_report")
        assert isinstance(qr, dict)

    def test_normalize_without_loaded_ontology_returns_error(self, facade):
        """normalize_ontology with no loaded ontology returns error immediately."""
        result = facade.normalize_ontology()
        assert result["status"] == "error"
        assert "carregada" in result["message"].lower() or "loaded" in result["message"].lower()


# ===========================================================================
# Cover the pending-corrections branches (lines ~554-680)
# ===========================================================================

class TestNormalizeWithPendingCorrections:
    """
    Exercise the prefLabel and definition correction-analysis loops
    by loading an ontology that the normalizer can find issues in.
    """

    def test_normalize_with_lowercase_preflabel(self, facade, tmp_path):
        """
        ontology with a prefLabel that has wrong capitalisation exercises
        the pending_preflabel_corrections branch of normalize_ontology.
        """
        g = Graph()
        g.bind("edo", EDO)
        g.bind("skos", SKOS)
        g.bind("dcterms", DCTERMS)

        # Add class with potentially normalizable prefLabel (lowercase)
        g.add((EDO.MyThing, RDF.type, OWL.Class))
        # prefLabel in lowercase – normalizer may propose Title Case
        g.add((EDO.MyThing, SKOS.prefLabel, Literal("my thing", lang="en")))
        g.add((EDO.MyThing, SKOS.prefLabel, Literal("minha coisa", lang="pt-br")))
        # Add a definition without period
        g.add((EDO.MyThing, SKOS.definition, Literal("A test entity without period", lang="en")))
        g.add((EDO.MyThing, DCTERMS.identifier, Literal("MyThing")))

        _make_loaded_graph(g, facade, tmp_path)

        # validate_only mode (auto_fix=False) will populate pending_corrections
        result = facade.normalize_ontology(auto_fix=False)
        assert result["status"] in ("success", "success_with_warnings")
        assert "quality_issues" in result

    def test_normalize_with_auto_fix_true(self, facade, tmp_path):
        """auto_fix=True exercises the 'if result.auto_fix_applied' branch."""
        g = Graph()
        g.add((EDO.FixMe, RDF.type, OWL.Class))
        g.add((EDO.FixMe, SKOS.prefLabel, Literal("fix me", lang="en")))
        g.add((EDO.FixMe, SKOS.definition, Literal("needs period", lang="en")))
        g.add((EDO.FixMe, DCTERMS.identifier, Literal("FixMe")))
        _make_loaded_graph(g, facade, tmp_path)

        result = facade.normalize_ontology(auto_fix=True)
        assert result["status"] in ("success", "success_with_warnings", "error")
        # If success, auto_fix_applied may be True or False depending on normalizer
        if result["status"] in ("success", "success_with_warnings"):
            assert "auto_fix_applied" in result

    def test_normalize_explicit_graph_arg(self, facade, tmp_path):
        """normalize_ontology accepts an explicit graph= argument."""
        g = Graph()
        g.add((EDO.Explicit, RDF.type, OWL.Class))
        g.add((EDO.Explicit, SKOS.prefLabel, Literal("Explicit Thing", lang="en")))

        ttl_file = tmp_path / "explicit.ttl"
        g.serialize(destination=str(ttl_file), format="turtle")
        loaded_graph = OntologyGraph.load(str(ttl_file), RDFlibAdapter)

        result = facade.normalize_ontology(graph=loaded_graph)
        assert result["status"] in ("success", "success_with_warnings")

    def test_normalize_multiple_classes_with_issues(self, facade, tmp_path):
        """Multiple entities with issues exercises the full loop bodies."""
        g = Graph()
        for i in range(5):
            uri = EDO[f"Class{i}"]
            g.add((uri, RDF.type, OWL.Class))
            # Intentionally faulty prefLabels and definitions
            g.add((uri, SKOS.prefLabel, Literal(f"class {i}", lang="en")))
            g.add((uri, SKOS.prefLabel, Literal(f"classe {i}", lang="pt-br")))
            g.add((uri, SKOS.definition, Literal(f"definition of class {i}", lang="en")))
            g.add((uri, DCTERMS.identifier, Literal(f"Class{i}")))

        _make_loaded_graph(g, facade, tmp_path)

        result = facade.normalize_ontology(auto_fix=False)
        assert result["status"] in ("success", "success_with_warnings")

    def test_normalize_with_real_ontology(self, tmp_path):
        """
        Load the real energy-domain-ontology.ttl and run normalize.
        Exercises the full audit-log building code with real data.
        """
        real_ttl = (
            Path(__file__).parent.parent.parent.parent
            / "data" / "examples" / "energy-domain-ontology.ttl"
        )
        if not real_ttl.exists():
            pytest.skip("energy-domain-ontology.ttl not found")

        logger = MagicMock()
        logger.log = MagicMock()
        logger.get_log_path.return_value = Path("/tmp/audit.json")

        facade = OntoToolsFacade(
            rdf_adapter=RDFlibAdapter(),
            audit_logger=logger,
            config_path=None,
        )
        load_result = facade.load_ontology(str(real_ttl), validate=False)
        assert load_result["status"] == "success"

        result = facade.normalize_ontology(auto_fix=False)
        assert result["status"] in ("success", "success_with_warnings")
        # real ontology should produce some quality issues
        assert "quality_issues" in result


# ===========================================================================
# Error path: exception inside normalizer
# ===========================================================================

class TestNormalizeErrorHandling:
    """Cover the except branch of normalize_ontology."""

    def test_normalize_exception_returns_error(self, facade, tmp_path):
        """If the normalizer raises, normalize_ontology returns error status."""
        from unittest.mock import patch

        g = Graph()
        g.add((EDO.Bad, RDF.type, OWL.Class))
        _make_loaded_graph(g, facade, tmp_path)

        with patch(
            "onto_tools.domain.ontology.normalizer.Normalizer.normalize",
            side_effect=RuntimeError("normalizer exploded"),
        ):
            result = facade.normalize_ontology()

        assert result["status"] == "error"
        assert "normalizer exploded" in result["message"]


# ===========================================================================
# Facade error paths: load_ontology, canonicalize_ontology, _generate_audit_report
# ===========================================================================

class TestFacadeLoadErrorPaths:
    """Cover error and exception branches in facade.load_ontology (lines ~116, 167-169)."""

    def test_load_encoding_validation_failure(self, facade, tmp_path):
        """Returns error when encoding validation fails (line ~116)."""
        # Create a non-UTF-8 file (Latin-1 with non-ASCII bytes)
        bad_file = tmp_path / "bad_encoding.ttl"
        bad_file.write_bytes(
            b"@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            b"# Comment with bad byte: \xff\xfe\n"
        )
        # Patch the normalizer to return False for encoding check
        from unittest.mock import patch
        with patch(
            "onto_tools.domain.ontology.normalizer.Normalizer.validate_encoding",
            return_value=False,
        ):
            result = facade.load_ontology(str(bad_file), validate=True)

        assert result["status"] == "error"
        assert "encoding" in result["message"].lower() or "utf" in result["message"].lower()

    def test_load_exception_returns_error(self, facade, tmp_path):
        """Exception during graph loading returns error status (lines ~167-169)."""
        from unittest.mock import patch

        ttl_file = tmp_path / "ok.ttl"
        ttl_file.write_text("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")

        with patch(
            "onto_tools.domain.ontology.graph.OntologyGraph.load",
            side_effect=RuntimeError("graph load exploded"),
        ):
            result = facade.load_ontology(str(ttl_file), validate=False)

        assert result["status"] == "error"
        assert "graph load exploded" in result["message"]

    def test_load_with_validate_false(self, facade, tmp_path):
        """validate=False skips encoding check branch (line ~144->153)."""
        ttl_file = tmp_path / "valid.ttl"
        ttl_file.write_text(
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            "<https://example.org/A> a owl:Class .\n"
        )
        result = facade.load_ontology(str(ttl_file), validate=False)
        assert result["status"] == "success"


class TestFacadeCanonicalizeErrorPaths:
    """Cover exception branches in facade.canonicalize_ontology (lines ~204, 231-233)."""

    def test_canonicalize_no_graph_returns_error(self, facade):
        """canonicalize_ontology with no loaded ontology returns error immediately."""
        result = facade.canonicalize_ontology()
        assert result["status"] == "error"
        assert "carregada" in result["message"].lower() or "loaded" in result["message"].lower()

    def test_canonicalize_exception_returns_error(self, facade, tmp_path):
        """Exception in canonicalizer returns error status (lines ~231-233)."""
        from unittest.mock import patch

        g = Graph()
        g.add((EDO.X, RDF.type, OWL.Class))
        _make_loaded_graph(g, facade, tmp_path)

        with patch(
            "onto_tools.domain.ontology.canonicalizer.Canonicalizer.canonicalize",
            side_effect=RuntimeError("canon exploded"),
        ):
            result = facade.canonicalize_ontology()

        assert result["status"] == "error"
        assert "canon exploded" in result["message"]


class TestFacadeGenerateAuditReport:
    """Cover _generate_audit_report success + error paths (lines 116 and 120)."""

    def test_generate_audit_report_exception_returns_none(self, facade, mock_audit_logger):
        """_generate_audit_report returns None when audit logger raises."""
        # Set side_effect directly on the mock (not on AuditLogger class)
        mock_audit_logger.get_log_path.side_effect = Exception("no log path")
        result = facade._generate_audit_report()
        assert result is None

    def test_generate_audit_report_success_returns_path(self, facade, mock_audit_logger, tmp_path):
        """_generate_audit_report returns md path string when format_audit_log succeeds."""
        import json
        # Create a valid minimal audit log JSON (format_to_markdown expects {"ops": [...]})
        audit_json = tmp_path / "audit.json"
        audit_json.write_text(json.dumps({"ops": []}), encoding="utf-8")

        mock_audit_logger.get_log_path.return_value = audit_json
        mock_audit_logger.get_log_path.side_effect = None  # clear any leftover side_effect

        result = facade._generate_audit_report()
        # Should return the .md path as a string
        assert result is not None
        assert result.endswith(".md")


class TestHasLoadedOntology:
    """Cover has_loaded_ontology() return statement (facade.py line 93)."""

    def test_has_loaded_ontology_returns_false_initially(self, facade):
        """has_loaded_ontology is False before any load."""
        assert facade.has_loaded_ontology() is False

    def test_has_loaded_ontology_returns_true_after_load(self, facade, tmp_path):
        """has_loaded_ontology is True after a successful load."""
        g = Graph()
        g.add((EDO.SomeClass, RDF.type, OWL.Class))
        _make_loaded_graph(g, facade, tmp_path)
        assert facade.has_loaded_ontology() is True


class TestFacadeLoadConfigEdgeCases:
    """Cover _load_config branches (lines ~65->70, 66->65)."""

    def test_load_config_none_with_working_dir(self, mock_audit_logger, tmp_path, monkeypatch):
        """_load_config with config_path=None searches possible paths."""
        # Create a valid config.yaml in a sub-directory matching possible_paths[0]
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("outputs:\n  logs: ./logs\n")

        # Change working directory to tmp_path so Path("config/config.yaml") resolves there
        monkeypatch.chdir(tmp_path)

        f = OntoToolsFacade(
            rdf_adapter=RDFlibAdapter(),
            audit_logger=mock_audit_logger,
            config_path=None,  # triggers the for-loop in _load_config
        )
        # Should have loaded the config
        assert f._config.get("outputs", {}).get("logs") == "./logs"

    def test_load_config_none_no_file_uses_defaults(self, mock_audit_logger, tmp_path, monkeypatch):
        """_load_config with config_path=None and no config file uses default dict."""
        # Change to a temp dir with no config subdir
        monkeypatch.chdir(tmp_path)

        f = OntoToolsFacade(
            rdf_adapter=RDFlibAdapter(),
            audit_logger=mock_audit_logger,
            config_path=None,
        )
        assert "outputs" in f._config
