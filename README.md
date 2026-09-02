# Textbook Extraction Workspace

This repository contains a reusable textbook extraction capability and a paired benchmark.

- `skill/textbook-knowledge-extractor/` contains the reusable v2.4 extraction workflow, references, scope utilities, rendering checks, and legacy audit contract.
- `benchmark/` contains the v2.5 outcome-only paired evaluation protocol, neutral public task files, hidden control data, gold, validators, scorers, and historical development fixtures.
- `scratch/` contains ignored historical materials, backups, notes, and prior outputs.

The paired benchmark gives both experiment conditions byte-identical public prompt, case, source slice, output schema, and scoring protocol. The v2.5 headline score evaluates only the final `knowledge.md` and result-level `audit.json`; process traces and self-reported acceptance do not affect the (100)-point score.

Run repository checks from the root:

```text
python -X utf8 -m unittest discover -s skill/textbook-knowledge-extractor/scripts -p "test_*.py"
python -X utf8 -m unittest discover -s benchmark/scripts -p "test_*.py"
```

LADR Chapter 1 gold remains non-headline while its atomic annotations require human review. Passing structural tests does not override that gate.
