# Extraction policy (v2.3)

## Operating mode

The default is `strict-statement-plus`: retain formal statements and source-designated examples, counterexamples, and remarks; exclude proofs and free explanatory prose. The core remains strict-statement while the three user-required block types are mandatory.

## Required block taxonomy

| Class | Typical labels or signals | Treatment |
|---|---|---|
| definition | Definition, 定义, terminology introduced by “is called” | Include complete definition and necessary notation. |
| axiom/notation | Axiom, Convention, Notation, 公理, 约定, 记号 | Include. |
| proposition family | Proposition, Lemma, Theorem, Corollary, 命题, 引理, 定理, 推论 | Include statement only. |
| property/criterion | Property, Test, Criterion, identity, law, 性质, 判别法, 恒等式 | Include assumptions and conclusion. |
| key formula | Displayed or inline formula stating a reusable relation | Include with immediately necessary conditions. |
| construction | Named or structurally important construction | Include defining steps and stated properties, not proof. |
| example | Example, Examples, 例 | Include mathematical setup and result. |
| counterexample | Counterexample, 反例, or example explicitly disproving a converse | Include. |
| remark | Remark, Note, 评注, 注 | Include mathematical content. |

Do not assume every numbered item is required or every required item is numbered. Build both numbered-item and unnumbered-candidate indexes. The inventory is the declared set of source containers in the verified slice; ordinary selfcheck validates that declaration and its consistency, and must not silently derive a hidden expected set from wording signals. A benchmark may separately provide an explicit or hidden coverage manifest, but coverage scoring is distinct from structural selfcheck.

## Container boundaries and source positions

Every candidate has a deterministic container boundary. `source_start_line` means the marker line, not the first semantic content line:

- ATX heading: the `# ...` line;
- Setext heading: the title text line (never the underline);
- fenced code: the opening fence;
- `> [!info]` or another callout: the first callout marker line;
- HTML table: `<table ...>` or, when absent, the first `<tr>`;
- ordinary paragraph, list, or formula without a container: its first non-empty line.

`source_end_line` includes the closing fence, final callout line, `</table>`, or final content line. Optional `content_start_line` and `content_end_line` identify semantic content after container syntax is removed. Record these values under `source_position`; `marker_start_line` must equal `source_start_line`. If a parser cannot identify a marker, use the first non-empty line and record `container_type="other"` plus the reason. Never change the start-line convention between candidates.

Canonical `container_type` values are `heading`, `paragraph`, `display_formula`, `fenced_code`, `callout`, `html_table`, `list`, and `other`.

## Unlabeled prose decision rule

An unlabeled paragraph is not a property merely because it contains a true
mathematical sentence. Classify it with this ordered test and record the test
result in `audit.json.extraction_judgments`:

1. **Property/criterion:** include when the paragraph has a reusable
   hypothesis-to-conclusion form, an equality/inequality/law, or an explicit
   necessary/sufficient test that can be cited independently of the surrounding
   motivation. Record the hypotheses and conclusion in the basis.
2. **Remark:** include when it comments on scope, variants, naming, edge cases,
   notation, or the relationship between already-stated results, without
   introducing a new proof step. A remark may be unnumbered.
3. **Example/counterexample:** include only when the source presents concrete
   data or an object as an instance, and states what it demonstrates or whether
   it fails a property. A bare object mentioned as intuition is not enough.
4. **Explanation:** exclude motivational, historical, geometric, or pedagogical
   prose whose purpose is to help understanding rather than state a reusable
   fact. An unlabeled paragraph that cannot pass tests 1–3 is explanation by
   default, not an inferred property.

When two readings remain plausible, use `decision="split"` or `classification`
`"mixed"`, list the alternative classification and evidence, and stop for
human review if the choice changes recall. Never let an unlabeled fact enter the
knowledge list without a recorded basis.

## Examples containing derivations

