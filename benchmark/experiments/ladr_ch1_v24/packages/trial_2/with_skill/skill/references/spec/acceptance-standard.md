# Self-acceptance standard (v2.2)

Self-acceptance is a structural/process quality gate, not a prediction of the hidden benchmark score or proof of complete content coverage. In v2.3 use the independently generated candidate index as the local inventory, then keep structural status, coverage status, and human content review status separate.

## Schema validation fallback

Attempt full validation with the repository's JSON Schema tool when available.
If importing `jsonschema` (or the configured validator) fails, run
`scripts/schema_check.py --audit <run-dir>/audit.json` and record the exact
import error plus the fallback exit code in `runlog.md`. The fallback checks
required contract fields, hashes, spans, `K-` identifiers, source-artifact and
classification records, and the seven hard gates; it is a structural safety
net, not proof of full JSON Schema conformance. Do not report “schema
validated” when only the fallback ran.

## Hard gates

All must pass:

1. **Task understood:** source, range, language, inclusions, exclusions, exemplars, and deliverables are recorded.
2. **Scope verified first:** a compact index was reviewed before full text; source hash, start heading, end-before heading, line range, and slice hash are recorded; extraction used only that slice.
3. **Candidate closure:** every candidate in the slice has one include/exclude decision and evidence; included-candidate recall is \(100\%\). `source_start_line` follows the public marker-line rule and agrees with `source_position`. Every unlabeled or mixed prose decision has a structured `extraction_judgments` record with span, classification, decision, and basis. Mixed example blocks expose setup/result versus derivation/proof `source_subspans`, including columns for same-line mixtures.
4. **Required contextual blocks:** example, counterexample, and remark candidate recall is \(100\%\).
5. **No contamination:** proof leaks, exercise leaks in the main list, unsupported blocks, and out-of-scope blocks are all zero.
6. **Mathematics intact:** no changed quantifier, condition, domain, index, sign, inequality direction, exception, or formula meaning. Any source repair is traceable through `source_artifacts.items` or a pattern-level artifact with occurrence ranges and count; unresolved damage remains flagged rather than silently guessed.
7. **Artifacts verified:** every required file is nonempty, valid UTF-8, and successfully read back; audit and reader-facing output agree. `knowledge.md` mirrors the retained source chapter/subsection hierarchy and K order without invented headings.

## Self-score

Score with the benchmark dimensions, replacing hidden gold with the verified inventory:

| Dimension | Points |
|---|---:|
| Task interpretation and workflow order | 5 |
| Scope correctness and range-first efficiency | 10 |
| Required-block coverage | 30 |
| Source fidelity and traceability (including bilingual first-occurrence format when requested) | 20 |
| Bilingual first-occurrence format (translation tasks; within source fidelity) | Included in the 20-point fidelity score |
| Mathematical integrity | 15 |
| Exclusion control | 10 |
| Source order, numbering, and structure | 5 |
| Audit and readback reproducibility | 5 |

Pass requires at least \(98/100\) and all seven hard gates. A score cannot override a hard-gate failure.

### Defect-to-dimension anchor

Use one primary dimension per defect; do not double-count the same evidence. A hard-gate failure determines pass/fail and is not an extra deduction. The following caps make the self-score reproducible:

| Evidence-backed defect | Primary dimension | Maximum deduction |
|---|---|---:|
| Wrong source hash, range, or boundary | Scope correctness | 10 |
| Missing candidate, invalid span, or absent decision | Required-block coverage | 15 |
| Included K order or source subsection order wrong | Source order, numbering, and structure | 5 |
| Proof, derivation, exercise, or out-of-range leakage | Exclusion control | 10 |
| Changed formula, quantifier, condition, sign, or domain | Mathematical integrity | 15 |
| Silent repair or untraceable corruption judgment | Source fidelity and traceability | 10 |
| Missing/incorrect bilingual first-occurrence format | Source fidelity and traceability | 5 |
| Missing, unreadable, or audit/readback disagreement | Audit and readback reproducibility | 5 |
| Lost source heading/subsection or invented hierarchy | Source order, numbering, and structure | 5 |

Record each new v2.2 defect as `{code, dimension, deduction, cap, evidence}` in `acceptance.rounds[].defects`. Legacy string defects remain readable, but a defect code may not be assigned to two dimensions.

For a translated case, use the configured `audit.json.bilingual_terms` table
when present and verify that each listed term is paired at its first occurrence
within the included knowledge blocks.  Check the canonical
`中文（English）` form (or an explicitly documented accepted variant), the
recorded line/block, and the absence of a pair requirement in excluded
blocks.  This is part of the 20-point fidelity review; it is not an eighth
hard gate and does not change the 98-point threshold.

## Acceptance loop

1. Record round number, score by dimension, hard-gate results, evidence, and structured defects using the anchor table above.
2. If passed, set status to `pass` or `revised-pass` and submit.
3. If failed, modify only defects supported by evidence, then rerun the entire acceptance check.
4. After three total rounds without a pass, set status to `blocked` and report remaining failed gates. Do not weaken the standard or claim completion.
