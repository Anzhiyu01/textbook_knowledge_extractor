# Textbook Extraction Workspace v2.3

This repository contains two packages with a one-way dependency:

- `skill/textbook-knowledge-extractor/` is the reusable extraction skill, specification references, lessons, scope tool, candidate discovery tool, and shared output contract.
- `benchmark/` contains the benchmark prompt, scoring protocol, schemas, validators, development cases, gold annotations, and disabled future interfaces.

The benchmark imports the skill's public scripts; the skill never imports benchmark code. v2.3 uses a program-generated candidate index, structured boundary evidence, and explicit mixed-block evidence. Structural selfcheck is not a claim of complete mathematical coverage; hidden gold and human review remain authoritative for content correctness.

Run development checks from `benchmark/`:

```text
python -X utf8 scripts/validate_submission.py --case dev/input/sample_case.json --submission dev/submissions/sample_good
python -X utf8 scripts/score_sample.py --case dev/input/sample_case.json --submission dev/submissions/sample_good
```

Historical materials, old runs, backups, and notes are kept locally under `scratch/`, which is ignored by version control.