The `example` label makes the setup and stated result mandatory; it does not
turn every calculation into retained knowledge. Split mixed blocks into
`source_subspans` (or linked candidate records): retain `setup` and the final
source-stated `result`, exclude `derivation`, `verification`, and proof-like
work unless the case explicitly opts in. If the result appears only at the end
of a calculation, retain that terminal assertion and record the omitted span.
Overlapping parent/child spans are valid in the audit when a parent example is
kept for recall and a derivation child is excluded for contamination. For mixed
content on one physical line, add 1-based half-open Unicode code-point columns
(`start_column`, `end_column`) to each `source_subspan`; the end column is
exclusive. Different roles may overlap, but every overlap needs a note and an
explicit include/exclude decision. The reader-facing list must contain no proof
or derivation text.

## Exclusions

Exclude:

- proof blocks, proof sketches, demonstrations, and derivations;
- motivational, historical, pedagogical, or intuitive explanation not needed to state a retained block;
- chapter summaries that merely repeat earlier statements, unless explicitly requested;
- exercises from the main knowledge list;
- knowledge imported from other chapters, editions, memory, or general knowledge.

Words such as “therefore” are not automatically proof markers. Classify by function and structure. Conversely, an unlabeled derivation remains proof and must be excluded.

## Range-first boundary protocol

Do not inject the full textbook into model context to discover a boundary.

1. Run from the benchmark harness or skill directory: `python -X utf8 ../scripts/scope_markdown.py index --source <book.md>`. From the skill directory, use `python -X utf8 scripts/scope_markdown.py ...`. The program scans locally but returns only headings, levels, line numbers, source hash, and line count.
2. If duplicate or unclear titles need minimal context, rerun with `--preview-chars 32` or another value no greater than 160. Do not print the full file or every line prefix.
3. Let the model select the exact requested start heading from compact evidence. Normally the end is the next heading at the same or higher level; use an explicit end-before heading for a nonstandard requested range.
4. Run `extract` with chosen start and output paths. Record source hash, start/end headings, line range, selection method, slice hash, and slice line count.
5. Inject and read only the generated slice for inventory and extraction. Account separately for appendices, examples, remarks, and exercises inside it.
6. Cross-check slice first/last headings and one boundary fact against the compact index. Never use source memory as evidence.

When the boundary evidence is a verified pair of line numbers rather than a
heading, run `extract --start-line N --end-line M`. The range is 1-based and
inclusive; `--start-line` requires `--end-line`, and the start line must not be
inside a fenced code block. A heading start can be combined with `--end-line`.
The manifest records `selection_method="explicit-line-range"` and whether
either boundary was resolved from a heading.

The tool supports ATX and Setext headings and ignores headings inside fenced code. Each index record carries `kind` (atx/setext) and `matched_by` (strict/loose). An ATX heading whose marker is not followed by a space (e.g. `#第1章`) is invisible to strict mode; run `index --loose-atx` to surface it, treat `matched_by=loose` records as lower-confidence evidence, and prefer a line-based slice. Bare chapter text (`第三章 极限`) is never promoted to a heading: run `scope_markdown.py probe --pattern <chapter-marker-regex>` to get its line numbers, then use `extract --start-line N --end-line M`. Record the fallback and require two independent boundary cues. If ambiguity remains, stop.

A Setext heading whose source line ends with sentence punctuation or contains multiple sentences is tagged `suspicious=true` (a `---` separator under prose is a common false heading). `extract` prints a warning to stderr when such a heading is used as a boundary but still applies the resolved rule; treat the warning as a cue to double-check the boundary, not as an automatic failure.

`--start-heading` and `--end-before-heading` tolerate a leading `#{1,6}` marker and surrounding whitespace (`"## 第一章 数列"`); the index text remains the canonical identity recorded in the manifest.

For unfamiliar or possibly damaged sources, run `scope_markdown.py precheck --source <book.md>` first. It only warns (never modifies): heading level jumps, numbering gaps within the same parent (headings only), bare chapter-like lines, directory-like table-of-contents rows, U+FFFD replacement characters, unclosed fences, literal `?` placeholders, common `fi`/`ffi` ligature-loss tokens, and possible references to numbered items whose labels are absent from the heading index. Use `--scope whole|slice|both`; `both` reports whole-source health and the verified slice separately. Numbering-gap analysis ignores fenced code, callouts, HTML tables, cross-section references, and directory rows. `possible_numbering_label_loss` is a low-confidence prompt for nearby inspection, never proof that a label was lost or permission to invent one. Whole-source warnings are advisory; slice warnings drive boundary review and ledger entries. Each warning carries scope and confidence, and adopted warning types are copied into `audit.json.source_artifacts.precheck_warning_types`.

