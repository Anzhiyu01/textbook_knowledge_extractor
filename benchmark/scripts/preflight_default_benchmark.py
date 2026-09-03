"""Preflight the complete default catalog before any model run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def preflight(catalog_path: Path, repo_root: Path) -> dict[str, Any]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    declared = {case["case_id"]: case for case in catalog.get("cases", [])}
    for case_id in catalog.get("default_case_ids", []):
        case = declared.get(case_id)
        if case is None:
            errors.append(f"undeclared default case: {case_id}")
            continue
        missing: list[str] = []
        for field in (
            "source_of_truth", "public_slice", "public_case", "backend_gold", "backend_case"
        ):
            value = case.get(field)
            if not isinstance(value, str) or not (repo_root / value).is_file():
                missing.append(field)
        status = case.get("status")
        ready = not missing and status == "ready"
        if not ready:
            errors.append(
                f"{case_id}: status={status!r}, missing={','.join(missing) or 'none'}"
            )
        cases.append({"case_id": case_id, "status": status, "missing": missing, "ready": ready})
    return {
        "status": "PASS" if not errors else "BLOCKED",
        "case_count": len(cases),
        "cases": cases,
        "errors": errors,
        "rule": "all default cases must be ready before a paired headline score",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path(__file__).parents[1] / "default_cases.json")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    args = parser.parse_args()
    report = preflight(args.catalog.resolve(), args.repo_root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
