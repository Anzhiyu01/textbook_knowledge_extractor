#!/usr/bin/env python3
"""Dependency-free structural fallback for audit.json.

This is intentionally smaller than JSON Schema validation.  Use it only when
the ``jsonschema`` package is unavailable, and record that limitation in the
run log.  It checks the contract fields that are most likely to invalidate a
submission: top-level keys, hashes, spans, block-id width, decisions,
source-artifact records, and acceptance hard gates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SHA256_RE = re.compile(r"^[A-Fa-f0-9]{64}$")
BLOCK_ID_RE = re.compile(r"^K-[0-9]{3,}$")
HARD_GATES = {
    "task_understood",
    "scope_verified_first",
    "candidate_closure",
    "contextual_block_recall",
    "no_contamination",
    "mathematics_intact",
    "artifacts_verified",
}


def check(audit: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "case_id",
        "source_sha256",
        "task_understanding",
        "scope_preprocessing",
        "boundaries",
        "candidates",
        "acceptance",
    }
    missing = sorted(required - set(audit))
    if missing:
        errors.append(f"missing top-level field(s): {', '.join(missing)}")
    if not isinstance(audit.get("source_sha256"), str) or not SHA256_RE.fullmatch(audit["source_sha256"]):
        errors.append("source_sha256 must be a 64-hex string")

    candidates = audit.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidates must be a non-empty array")
    else:
        seen: set[str] = set()
        previous_start = 0
        for index, candidate in enumerate(candidates, start=1):
            if not isinstance(candidate, dict):
                errors.append(f"candidates[{index}] must be an object")
                continue
            block_id = candidate.get("block_id")
            if not isinstance(block_id, str) or not BLOCK_ID_RE.fullmatch(block_id):
                errors.append(f"candidates[{index}] invalid block_id {block_id!r}")
            elif block_id in seen:
                errors.append(f"duplicate block_id {block_id}")
            else:
                seen.add(block_id)
            start, end = candidate.get("source_start_line"), candidate.get("source_end_line")
            if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or start > end:
                errors.append(f"candidates[{index}] invalid source span")
            elif start < previous_start:
                errors.append(f"candidates[{index}] is out of source order")
            else:
                previous_start = start
            if candidate.get("decision") not in {"include", "exclude"}:
                errors.append(f"candidates[{index}] invalid decision")

    artifacts = audit.get("source_artifacts")
    if artifacts is not None:
        if not isinstance(artifacts, dict) or not isinstance(artifacts.get("items"), list):
            errors.append("source_artifacts.items must be an array when source_artifacts is present")
        else:
            for index, item in enumerate(artifacts["items"], start=1):
                if not isinstance(item, dict):
                    errors.append(f"source_artifacts.items[{index}] must be an object")
                    continue
                for field in ("category", "source_line", "original", "basis"):
                    if field not in item:
                        errors.append(f"source_artifacts.items[{index}] missing {field}")

    judgments = audit.get("extraction_judgments", [])
    if not isinstance(judgments, list):
        errors.append("extraction_judgments must be an array")
    else:
        for index, judgment in enumerate(judgments, start=1):
            if isinstance(judgment, str):
                continue  # legacy free-text records remain readable
            if not isinstance(judgment, dict):
                errors.append(f"extraction_judgments[{index}] must be a string or object")
                continue
            for field in ("judgment_id", "source_start_line", "source_end_line", "classification", "decision", "basis"):
                if field not in judgment:
                    errors.append(f"extraction_judgments[{index}] missing {field}")

    acceptance = audit.get("acceptance")
    if not isinstance(acceptance, dict) or acceptance.get("status") not in {"pass", "revised-pass", "blocked"}:
        errors.append("acceptance.status is invalid or missing")
    rounds = acceptance.get("rounds") if isinstance(acceptance, dict) else None
    if not isinstance(rounds, list) or not 1 <= len(rounds) <= 3:
        errors.append("acceptance.rounds must contain 1..3 records")
    elif rounds:
        gates = rounds[-1].get("hard_gates") if isinstance(rounds[-1], dict) else None
        if not isinstance(gates, dict) or set(gates) != HARD_GATES or not all(value is True for value in gates.values()):
            errors.append("final hard_gates must contain exactly the seven boolean gates, all true")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        audit = json.loads(args.audit.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"SCHEMA-FALLBACK ERROR: cannot read audit.json: {exc}")
        return 2
    if not isinstance(audit, dict):
        print("SCHEMA-FALLBACK FAIL: audit.json must contain an object")
        return 1
    errors = check(audit)
    if errors:
        print("SCHEMA-FALLBACK FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SCHEMA-FALLBACK PASS (dependency-free structural checks; not full JSON Schema validation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