Line numbers are evidence but not stable identity. Always record heading text, level, occurrence, source hash, and slice hash.

## Fidelity rules

- Same-language output: copy wording rather than paraphrasing.
- Requested translation: preserve logical strength, quantifiers, hypotheses, exceptions, terminology, and formula structure; never silently summarize.
- Preserve source numbering and order. Never renumber to hide gaps.
- When source order conflicts with numerical order, source order is the
  authoritative presentation order. Preserve each original label verbatim and
  add an `order_artifact` entry to `audit.json.source_artifacts` describing the
  conflict (source lines, labels, and the chosen order). Never sort by number.
- Preserve LaTeX commands, delimiters, indices, signs, inequality direction, domains, and alignment where practical.
- Preserve the relation between prose and formula. A formula without required conditions is incomplete.
- Do not silently correct the textbook. Flag suspected source errors separately.
- For damaged conversions, use the standard `source_artifacts` ledger. A
  restoration is allowed only when the intended token is uniquely determined;
  otherwise preserve the literal source token and flag it. Repeated identical
  damage is recorded as one `granularity="pattern"` entry with `pattern`,
  `count`, representative original text, occurrence lines or ranges, action,
  and evidence basis. Irregular or high-risk damage uses `granularity="item"`.
  Record the original text, affected source line(s) or ranges, action, restored
  text (if any), and evidence basis for each item or pattern-level judgment.
- If bilingual terminology is requested, add the source term at first occurrence only unless the exemplar requires more.

## Reader-facing structure

`knowledge.md` mirrors the verified source hierarchy rather than inventing a
new taxonomy. Use the range note first, then the real source chapter heading,
real subsection headings (for example 2A/2B/2C), and the K blocks that begin
under each subsection. K headings identify retained blocks but do not replace
source headings. Do not add headings such as “Summary”, “Explanation”, or
model-created categories. Place a block that crosses a subsection boundary
under the subsection containing its `source_start_line`, and record the
cross-boundary span in audit. The checker compares the retained source-heading
sequence and K order separately; it does not require excluded source prose to
appear in the reader-facing file.

### Bilingual first-occurrence protocol

This protocol is a format-level traceability check for translated output; it
does not decide whether a translation is semantically ideal.  "First
occurrence" is counted only within the knowledge list produced from the
verified slice, in source order.  Excluded proof, explanation, and exercise
blocks do not advance the count and do not require a bilingual pair.  A term
table should be derived first from a terminology/index section in the source;
when no such section exists, the extractor may select terms from the source
and must record that judgment (including the selection basis and any
uncertainty) in `audit.json.bilingual_terms`. The term table should contain
only terms that occur in retained blocks; an absent term cannot have a
verifiable first occurrence.

Use `中文（English）` as the canonical form, with the target-language term
first and full-width parentheses.  The validator may accept half-width
parentheses and the reverse `English（中文）` orientation as explicit
format-level alternatives.  It checks that the pair's opening parenthesis is
within eight characters of the configured term on the same knowledge-list
line; the extractor should not alternate forms without a documented reason.
Record the target term, source spelling,
optional knowledge line, and optional `block_id` in the audit table.  The
recorded line is the line in the reader-facing knowledge list, not a line from
an excluded source block.  Only the first occurrence requires the pair; later
occurrences must remain faithful to the source and are not required to repeat
the English term.

## Two-pass extraction audit

The inventory pass records at least `block_id`, source label, class, source position, include/exclude decision, and exclusion reason. The readback pass verifies:

1. every included inventory item appears once;
2. no excluded proof or exercise leaked into the main list;
3. numbering and order match source;
4. examples, counterexamples, and remarks were not skipped;
5. formulas retain mathematical tokens and conditions;
6. all output claims are supported inside the verified slice;
7. required files exist, are nonempty, and read back as UTF-8.

File existence alone is not completion evidence.
