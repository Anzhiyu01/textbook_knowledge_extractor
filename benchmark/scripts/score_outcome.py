#!/usr/bin/env python3
"""Score v2.5 final artifacts without using experiment-arm or process data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from validate_public_submission import validate_public_submission
except ImportError:  # pragma: no cover
    from .validate_public_submission import validate_public_submission


CONTEXTUAL_KINDS = {"example", "counterexample", "remark"}
FRACTIONS = {0.0, 0.25, 0.5, 0.75, 1.0}
DIMENSIONS = {
    "coverage": 40.0,
    "fidelity_math": 30.0,
    "exclusion": 15.0,
    "structure": 10.0,
    "traceability": 5.0,
}


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _gold_id(item: dict[str, Any]) -> str | None:
    value = item.get("gold_id", item.get("block_id"))
    return value if isinstance(value, str) and value else None


def _included_items(gold: dict[str, Any]) -> list[dict[str, Any]]:
    rows = gold.get("items", [])
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict) and row.get("decision") == "include"]


def _weighted_fraction(items: list[dict[str, Any]], values: dict[str, float], field: str) -> float:
    total = sum(float(item.get("weight", 1.0)) for item in items)
    if total <= 0:
        return 0.0
    earned = 0.0
    for item in items:
        item_id = _gold_id(item)
        earned += float(item.get("weight", 1.0)) * values.get(item_id or "", 0.0)
    return earned / total


def score_submission(
    case_path: Path,
    submission: Path,
    gold_path: Path,
    review_path: Path | None = None,
) -> dict[str, Any]:
    validation, _ = validate_public_submission(case_path, submission)
    gold = _object(gold_path)
    review = _object(review_path) if review_path is not None else {}
    blocked: list[str] = []
    if gold.get("status") != "reviewed":
        blocked.append("gold is not fully human-reviewed")
    if review.get("status") != "reviewed":
        blocked.append("submission semantic review is not complete")
    if not validation.get("scorable"):
        blocked.append("knowledge.md is not scorable")

    included = _included_items(gold)
    if gold.get("status") == "reviewed" and not included:
        blocked.append("reviewed gold has no included atomic items")
    review_rows = review.get("items", []) if isinstance(review.get("items"), list) else []
    review_by_id = {
        row.get("gold_id"): row
        for row in review_rows
        if isinstance(row, dict) and isinstance(row.get("gold_id"), str)
    }

    coverage: dict[str, float] = {}
    fidelity: dict[str, float] = {}
    for item in included:
        item_id = _gold_id(item)
        if not item_id:
            blocked.append("gold contains an item without gold_id/block_id")
            continue
        row = review_by_id.get(item_id)
        if row is None:
            blocked.append(f"submission review missing {item_id}")
            continue
        c_value = row.get("coverage")
        f_value = row.get("fidelity_math")
        if not isinstance(c_value, (int, float)) or float(c_value) not in FRACTIONS:
            blocked.append(f"invalid coverage fraction for {item_id}")
        else:
            coverage[item_id] = float(c_value)
        if not isinstance(f_value, (int, float)) or not 0 <= float(f_value) <= 1:
            blocked.append(f"invalid fidelity_math fraction for {item_id}")
        else:
            fidelity[item_id] = float(f_value)

    formal = [item for item in included if item.get("kind") not in CONTEXTUAL_KINDS]
    contextual = [item for item in included if item.get("kind") in CONTEXTUAL_KINDS]
    formal_points = 30.0 * _weighted_fraction(formal, coverage, "coverage") if formal else 0.0
    contextual_points = 10.0 * _weighted_fraction(contextual, coverage, "coverage") if contextual else 0.0
    coverage_points = formal_points + contextual_points
    fidelity_points = 30.0 * _weighted_fraction(included, fidelity, "fidelity_math") if included else 0.0

    exclusion_fraction = review.get("exclusion_fraction")
    structure_fraction = review.get("structure_fraction")
    if not isinstance(exclusion_fraction, (int, float)) or not 0 <= float(exclusion_fraction) <= 1:
        blocked.append("review exclusion_fraction must be in [0, 1]")
        exclusion_fraction = 0.0
    if not isinstance(structure_fraction, (int, float)) or not 0 <= float(structure_fraction) <= 1:
        blocked.append("review structure_fraction must be in [0, 1]")
        structure_fraction = 0.0
    explicit_leak_count = max(
        int(review.get("proof_leak_count", 0) or 0),
        int(validation.get("proof_leak_count", 0) or 0),
    ) + max(
        int(review.get("exercise_leak_count", 0) or 0),
        int(validation.get("exercise_leak_count", 0) or 0),
    )
    exclusion_points = min(
        15.0 * float(exclusion_fraction),
        max(0.0, 15.0 - 3.0 * explicit_leak_count),
    )
    structure_points = 10.0 * float(structure_fraction)
    trace_points = 5.0 * float(validation.get("audit_trace_fraction", 0.0))

    dimension_scores = {
        "coverage": round(coverage_points, 4),
        "fidelity_math": round(fidelity_points, 4),
        "exclusion": round(exclusion_points, 4),
        "structure": round(structure_points, 4),
        "traceability": round(trace_points, 4),
    }
    total = round(sum(dimension_scores.values()), 4)
    partial = sum(value in {0.25, 0.5, 0.75} for value in coverage.values())
    omitted = sum(value == 0 for value in coverage.values())
    report: dict[str, Any] = {
        "score_protocol_version": "2.5",
        "case_id": gold.get("case_id"),
        "headline_eligible": not blocked,
        "blocked_reasons": list(dict.fromkeys(blocked)),
        "dimension_maxima": DIMENSIONS,
        "dimension_scores_diagnostic": dimension_scores,
        "formal_block_recall": round(_weighted_fraction(formal, coverage, "coverage"), 6) if formal else None,
        "contextual_block_recall": round(_weighted_fraction(contextual, coverage, "coverage"), 6) if contextual else None,
        "partial_hit_count": partial,
        "omitted_count": omitted,
        "unsupported_extra_count": int(review.get("unsupported_extra_count", 0) or 0),
        "mathematical_error_count": int(review.get("mathematical_error_count", 0) or 0),
        "proof_leak_count": max(
            int(review.get("proof_leak_count", 0) or 0),
            int(validation.get("proof_leak_count", 0) or 0),
        ),
        "exercise_leak_count": max(
            int(review.get("exercise_leak_count", 0) or 0),
            int(validation.get("exercise_leak_count", 0) or 0),
        ),
        "human_review_items": review.get("human_review_items", []),
        "validation": validation,
    }
    if not blocked:
        report["total_points"] = total
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--submission", required=True, type=Path)
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--review", type=Path)
    args = parser.parse_args()
    report = score_submission(
        args.case.resolve(), args.submission.resolve(), args.gold.resolve(),
        args.review.resolve() if args.review else None,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["headline_eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
