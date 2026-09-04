"""Adapt user-accepted Markdown knowledge lists into review-gated v2.5 gold."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SPECS = (
    ("ladr_ch1_v25", "scratch/ladr_ch1_list.md", "benchmark/ladr_ch1/gold", "bold_k"),
    ("rudin_ch2_v25", "scratch/Rudin_ch2_list.md", "benchmark/rudin_ch2/gold", "rudin"),
    ("probability_ch1_v25", "scratch/probability_ch1_list.md", "benchmark/probability_ch1/gold", "bold_k"),
)
BOLD_K_RE = re.compile(r"^\*\*(K-[0-9]+)\s+(.+?)\*\*\s*$")
RUDIN_RE = re.compile(r"^###\s+.*?\b2\.([0-9]+)\b.*$")


def _kind(title: str) -> str:
    lowered = title.lower()
    for pattern, value in (
        (r"反例|counterexample", "counterexample"),
        (r"定义|definition", "definition"),
        (r"公理|axiom", "axiom"),
        (r"约定|convention", "convention"),
        (r"记号|notation", "notation"),
        (r"引理|lemma", "lemma"),
        (r"推论|corollary", "corollary"),
        (r"定理|theorem", "theorem"),
        (r"命题|proposition", "proposition"),
        (r"例|example", "example"),
        (r"评注|备注|注[:：]|remark", "remark"),
        (r"性质|property", "property"),
        (r"公式|formula", "formula"),
        (r"判定|criterion", "criterion"),
    ):
        if re.search(pattern, lowered):
            return value
    return "other"


def _blocks(text: str, mode: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        if mode == "bold_k":
            match = BOLD_K_RE.match(line)
            if match:
                starts.append((index, match.group(1), match.group(2)))
        else:
            match = RUDIN_RE.match(line)
            if match:
                number = match.group(1)
                title = line[4:].strip()
                starts.append((index, f"K-{200 + int(number):03d}", title))
    items: list[dict[str, Any]] = []
    for position, (start, block_id, title) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines) - 1
        body = "\n".join(lines[start + 1 : end + 1]).strip()
        reference_text = f"{title}\n\n{body}".strip()
        items.append({
            "block_id": block_id,
            "decision": "include",
            "kind": _kind(title),
            "source_anchor": title[:200],
            "atomic_requirements": [],
            "weight": 1,
            "review": "user-accepted reference; independent source and atomic review required",
            "review_evidence": [f"reference_knowledge.md:{start + 1}-{end + 1}"],
            "reference_start_line": start + 1,
            "reference_end_line": end + 1,
            "reference_text": reference_text,
            "source_mapping_status": "human_review_required",
        })
    if not items:
        raise ValueError(f"no knowledge blocks parsed with mode={mode}")
    ids = [item["block_id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate gold block IDs")
    return items


def adapt(repo_root: Path, case_id: str, source_rel: str, gold_rel: str, mode: str) -> dict[str, Any]:
    source = repo_root / source_rel
    gold_dir = repo_root / gold_rel
    text = source.read_text(encoding="utf-8-sig")
    items = _blocks(text, mode)
    gold_dir.mkdir(parents=True, exist_ok=True)
    reference = gold_dir / "reference_knowledge.md"
    shutil.copy2(source, reference)
    digest = hashlib.sha256(reference.read_bytes()).hexdigest()
    gold = {
        "gold_version": "2.5",
        "case_id": case_id,
        "status": "human_review_required",
        "review": {
            "required": True,
            "completed": False,
            "minimum_reviewers": 2,
            "accepted_reference": True,
            "accepted_by": "benchmark owner",
            "independent_reviewers_completed": 0,
            "note": "The owner accepted this deliverable as useful. Independent source mapping and atomic review remain required before headline scoring.",
        },
        "reference": {
            "file": "reference_knowledge.md",
            "source_file": source_rel,
            "sha256": digest,
            "adaptation": mode,
        },
        "candidate_count": len(items),
        "items": items,
    }
    output = gold_dir / "candidate_gold.json"
    output.write_text(json.dumps(gold, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"case_id": case_id, "item_count": len(items), "reference_sha256": digest, "gold": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    args = parser.parse_args()
    root = args.repo_root.resolve()
    reports = [adapt(root, *spec) for spec in SPECS]
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
