#!/usr/bin/env python3
"""Optional benchmark coverage comparison.

Unlike selfcheck, this command only compares an audit's explicit candidate IDs
with a supplied manifest.  It never infers candidates from source prose.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--audit", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    args = p.parse_args()
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    gold = json.loads(args.manifest.read_text(encoding="utf-8"))
    actual = [c.get("block_id") for c in audit.get("candidates", []) if isinstance(c, dict) and c.get("decision") == "include"]
    expected = gold.get("included_ids") if isinstance(gold, dict) else gold
    if expected is None and isinstance(gold, dict):
        rows = gold.get("candidates", gold.get("required_blocks", gold.get("blocks", [])))
        expected = [r.get("block_id") for r in rows if isinstance(r, dict) and r.get("decision", "include") == "include"]
    expected = expected or []
    if not isinstance(expected, list):
        raise SystemExit("manifest must be a list or object with included_ids")
    missing = [x for x in expected if x not in actual]
    extra = [x for x in actual if x not in expected]
    report = {"status": "PASS" if not missing and not extra else "FAIL", "expected": expected, "actual": actual, "missing": missing, "extra": extra}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1
if __name__ == "__main__":
    raise SystemExit(main())
