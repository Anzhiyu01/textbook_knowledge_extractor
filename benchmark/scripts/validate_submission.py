#!/usr/bin/env python3
"""Deterministic structural checks for a textbook extraction submission."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

_SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skill" / "textbook-knowledge-extractor" / "scripts"
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))
try:  # Script execution (``python scripts/...``) and package imports alike.
    from bilingual import infer_terms, normalise_terms, validate_bilingual_terms
    from leak_patterns import exercise_leak_matches, proof_leak_matches
    from contract import BLOCK_ID_RE, valid_block_id, ARTIFACT_CATEGORIES, ARTIFACT_ACTIONS
    from scope_markdown import discover_candidates
except ImportError:  # pragma: no cover - only needed when imported as a package
    from .bilingual import infer_terms, normalise_terms, validate_bilingual_terms
    from .leak_patterns import exercise_leak_matches, proof_leak_matches
    from .contract import BLOCK_ID_RE, valid_block_id, ARTIFACT_CATEGORIES, ARTIFACT_ACTIONS

try:
    from scope_markdown import discover_candidates
except ImportError:  # pragma: no cover
    discover_candidates = None


ALLOWED_KINDS = {
    "definition", "axiom", "notation", "proposition", "lemma", "theorem",
    "corollary", "property", "criterion", "formula", "construction", "example",
    "counterexample", "remark", "proof", "explanation", "exercise",
}
REQUIRED_HARD_GATES = {
    "task_understood", "scope_verified_first", "candidate_closure",
    "contextual_block_recall", "no_contamination", "mathematics_intact",
    "artifacts_verified",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--submission", required=True, type=Path)
    parser.add_argument(
        "--require-bilingual",
        "--bilingual",
        dest="require_bilingual",
        action="store_true",
        help=(
            "require each configured (or conservatively inferred) term to be "
            "bilingual at its first occurrence; disabled by default"
        ),
    )
    args = parser.parse_args()
    case_path = args.case.resolve()
    submission = args.submission.resolve()
    errors: list[str] = []

    try:
        case = json.loads(case_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read case: {exc}")
        return 2

    provability = case.get("extensions", {}).get("proposition_provability", {})
    if provability.get("enabled") is not False:
        fail(errors, "this extractor benchmark requires proposition_provability.enabled=false")

    required_files = tuple(case.get("submission_files", ("knowledge.md", "audit.json")))
    if set(required_files) != {"knowledge.md", "audit.json"}:
        fail(errors, "submission_files must contain only knowledge.md and audit.json")
    for name in required_files:
        path = submission / name
        if not path.is_file():
            fail(errors, f"missing {name}")
        elif not path.read_text(encoding="utf-8").strip():
            fail(errors, f"empty {name}")

    source = (case_path.parent / case["source_file"]).resolve()
    if not source.is_file():
        fail(errors, f"missing source {source}")
        source_lines: list[str] = []
    else:
        source_bytes = source.read_bytes()
        actual_hash = hashlib.sha256(source_bytes).hexdigest().upper()
        if actual_hash != case["source_sha256"].upper():
            fail(errors, "source SHA-256 does not match case manifest")
        source_lines = source.read_text(encoding="utf-8").splitlines()

    audit: dict = {}
    audit_path = submission / "audit.json"
    if audit_path.is_file():
        try:
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"audit.json is not valid JSON: {exc}")

    included_ids: set[str] = set()
    if audit:
        if audit.get("case_id") != case["case_id"]:
            fail(errors, "audit case_id mismatch")
        if audit.get("source_sha256", "").upper() != case["source_sha256"].upper():
            fail(errors, "audit source_sha256 mismatch")

        understanding = audit.get("task_understanding", {})
        for key in (
            "source", "target", "output_language", "include_classes",
            "exclude_classes", "deliverables",
        ):
            if not understanding.get(key):
                fail(errors, f"missing task_understanding.{key}")
        if set(understanding.get("deliverables", [])) != set(required_files):
            fail(errors, "task_understanding.deliverables mismatch")

        target = case["target"]
        boundaries = audit.get("boundaries", {})
        scope = audit.get("scope_preprocessing", {})
        if scope.get("index_before_full_read") is not True:
            fail(errors, "scope index was not recorded before full read")
        if scope.get("full_source_opened_before_slice") is not False:
            fail(errors, "full source was opened before the verified slice")
        if not scope.get("tool") or not scope.get("selection_method"):
            fail(errors, "scope tool or selection method missing")
        for key in ("start_heading", "end_before_heading"):
            if boundaries.get(key) != target[key]:
                fail(errors, f"boundary {key} mismatch")
        if audit.get("audit_schema_version") == "2.3":
            evidence = boundaries.get("evidence")
            if not isinstance(evidence, list) or len(evidence) < 2:
                fail(errors, "v2.3 boundaries require at least two evidence records")
            else:
                for item in evidence:
                    if not isinstance(item, dict) or not all(k in item for k in ("kind", "line", "text", "reliability", "relation")):
                        fail(errors, "invalid v2.3 boundary evidence record")
                    elif not isinstance(item.get("line"), int) or not 1 <= item["line"] <= len(source_lines):
                        fail(errors, "v2.3 boundary evidence line outside target")
        if boundaries.get("start_line") != target["expected_start_line"]:
            fail(errors, "boundary start_line mismatch")
        if boundaries.get("end_line") != target["expected_end_line"]:
            fail(errors, "boundary end_line mismatch")

        if source_lines:
            start = target["expected_start_line"]
            end = target["expected_end_line"]
            slice_text = "\n".join(source_lines[start - 1 : end]) + "\n"
            slice_hash = hashlib.sha256(slice_text.encode("utf-8")).hexdigest().upper()
            if scope.get("slice_sha256", "").upper() != slice_hash:
                fail(errors, "scope slice_sha256 mismatch")
            if scope.get("slice_line_count") != end - start + 1:
                fail(errors, "scope slice_line_count mismatch")

        seen: set[str] = set()
        candidates = audit.get("candidates", [])
        if not candidates:
            fail(errors, "candidate inventory is empty")
        for candidate in candidates:
            block_id = candidate.get("block_id", "")
            if block_id in seen:
                fail(errors, f"duplicate block_id {block_id}")
            seen.add(block_id)
            if not valid_block_id(block_id):
                fail(errors, f"invalid block_id {block_id}")
            kind = candidate.get("kind")
            if kind not in ALLOWED_KINDS:
                fail(errors, f"invalid kind for {block_id}: {kind}")
            start = candidate.get("source_start_line", 0)
            end = candidate.get("source_end_line", 0)
            if not isinstance(start, int) or not isinstance(end, int) or start > end:
                fail(errors, f"invalid source span for {block_id}")
            elif source_lines and (start < 1 or end > len(source_lines)):
                fail(errors, f"source span out of file for {block_id}")
            decision = candidate.get("decision")
            if decision not in {"include", "exclude"}:
                fail(errors, f"invalid decision for {block_id}")
            elif decision == "include":
                included_ids.add(block_id)
            if (
                isinstance(start, int)
                and isinstance(end, int)
                and (
                    start < target["expected_start_line"]
                    or end > target["expected_end_line"]
                )
            ):
                fail(errors, f"candidate outside target range: {block_id}")
            if audit.get("audit_schema_version") == "2.2":
                position = candidate.get("source_position")
                if not isinstance(position, dict):
                    fail(errors, f"v2.2 candidate missing source_position: {block_id}")
                elif position.get("marker_start_line") != start:
                    fail(errors, f"source_position marker_start_line mismatch: {block_id}")
                for subspan in candidate.get("source_subspans", []):
                    if not isinstance(subspan, dict):
                        fail(errors, f"invalid source_subspan for {block_id}")
                        continue
                    if "start_column" in subspan or "end_column" in subspan:
                        if not (isinstance(subspan.get("start_column"), int) and isinstance(subspan.get("end_column"), int) and subspan["start_column"] >= 1 and subspan["start_column"] < subspan["end_column"]):
                            fail(errors, f"invalid half-open source_subspan columns for {block_id}")
            if audit.get("audit_schema_version") == "2.3" and candidate.get("mixed") is True:
                for field in ("retained_conclusion_anchor", "excluded_intervals", "formula_token_map", "source_subspans"):
                    if field not in candidate:
                        fail(errors, f"v2.3 mixed candidate missing {field}: {block_id}")

        if audit.get("audit_schema_version") == "2.3" and source_lines:
            generated = discover_candidates(source_lines, target["expected_start_line"], target["expected_end_line"])
            declared = [{k: c.get(k) for k in ("block_id", "source_start_line", "source_end_line", "container_type", "signal", "text_anchor")} for c in candidates if isinstance(c, dict)]
            expected = [{k: row.get(k) for k in ("block_id", "source_start_line", "source_end_line", "container_type", "signal", "text_anchor")} for row in generated]
            if declared != expected:
                fail(errors, "v2.3 candidates do not exactly match independently generated candidate index")
            discovery = audit.get("candidate_discovery", {})
            if not isinstance(discovery, dict) or not isinstance(discovery.get("index_file"), str):
                fail(errors, "v2.3 candidate_discovery index_file is missing")
            else:
                try:
                    index_bytes = (submission / discovery["index_file"]).resolve().read_bytes()
                    actual_index_hash = hashlib.sha256(index_bytes).hexdigest().upper()
                    if str(discovery.get("index_sha256", "")).upper() != actual_index_hash:
                        fail(errors, "v2.3 candidate index hash mismatch")
                except OSError:
                    fail(errors, "v2.3 candidate index file is unreadable")
            ledger = audit.get("source_artifacts")
            if isinstance(ledger, dict):
                for item in ledger.get("items", []):
                    if not isinstance(item, dict) or item.get("category") not in ARTIFACT_CATEGORIES:
                        fail(errors, "invalid v2.3 source_artifacts category")
                    if "action" in item and item.get("action") not in ARTIFACT_ACTIONS:
                        fail(errors, "invalid v2.3 source_artifacts action")

        acceptance = audit.get("acceptance", {})
        if acceptance.get("status") not in {"pass", "revised-pass"}:
            fail(errors, "acceptance status is not pass/revised-pass")
        rounds = acceptance.get("rounds", [])
        if not 1 <= len(rounds) <= 3:
            fail(errors, "acceptance must contain 1..3 rounds")
        elif rounds:
            final_round = rounds[-1]
            if final_round.get("score", 0) < 98:
                fail(errors, "final self-acceptance score is below 98")
            gates = final_round.get("hard_gates", {})
            if set(gates) != REQUIRED_HARD_GATES:
                fail(errors, "self-acceptance hard-gate set is incomplete or unexpected")
            elif not all(value is True for value in gates.values()):
                fail(errors, "one or more self-acceptance hard gates failed")

    knowledge_path = submission / "knowledge.md"
    knowledge = knowledge_path.read_text(encoding="utf-8") if knowledge_path.is_file() else ""
    if proof_leak_matches(knowledge):
        fail(errors, "proof heading leaked into knowledge.md")
    if exercise_leak_matches(knowledge):
        fail(errors, "exercise section leaked into knowledge.md")
    if audit:
        for candidate in audit.get("candidates", []):
            if candidate.get("decision") == "include" and candidate.get("block_id") not in knowledge:
                fail(errors, f"included candidate missing from knowledge.md: {candidate.get('block_id')}")

    if args.require_bilingual:
        raw_terms = audit.get("bilingual_terms") if audit else None
        terms, term_format_errors = normalise_terms(raw_terms)
        for term_error in term_format_errors:
            fail(errors, term_error)
        if raw_terms is not None and not terms:
            fail(errors, "双语术语表为空: --require-bilingual 至少需要一条 bilingual_terms 记录")
        elif raw_terms is None and not terms:
            # A term table is the reliable path for translated material.  The
            # fallback keeps tiny hand-written fixtures useful and is limited
            # to strict mode, so legacy same-language submissions remain
            # byte-for-byte compatible when the flag is omitted.
            included = [
                candidate.get("block_id")
                for candidate in audit.get("candidates", [])
                if candidate.get("decision") == "include" and candidate.get("block_id")
            ] if audit else []
            terms = infer_terms(knowledge, included)
            if not terms:
                fail(
                    errors,
                    "双语术语表缺失: --require-bilingual 需要 audit.bilingual_terms，且无法从纳入块推断术语",
                )
        for term in terms:
            if term.block_id and term.block_id not in included_ids:
                fail(
                    errors,
                    f"双语术语块不是纳入候选: {term.term}（{term.block_id}）",
                )
        for bilingual_error in validate_bilingual_terms(
            knowledge, terms, included_block_ids=included_ids
        ):
            fail(errors, bilingual_error)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: workflow, scope slice, candidates, self-acceptance, and extraction artifacts verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
