"""
Verification Module - Núcleo de verificação para pipeline OntoTools.

Implementa verificações nativas do protocolo descrito no artigo:
- (i) Idempotency: sha256(output) + reapply + byte_equal
- (ii) Semantic preservation: RDF isomorphism
- (iii) Byte-level determinism: multi-run hash comparison
- (iv) Manifest: run_manifest com todas as evidências

K1: Pipeline NORMAL gera verificações nativamente.
K2: RC orquestra (não reimplementa).
"""

from .hasher import sha256_file, sha256_bytes, sha256_string, file_size_bytes
from .isomorphism import compare_isomorphism, compare_graphs, IsomorphismReport
from .idempotency import (
    check_idempotency,
    check_graph_idempotency,
    check_full_idempotency,
    verify_canonicalization_idempotent,
    IdempotencyReport,
    FullIdempotencyReport
)
from .manifest_writer import (
    RunManifest,
    InputArtifact,
    OutputArtifact,
    VerificationResult,
    EnvironmentInfo,
    write_manifest_atomic,
    write_manifest_append,
    read_manifest
)
from .evidence_writer import (
    EvidenceWriter,
    EvidenceFile,
    EvidenceBundle,
    create_rc_evidence_directory
)

__all__ = [
    # Hasher
    "sha256_file",
    "sha256_bytes",
    "sha256_string",
    "file_size_bytes",
    # Isomorphism
    "compare_isomorphism",
    "compare_graphs",
    "IsomorphismReport",
    # Idempotency
    "check_idempotency",
    "check_graph_idempotency",
    "verify_canonicalization_idempotent",
    "IdempotencyReport",
    # Manifest
    "RunManifest",
    "InputArtifact",
    "OutputArtifact",
    "VerificationResult",
    "EnvironmentInfo",
    "write_manifest_atomic",
    "write_manifest_append",
    "read_manifest",
    # Evidence
    "EvidenceWriter",
    "EvidenceFile",
    "EvidenceBundle",
    "create_rc_evidence_directory",
]
