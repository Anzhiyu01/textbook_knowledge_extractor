"""Materialize public slices and review-gated gold skeletons from scratch sources."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CASE_SPECS = (
    {
        "case_id": "rudin_ch2_v25",
        "target": "Principles of Mathematical Analysis, Chapter 2",
        "source": "scratch/Rudin.md",
        "start_heading": "## FINITE, COUNTABLE, AND UNCOUNTABLE SETS",
        "end_before_heading": "# NUMERICAL SEQUENCES AND SERIES",
        "source_file": "rudin_ch2_slice.md",
        "public_dir": "rudin_ch2",
    },
    {
        "case_id": "probability_ch1_v25",
        "target": "Probability, Chapter 1",
        "source": "scratch/probability_theory.md",
        "start_heading": "## 第一章 事件与概率",
        "end_before_heading": "## 第二章 条件概率与统计独立性",
        "source_file": "probability_ch1_slice.md",
        "public_dir": "probability_ch1",
    },
)


def _candidate_kind(text: str) -> str:
    lowered = text.lower()
    if re.search(r"definition|定义", lowered):
        return "definition"
    if re.search(r"theorem|lemma|proposition|corollary|定理|引理|命题|推论", lowered):
        return "theorem"
    if re.search(r"example|例", lowered):
        return "example"
    if re.search(r"remark|备注|注", lowered):
        return "remark"
    if re.search(r"formula|公式|=|\\equiv|\\leq|\\subset", lowered):
        return "formula"
    return "other"


def _candidate_items(lines: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    block_start: int | None = None
    block: list[str] = []

    def flush(end_line: int) -> None:
        nonlocal block_start, block
        text = " ".join(part.strip() for part in block if part.strip())
        if text and block_start is not None:
            items.append({
                "block_id": f"K-{block_start:03d}",
                "decision": None,
                "kind": _candidate_kind(text),
                "source_start_line": block_start,
                "source_end_line": end_line,
                "source_anchor": text[:200],
                "atomic_requirements": [],
                "weight": 1,
                "review": "required",
            })
        block_start = None
        block = []

    for relative_line, line in enumerate(lines, start=1):
        if line.strip():
            if block_start is None:
                block_start = relative_line
            block.append(line)
        elif block_start is not None:
            flush(relative_line - 1)
    if block_start is not None:
        flush(len(lines))
    return items


def prepare_case(repo_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    source_path = repo_root / spec["source"]
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    source_lines = source_path.read_text(encoding="utf-8-sig").splitlines()
    try:
        start_index = source_lines.index(spec["start_heading"])
        end_index = source_lines.index(spec["end_before_heading"], start_index + 1)
    except ValueError as error:
        raise ValueError(f"{spec['case_id']}: chapter heading boundary not found") from error
    slice_lines = source_lines[start_index:end_index]

    case_root = repo_root / "benchmark" / spec["public_dir"]
    input_dir = case_root / "input"
    control_dir = case_root / "control"
    gold_dir = case_root / "gold"
    input_dir.mkdir(parents=True, exist_ok=True)
    control_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / spec["source_file"]).write_text(
        "\n".join(slice_lines) + "\n", encoding="utf-8"
    )
    public_case = {
        "public_case_version": "2.5",
        "case_id": spec["case_id"],
        "source_file": spec["source_file"],
        "target": spec["target"],
        "output_language": "zh-CN",
        "include_classes": [
            "definition", "axiom", "convention", "notation", "proposition",
            "lemma", "theorem", "corollary", "property", "criterion", "identity",
            "formula", "construction", "example", "counterexample", "remark",
        ],
        "exclude_classes": [
            "proof", "derivation", "ordinary explanation", "exercise",
            "out-of-slice content", "unsupported addition",
        ],
        "submission_files": ["knowledge.md", "audit.json"],
        "audit_schema_file": "public_audit.schema.json",
    }
    (input_dir / "public_case.json").write_text(
        json.dumps(public_case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    backend_case = {
        "case_version": "2.5.0",
        "case_id": spec["case_id"],
        "source_file": spec["source"],
        "target": {
            "start_heading": spec["start_heading"],
            "end_before_heading": spec["end_before_heading"],
            "resolved_start_line": start_index + 1,
            "resolved_end_line": end_index,
        },
        "submission_files": ["knowledge.md", "audit.json"],
    }
    (control_dir / "case_v25.json").write_text(
        json.dumps(backend_case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    items = _candidate_items(slice_lines)
    gold = {
        "gold_version": "2.5",
        "case_id": spec["case_id"],
        "status": "human_review_required",
        "review": {
            "required": True,
            "completed": False,
            "minimum_reviewers": 2,
            "note": "Auto-generated candidate boundaries require independent include/exclude and atomic review.",
        },
        "candidate_count": len(items),
        "items": items,
    }
    (gold_dir / "candidate_gold.json").write_text(
        json.dumps(gold, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "case_id": spec["case_id"],
        "source": str(source_path),
        "slice": str(input_dir / spec["source_file"]),
        "candidate_count": len(items),
        "slice_line_count": len(slice_lines),
        "resolved_source_lines": [start_index + 1, end_index],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    args = parser.parse_args()
    reports = [prepare_case(args.repo_root.resolve(), spec) for spec in CASE_SPECS]
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
