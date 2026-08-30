# Verified Pitfalls

- Scan converted output for `defnition`, `finite`, `feld`, `fgure`, and `frst` ligature damage before extraction; never silently restore ambiguous text.
- Preserve every digit in `K-{source_start_line:03d}` IDs. Four-digit and longer source lines must not be truncated or replaced by an unrecorded ordinal.
- `knowledge.md` K headings must use the audit marker line, not a label or content line.
- Compare the included candidate set against rendered K blocks; do not infer closure from memory or from a self-declared inventory.
- When `jsonschema` is unavailable, report the dependency-free fallback explicitly; do not call it full schema validation.
- Keep `precheck --mode`, `index --preview-chars`, and `probe --prefix-chars` parameter names exact and verify command help after moves.
- Bilingual first occurrence is checked within rendered included K blocks in source order.
- Pattern-level `source_artifacts` entries must satisfy the same occurrence and evidence requirements as item-level entries.

Lessons are promoted here only when a runlog records a trigger, root cause, evidence, and a successful rerun.
