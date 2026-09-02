"""Check whether the declared default cases are safe to freeze and run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def check_catalog(catalog_file: Path, repo_root: Path) -> dict[str, Any]:
    catalog = json.loads(catalog_file.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    statuses: dict[str, str] = {}
    cases = {case["case_id"]: case for case in catalog.get("cases", [])}
    for case_id in catalog.get("default_case_ids", []):
        case = cases.get(case_id)
        if case is None:
            errors.append(f"default case is not declared: {case_id}")
            continue
        status = case.get("status", "unknown")
        statuses[case_id] = status
        for field in ("source_of_truth", "public_slice", "public_case", "backend_gold"):
            value = case.get(field)
            if isinstance(value, str):
                path = repo_root / value
                if not path.is_file():
                    errors.append(f"{case_id}: missing {field}: {value}")
        if status != "ready":
            errors.append(f"{case_id}: not runnable ({status})")
    return {
        "status": "PASS" if not errors else "BLOCKED",
        "default_case_ids": catalog.get("default_case_ids", []),
        "case_statuses": statuses,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path(__file__).parents[1] / "default_cases.json")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    args = parser.parse_args()
    report = check_catalog(args.catalog.resolve(), args.repo_root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
