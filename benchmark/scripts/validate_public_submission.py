#!/usr/bin/env python3
"""Validate the neutral v2.5 public output contract.

The validator intentionally ignores process evidence. A missing or malformed
audit reduces traceability but does not make readable knowledge unscorable.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from leak_patterns import exercise_leak_matches, proof_leak_matches
except ImportError:  # pragma: no cover
    from .leak_patterns import exercise_leak_matches, proof_leak_matches


BLOCK_RE = re.compile(r"^#{1,6}\s+(B-[0-9]{3,})(?:\s|$)", re.MULTILINE)
ALLOWED_KINDS = {
    "definition", "axiom", "convention", "notation", "proposition",
    "lemma", "theorem", "corollary", "property", "criterion", "identity",
    "formula", "construction", "example", "counterexample", "remark", "other",
}
TOP_LEVEL_FIELDS = {"public_audit_version", "case_id", "entries"}
ENTRY_FIELDS = {"output_id", "kind", "source"}
SOURCE_FIELDS = {
    "relative_start_line", "relative_end_line", "text_anchor", "uncertain",
    "uncertainty_note",
}


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _unique_in_source(anchor: str, source: str) -> bool:
    return bool(anchor) and source.count(anchor) == 1


def validate_public_submission(case_path: Path, submission: Path) -> tuple[dict[str, Any], int]:
    errors: list[str] = []
    warnings: list[str] = []
    diagnostics: list[str] = []

    try:
        case = _read_object(case_path)
    except Exception as exc:
        return {"status": "ERROR", "scorable": False, "errors": [str(exc)]}, 2

    source_file = case.get("source_file")
    source_path = case_path.parent / source_file if isinstance(source_file, str) else None
    try:
        source = source_path.read_text(encoding="utf-8-sig") if source_path else ""
    except Exception as exc:
        return {
            "status": "ERROR", "scorable": False,
            "errors": [f"cannot read public source: {exc}"],
        }, 2
    source_lines = source.splitlines()

    knowledge_path = submission / "knowledge.md"
    try:
        knowledge = knowledge_path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        return {
            "status": "ERROR", "scorable": False,
            "errors": [f"cannot read knowledge.md: {exc}"],
        }, 2
    if not knowledge.strip():
        return {
            "status": "ERROR", "scorable": False,
            "errors": ["knowledge.md is empty"],
        }, 2

    knowledge_ids = BLOCK_RE.findall(knowledge)
    if len(knowledge_ids) != len(set(knowledge_ids)):
        errors.append("knowledge.md contains duplicate B-* identifiers")
    if not knowledge_ids:
        errors.append("knowledge.md contains no B-* knowledge blocks")

    audit_path = submission / "audit.json"
    audit: dict[str, Any] | None = None
    try:
        audit = _read_object(audit_path)
    except Exception as exc:
        warnings.append(f"audit.json is unavailable or invalid: {exc}")

    valid_mappings: set[str] = set()
    audit_ids: list[str] = []
    if audit is not None:
        if set(audit) != TOP_LEVEL_FIELDS:
            errors.append("audit.json has missing or unexpected top-level fields")
        if audit.get("public_audit_version") != "2.5":
            errors.append("public_audit_version must be 2.5")
        if audit.get("case_id") != case.get("case_id"):
            errors.append("audit case_id does not match public case")
        entries = audit.get("entries")
        if not isinstance(entries, list):
            errors.append("audit entries must be an array")
            entries = []
        for index, entry in enumerate(entries, 1):
            label = f"audit entry {index}"
            if not isinstance(entry, dict):
                errors.append(f"{label} is not an object")
                continue
            if set(entry) != ENTRY_FIELDS:
                errors.append(f"{label} has missing or unexpected fields")
            output_id = entry.get("output_id")
            if not isinstance(output_id, str) or not re.fullmatch(r"B-[0-9]{3,}", output_id):
                errors.append(f"{label} has invalid output_id")
                continue
            audit_ids.append(output_id)
            if entry.get("kind") not in ALLOWED_KINDS:
                errors.append(f"{label} has invalid kind")
            evidence = entry.get("source")
            if not isinstance(evidence, dict):
                errors.append(f"{label} source is not an object")
                continue
            if not set(evidence).issubset(SOURCE_FIELDS):
                errors.append(f"{label} source has unexpected fields")
            start = evidence.get("relative_start_line")
            end = evidence.get("relative_end_line")
            line_mapping = (
                isinstance(start, int) and not isinstance(start, bool)
                and isinstance(end, int) and not isinstance(end, bool)
                and 1 <= start <= end <= len(source_lines)
            )
            anchor = evidence.get("text_anchor")
            anchor_mapping = isinstance(anchor, str) and _unique_in_source(anchor, source)
            uncertain_mapping = (
                evidence.get("uncertain") is True
                and isinstance(evidence.get("uncertainty_note"), str)
                and bool(evidence["uncertainty_note"].strip())
            )
            if line_mapping or anchor_mapping:
                valid_mappings.add(output_id)
            elif uncertain_mapping:
                diagnostics.append(f"{output_id} source mapping is explicitly uncertain")
            else:
                errors.append(f"{output_id} has no valid source mapping")

        if len(audit_ids) != len(set(audit_ids)):
            errors.append("audit.json contains duplicate output_id values")
        missing = [item for item in knowledge_ids if item not in set(audit_ids)]
        orphan = [item for item in audit_ids if item not in set(knowledge_ids)]
        if missing:
            errors.append(f"knowledge blocks missing from audit: {', '.join(missing)}")
        if orphan:
            errors.append(f"audit entries missing from knowledge: {', '.join(orphan)}")
        if knowledge_ids and audit_ids != knowledge_ids:
            errors.append("audit entry order does not match knowledge block order")

    denominator = len(set(knowledge_ids))
    trace_fraction = len(valid_mappings.intersection(knowledge_ids)) / denominator if denominator else 0.0
    proof_leaks = proof_leak_matches(knowledge)
    exercise_leaks = exercise_leak_matches(knowledge)
    report = {
        "protocol_version": "2.5",
        "status": "PASS" if not errors and not warnings else "WARN",
        "scorable": True,
        "knowledge_block_count": len(knowledge_ids),
        "audit_entry_count": len(audit_ids),
        "valid_source_mapping_count": len(valid_mappings.intersection(knowledge_ids)),
        "audit_trace_fraction": round(trace_fraction, 6),
        "proof_leak_count": len(proof_leaks),
        "exercise_leak_count": len(exercise_leaks),
        "errors": errors,
        "warnings": warnings,
        "diagnostics": diagnostics,
    }
    return report, 0 if not errors and not warnings else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--submission", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report, code = validate_public_submission(args.case.resolve(), args.submission.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
