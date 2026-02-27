"""
Integration tests for verification module.

Tests the complete verification workflow with real ontology files.
"""
import json
from pathlib import Path

import pytest
from rdflib import Graph, Namespace

from onto_tools.application.verification import (
    sha256_file,
    compare_isomorphism,
    check_idempotency,
    RunManifest,
    write_manifest_atomic,
    EvidenceWriter
)


EX = Namespace("http://example.org/")


class TestVerificationIntegration:
    """Integration tests for complete verification workflow."""
    
    @pytest.fixture
    def sample_ontology(self, tmp_path: Path) -> Path:
        """Create a sample ontology file."""
        ontology_content = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/> .

ex:Ontology rdf:type owl:Ontology ;
    rdfs:label "Test Ontology" .

ex:Person rdf:type owl:Class ;
    rdfs:label "Person"@en ;
    rdfs:comment "A human being" .

ex:Organization rdf:type owl:Class ;
    rdfs:label "Organization"@en .

ex:name rdf:type owl:DatatypeProperty ;
    rdfs:domain ex:Person ;
    rdfs:range xsd:string .

ex:worksFor rdf:type owl:ObjectProperty ;
    rdfs:domain ex:Person ;
    rdfs:range ex:Organization .

ex:John rdf:type ex:Person ;
    ex:name "John Doe" ;
    ex:worksFor ex:Acme .

ex:Acme rdf:type ex:Organization ;
    rdfs:label "Acme Corp" .
