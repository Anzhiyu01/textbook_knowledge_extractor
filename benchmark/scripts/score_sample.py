#!/usr/bin/env python3
"""Small deterministic scorer for extraction development cases.

The historical invocation (``--submission`` only) still scores
``gold/sample_gold.json``.  A translated development case can pass
``--case`` or ``--gold`` explicitly; its gold may use ``any_of``/``alternatives``
for a bilingual fragment so punctuation and source/target orientation remain
format-level choices rather than accidental score failures.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:  # Script execution (``python scripts/...``) and package imports alike.
    from leak_patterns import exercise_leak_matches, proof_leak_matches
except ImportError:  # pragma: no cover - only needed when imported as a package
    from .leak_patterns import exercise_leak_matches, proof_leak_matches


def _fragment_hit(text: str, fragment: object, bilingual_any: bool = False) -> bool:
    """Match one gold fragment, accepting explicit alternatives.

    Gold files remain plain JSON and backwards compatible: a string means an
    exact substring, while a list or ``{"any_of": [...]}`` means any listed
    substring.  ``bilingual_any`` additionally treats full/half-width
    parentheses around a source term as equivalent for simple pair strings.
    """

    if isinstance(fragment, str):
        if fragment in text:
            return True
        if bilingual_any:
            # The common translation forms differ only by bracket width or
            # spacing.  Keep this deliberately format-level and conservative.
            variants = {
                fragment.replace("（", "(").replace("）", ")"),
                fragment.replace("(", "（").replace(")", "）"),
                fragment.replace("（", " ( ").replace("）", " ) "),
            }
            if any(variant in text for variant in variants):
                return True
            # Also accept ordinary spaces around either bracket width, but
            # only for fragments that visibly contain both languages.  This
            # keeps the opt-in tolerance from changing ordinary math/text
            # substring scoring.
            if (
                re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", fragment)
                and re.search(r"[A-Za-z]", fragment)
                and re.search(r"[（）()]", fragment)
            ):
                parts = re.split(r"([（）()])", fragment)
                pattern_parts: list[str] = []
                for part in parts:
                    if part in {"（", "("}:
                        pattern_parts.append(r"[ \t]*[（(][ \t]*")
                    elif part in {"）", ")"}:
                        pattern_parts.append(r"[ \t]*[）)][ \t]*")
                    else:
                        pattern_parts.append(re.escape(part))
                if re.search("".join(pattern_parts), text):
                    return True
            return False
        return False
    if isinstance(fragment, (list, tuple)):
        return any(_fragment_hit(text, item, bilingual_any) for item in fragment)
    if isinstance(fragment, dict):
        for key in ("any_of", "alternatives", "one_of"):
            if key in fragment:
                values = fragment[key]
                return isinstance(values, list) and any(
                    _fragment_hit(text, item, bilingual_any) for item in values
                )
        value = fragment.get("fragment")
        return _fragment_hit(text, value, bilingual_any) if value is not None else False
    return False


def contains_all(text: str, fragments: list[object], bilingual_any: bool = False) -> bool:
    return all(_fragment_hit(text, fragment, bilingual_any) for fragment in fragments)


def _load_gold(root: Path, case_path: Path | None, gold_path: Path | None) -> tuple[dict, Path, dict]:
    """Load a gold file and optional case metadata.

    ``case.gold_file`` (or ``case.gold``) is resolved relative to the case
    directory.  If omitted, the conventional sibling ``gold`` directory is
    searched before falling back to the public sample gold.
    """

    case: dict = {}
    if case_path is not None:
        case = json.loads(case_path.read_text(encoding="utf-8"))
    if gold_path is None and case_path is not None:
        declared = case.get("gold_file") or case.get("gold")
        if isinstance(declared, str) and declared:
            candidate = (case_path.parent / declared).resolve()
            if candidate.is_file():
                gold_path = candidate
        if gold_path is None:
            for name in (
                f"{case_path.stem.replace('_case', '_gold')}.json",
                f"{case_path.stem.replace('-case', '-gold')}.json",
            ):
                candidate = (root / "gold" / name).resolve()
                if candidate.is_file():
                    gold_path = candidate
                    break
    if gold_path is None:
        gold_path = root / "gold" / "sample_gold.json"
    gold_path = gold_path.resolve()
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    if not isinstance(gold, dict):
        raise ValueError("gold file must contain a JSON object")
    return gold, gold_path, case


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", required=True, type=Path)
    parser.add_argument(
        "--case",
        type=Path,
        help="optional case manifest; selects its gold_file and output metadata",
    )
    parser.add_argument(
        "--gold",
        type=Path,
        help="optional gold JSON (overrides case/default gold)",
    )
    parser.add_argument(
        "--bilingual-any",
        action="store_true",
        help="accept explicit bilingual fragment alternatives and bracket-width variants",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        gold, gold_path, case = _load_gold(
            root,
            args.case.resolve() if args.case else None,
            args.gold.resolve() if args.gold else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read case/gold: {exc}")
        return 2
    knowledge_path = args.submission / "knowledge.md"
    knowledge = knowledge_path.read_text(encoding="utf-8") if knowledge_path.is_file() else ""

    audit_path = args.submission / "audit.json"
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except Exception:
        audit = {}

    blocks = gold["required_blocks"]
    hit = [
        block
        for block in blocks
        if contains_all(knowledge, block["required_fragments"], args.bilingual_any)
    ]
    formal = [b for b in blocks if b["kind"] not in {"example", "counterexample", "remark"}]
    contextual = [b for b in blocks if b["kind"] in {"example", "counterexample", "remark"}]
    formal_hit = sum(
        contains_all(knowledge, b["required_fragments"], args.bilingual_any)
        for b in formal
    )
    contextual_hit = sum(
        contains_all(knowledge, b["required_fragments"], args.bilingual_any)
        for b in contextual
    )

    coverage_points = 30 * len(hit) / len(blocks)
    target = gold["boundaries"]
    audited_boundary = (
        audit.get("boundaries", {}).get("start_line") == target["start_line"]
        and audit.get("boundaries", {}).get("end_line") == target["end_line"]
        and audit.get("boundaries", {}).get("start_heading") == target["start_heading"]
        and audit.get("boundaries", {}).get("end_before_heading") == target["end_before_heading"]
    )
    boundary_points = 10 if audited_boundary else 0
    # Keep contamination detection exactly aligned with validate_submission;
    # translated outputs may use bilingual, punctuated, or numbered headings.
    proof_leaks = len(proof_leak_matches(knowledge))
    exercise_leaks = bool(exercise_leak_matches(knowledge))
    fidelity_points = 20 * len(hit) / len(blocks)
    math_points = 15 * len(hit) / len(blocks)
    exclusion_points = 10 if proof_leaks == 0 and not exercise_leaks else 0
    ordered_ids = [f"K-{block['start_line']:03d}" for block in blocks]
    id_positions = [knowledge.find(block_id) for block_id in ordered_ids]
    order_points = 5 if all(pos >= 0 for pos in id_positions) and id_positions == sorted(id_positions) else 0
    audit_points = 5 if audit.get("case_id") == gold["case_id"] and audit.get("source_sha256") == gold["source_sha256"] else 0

    final_rounds = audit.get("acceptance", {}).get("rounds", [])
    workflow_points = 0
    if (
        audit.get("task_understanding")
        and audit.get("scope_preprocessing", {}).get("index_before_full_read") is True
        and audit.get("scope_preprocessing", {}).get("full_source_opened_before_slice") is False
        and audit.get("acceptance", {}).get("status") in {"pass", "revised-pass"}
        and final_rounds
        and final_rounds[-1].get("score", 0) >= 98
        and all(final_rounds[-1].get("hard_gates", {}).values())
    ):
        workflow_points = 5

    total = (
        coverage_points + fidelity_points + math_points + exclusion_points
        + order_points + audit_points + boundary_points + workflow_points
    )
    if proof_leaks:
        total = max(0.0, total - 10 * proof_leaks)
    total = min(100.0, total)

    report = {
        "case_id": gold["case_id"],
        "gold_file": str(gold_path),
        "output_language": case.get("output_language", case.get("language")) if case else gold.get("output_language"),
        "bilingual_any": args.bilingual_any,
        "total_points_estimate": round(total, 2),
        "required_block_recall": round(len(hit) / len(blocks), 4),
        "formal_block_recall": round(formal_hit / len(formal), 4),
        "example_counterexample_remark_recall": round(contextual_hit / len(contextual), 4),
        "proof_leak_count": proof_leaks,
        "exercise_leak": exercise_leaks,
        "boundary_points_estimate": boundary_points,
        "order_points_estimate": order_points,
        "audit_points_estimate": audit_points,
        "workflow_points_estimate": workflow_points,
        "proposition_provability_extension": "disabled_not_scored",
        "note": "公开样题自动分只做开发反馈；正式分数仍需 hidden gold 与人工内容复核。",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
