# Command Log - RC_v13_CANON

## Overview

This file documents all commands executed during RC_v13_CANON generation.
All commands were executed via Python API (script `scripts/run_rc13.py`).

---

## FASE 0 - Inventory

### Environment Check
```python
import sys
print(f"Python: {sys.version}")  # 3.12.12

import onto_tools
print(onto_tools.__version__)  # 3.0.0
```

### CLI Discovery
```bash
python -m onto_tools --help
python -m onto_tools verify --help
python -m onto_tools ontology --help
```

---

## FASE 1 - Structure Creation

### Directory Structure
```
RC_v13_CANON/20260227_042545/
├── 00_meta/
├── 10_proofs/
├── 20_runs/
│   ├── run2a_canonicalize/
│   ├── run2b_canonicalize/
│   ├── run3_normalize_canonicalize/
│   └── run4_normalize_canonicalize/
├── 30_gates/
├── 40_tests/
├── 50_qa/
├── 60_reference/
└── 90_legacy/
```

### Input Hash
```python
import hashlib
with open("data/examples/energy-domain-ontology.ttl", "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest().upper()
# Result: A772AE732EF041B951B7AF0C27D4A62A611C09C0DFC0A8D0F2477BF4EEE2A8AE

from rdflib import Graph
g = Graph()
g.parse("data/examples/energy-domain-ontology.ttl", format="turtle")
print(len(g))  # 6803 triples
```

---

## FASE 2 - Canonicalization Runs

### Run 2a
```python
from onto_tools.domain.ontology.canonicalizer import canonicalize_graph
from rdflib import Graph
import hashlib

g = Graph()
g.parse("data/examples/energy-domain-ontology.ttl", format="turtle")
result = canonicalize_graph(g)
canonical_ttl = result.serialize(format="turtle")
sha = hashlib.sha256(canonical_ttl.encode()).hexdigest().upper()
# Result: E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49
```

### Run 2b
```python
# Same as Run 2a (independent execution)
# Result: E1F9622F50AF55FAC807DE0ED64790F234D6057CC42BC5DFD6252BEB9BC1DF49
# Determinism confirmed: Hash_2a == Hash_2b
```

---

## FASE 3 - Normalize + Canonicalize

### Run 3 (validate only)
```python
from onto_tools.domain.ontology.normalizer import Normalizer
normalizer = Normalizer()
result = normalizer.normalize("data/examples/energy-domain-ontology.ttl")
# 1831 total issues detected (260 errors, 1571 warnings)
# auto_fix_applied = False
```

### Run 4 (auto-fix)
```python
# Same as Run 3, with auto_fix=True
# 743 triples modified
# Output SHA256: B28D98AC2A22E4C763BD97EF98A37296FA089D78E681C587C90FE5700D0A498D
```

---

## FASE 4 - Gates

### Isomorphism Check
```python
from onto_tools.application.verification import compare_isomorphism
result = compare_isomorphism(input_graph, canonical_graph)
# Result: True (graphs are isomorphic)
```

### Idempotency Check
```python
from onto_tools.application.verification import check_idempotency
result = check_idempotency(canonical_graph, canonicalize_graph)
# Result: True (f(f(x)) == f(x))
```

---

## FASE 5 - Tests

### Pytest Execution
```bash
python -m pytest tests/1-uc-ontology -v --tb=short --cov=src/onto_tools --cov-report=term-missing --cov-report=json
```

### Results
- Tests: 963 passed
- Coverage: 95.04%
- Duration: 65.43s

---

## Verification

To verify any hash:
```powershell
Get-FileHash -Algorithm SHA256 <filename> | Select-Object Hash
```

---

*Log Generated: 2026-02-27T04:26:57Z*