"""
        ontology_path = tmp_path / "sample_ontology.ttl"
        ontology_path.write_text(ontology_content)
        return ontology_path
    
    def test_full_verification_workflow(self, tmp_path: Path, sample_ontology: Path):
        """Test complete verification workflow."""
        # Step 1: Hash input
        input_hash = sha256_file(sample_ontology)
        assert len(input_hash) == 64
        
        # Step 2: Create output (simple copy for this test)
        output_path = tmp_path / "output.ttl"
        output_path.write_text(sample_ontology.read_text())
        
        # Step 3: Verify isomorphism
        iso_report = compare_isomorphism(sample_ontology, output_path)
        assert iso_report.are_isomorphic is True
        
        # Step 4: Create manifest
        manifest = RunManifest.create(command="test_workflow")
        manifest.add_input(sample_ontology)
        manifest.add_output(output_path, artifact_type="processed_ontology")
        manifest.add_verification("isomorphism", iso_report.are_isomorphic, {
            "input_triples": iso_report.graph_a_triple_count,
            "output_triples": iso_report.graph_b_triple_count
        })
        manifest.set_duration(0.5)
        
        # Step 5: Write manifest
        manifest_path = tmp_path / "run_manifest.json"
        write_manifest_atomic(manifest, manifest_path)
        
        assert manifest_path.exists()
        
        # Verify manifest content
        with open(manifest_path, "r") as f:
            data = json.load(f)
        
        assert data["command"] == "test_workflow"
        assert len(data["inputs"]) == 1
        assert len(data["outputs"]) == 1
        assert len(data["verifications"]) == 1
        assert data["verifications"][0]["passed"] is True
    
    def test_evidence_bundle_creation(self, tmp_path: Path, sample_ontology: Path):
        """Test creating complete evidence bundle."""
        evidence_dir = tmp_path / "evidence"
        writer = EvidenceWriter(evidence_dir, run_id="test_bundle")
        
        # Write manifest
        manifest = RunManifest.create(command="test")
        manifest.add_input(sample_ontology)
        writer.write_manifest(manifest)
        
        # Copy artifact
        writer.copy_artifact(sample_ontology, "ontology_copy.ttl")
        
        # Write verification report
        iso_report = compare_isomorphism(sample_ontology, sample_ontology)
        writer.write_report("isomorphism", iso_report.to_dict())
        
        # Finalize
        bundle = writer.finalize(summary={
            "workflow": "test",
            "status": "success"
        })
        
        # Verify structure
        assert (evidence_dir / "run_manifest.json").exists()
        assert (evidence_dir / "artifacts" / "ontology_copy.ttl").exists()
        assert (evidence_dir / "reports" / "isomorphism_report.json").exists()
        assert (evidence_dir / "evidence_index.json").exists()
        
        # Verify index content
        index_path = evidence_dir / "evidence_index.json"
        with open(index_path, "r") as f:
            index = json.load(f)
        
        assert index["bundle_id"] == "test_bundle"
        assert index["summary"]["status"] == "success"
        assert len(index["files"]) >= 3
    
    def test_idempotency_with_rdf_serialization(self, tmp_path: Path, sample_ontology: Path):
        """Test idempotency with RDF serialization transform."""
        
        def rdf_serialize_transform(input_path: Path, output_path: Path) -> None:
            """Load and re-serialize RDF."""
            g = Graph()
            g.parse(str(input_path), format="turtle")
            g.serialize(destination=str(output_path), format="turtle")
        
        report = check_idempotency(sample_ontology, rdf_serialize_transform)
        
        # RDF serialization should be idempotent (semantically)
        assert report.is_idempotent is True
    
    def test_multiple_verification_checks(self, tmp_path: Path, sample_ontology: Path):
        """Test multiple verification checks on same file."""
        # Create modified version
        modified_path = tmp_path / "modified.ttl"
        g = Graph()
        g.parse(str(sample_ontology), format="turtle")
        
        # Add a triple
        g.add((EX.NewPerson, EX.name, EX.value))
        g.serialize(destination=str(modified_path), format="turtle")
        
        # Check isomorphism (should fail)
        iso_report = compare_isomorphism(sample_ontology, modified_path)
        assert iso_report.are_isomorphic is False
        assert iso_report.triples_only_in_b > 0
        
        # Hashes should differ
        original_hash = sha256_file(sample_ontology)
        modified_hash = sha256_file(modified_path)
        assert original_hash != modified_hash
    
    def test_hash_determinism(self, tmp_path: Path, sample_ontology: Path):
        """Test that hashing is deterministic across multiple calls."""
        hashes = [sha256_file(sample_ontology) for _ in range(10)]
        
        # All hashes should be identical
        assert len(set(hashes)) == 1
    
    def test_manifest_with_all_verification_types(self, tmp_path: Path, sample_ontology: Path):
        """Test manifest with all verification types."""
        manifest = RunManifest.create(command="comprehensive_test")
        
        # Add verifications
        manifest.add_verification("hash", True, {
            "algorithm": "SHA256",
            "hash": sha256_file(sample_ontology)
        })
        
        iso_report = compare_isomorphism(sample_ontology, sample_ontology)
        manifest.add_verification("isomorphism", iso_report.are_isomorphic, {
            "triple_count": iso_report.graph_a_triple_count
        })
        
        def identity(inp, out):
            import shutil
            shutil.copy2(inp, out)
        
        idemp_report = check_idempotency(sample_ontology, identity)
        manifest.add_verification("idempotency", idemp_report.is_idempotent, {
            "hashes_match": idemp_report.hashes_match
        })
        
        # Verify all checks passed
        for v in manifest.verifications:
            assert v.passed is True
        
        # Write and read back
        manifest_path = tmp_path / "comprehensive.json"
        write_manifest_atomic(manifest, manifest_path)
        
        with open(manifest_path, "r") as f:
            data = json.load(f)
        
        assert len(data["verifications"]) == 3
        verification_types = {v["check_type"] for v in data["verifications"]}
        assert verification_types == {"hash", "isomorphism", "idempotency"}


class TestVerificationWithRealOntologies:
    """Tests using realistic ontology patterns."""
    
    @pytest.fixture
    def owl_ontology(self, tmp_path: Path) -> Path:
        """Create OWL ontology with various constructs."""
        content = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix : <http://example.org/onto#> .

:Ontology rdf:type owl:Ontology ;
    owl:versionInfo "1.0.0" .

# Classes
:Building rdf:type owl:Class ;
    rdfs:subClassOf owl:Thing ;
    rdfs:label "Building"@en, "Edificio"@es .

:Floor rdf:type owl:Class ;
    rdfs:subClassOf :BuildingPart .

:BuildingPart rdf:type owl:Class .

# Object Properties
:hasFloor rdf:type owl:ObjectProperty ;
    rdfs:domain :Building ;
    rdfs:range :Floor ;
    owl:inverseOf :isFloorOf .

:isFloorOf rdf:type owl:ObjectProperty ;
    rdfs:domain :Floor ;
    rdfs:range :Building .

# Data Properties
:floorNumber rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
    rdfs:domain :Floor ;
    rdfs:range xsd:integer .

# Individuals
:Building1 rdf:type :Building ;
    rdfs:label "Main Building" ;
    :hasFloor :Floor1, :Floor2 .

:Floor1 rdf:type :Floor ;
    :floorNumber 1 .

:Floor2 rdf:type :Floor ;
    :floorNumber 2 .
"""
        path = tmp_path / "owl_ontology.ttl"
        path.write_text(content)
        return path
    
    def test_owl_ontology_verification(self, tmp_path: Path, owl_ontology: Path):
        """Test verification with OWL ontology."""
        # Hash
        file_hash = sha256_file(owl_ontology)
        assert len(file_hash) == 64
        
        # Self-isomorphism
        iso_report = compare_isomorphism(owl_ontology, owl_ontology)
        assert iso_report.are_isomorphic is True
        assert iso_report.graph_a_triple_count > 10  # Should have many triples
    
    def test_blank_node_handling(self, tmp_path: Path):
        """Test that blank nodes are handled correctly in isomorphism."""
        # Create two files with blank nodes
        ttl_a = """
@prefix ex: <http://example.org/> .

ex:Subject ex:hasPart [
    ex:name "Part A" ;
    ex:value 42
] .
"""
        ttl_b = """
@prefix ex: <http://example.org/> .

ex:Subject ex:hasPart [
    ex:value 42 ;
    ex:name "Part A"
] .
"""
        file_a = tmp_path / "a.ttl"
        file_b = tmp_path / "b.ttl"
        
        file_a.write_text(ttl_a)
        file_b.write_text(ttl_b)
        
        # Should be isomorphic despite blank node ordering
        iso_report = compare_isomorphism(file_a, file_b)
        assert iso_report.are_isomorphic is True
