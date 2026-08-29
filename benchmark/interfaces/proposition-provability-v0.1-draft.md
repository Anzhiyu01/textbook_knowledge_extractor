# Proposition provability provider interface v0.1-draft

## Status

- Provider: not implemented
- Integration: disabled
- Effect on the extraction skill: none
- Effect on the current benchmark score: none

This document reserves a boundary for a future dedicated skill that determines whether a proposition can be proved from one or more knowledge lists. The textbook extractor must not perform that judgment.

## Ownership boundary

The extraction skill owns:

- `knowledge.md`: source-faithful blocks with stable local `block_id` values;
- `audit.json`: source hash, verified scope, candidate decisions, and extraction acceptance evidence.

The future provability skill will own:

- proposition parsing;
- prerequisite-list selection;
- proof-obligation and permitted-primitive definitions;
- dependency closure, minimality, counterfactual checks, and adjudication;
- any proposition-level score or benchmark.

Its output must be separate from `knowledge.md` and `audit.json`. It must never modify the source-faithful list to make a proposition provable.

## Proposed request

```json
{
  "protocol_version": "0.1-draft",
  "proposition": {
    "id": "string",
    "text": "string"
  },
  "knowledge_lists": [
    {
      "list_id": "string",
      "knowledge_file": "path",
      "audit_file": "path",
      "sha256": "64 hex characters",
      "order": 0
    }
  ],
  "policy": "provider-owned policy identifier"
}
```

## Proposed response

```json
{
  "protocol_version": "0.1-draft",
  "proposition_id": "string",
  "status": "provable | partially_supported | not_provable | indeterminate",
  "knowledge_refs": ["list_id:block_id"],
  "missing_obligations": ["string"],
  "evidence_file": "path",
  "provider": {
    "skill": "string",
    "version": "string"
  }
}
```

The status vocabulary and semantics are placeholders until the dedicated skill is designed and independently evaluated.

## Activation requirements

Integration remains disabled until all of the following exist:

1. a separately versioned provability skill;
2. a frozen formal policy defining what counts as provable;
3. independent tests for soundness, prerequisite handling, and false-positive control;
4. a provider output validator;
5. an explicit benchmark decision about whether provider results are reported separately or scored.

Activation must require an explicit case-manifest change. Merely placing this interface file in the workspace must not invoke the provider.
