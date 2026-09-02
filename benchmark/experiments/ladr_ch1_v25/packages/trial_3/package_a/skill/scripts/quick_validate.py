"""Quick v2.4 run-package validator."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from check_math_rendering import validate_file

REQUIRED = {"knowledge.md", "audit.json", "runlog.md", "work/slice.md", "work/scope.json", "work/candidate_index.json", "work/math_check.json"}

def validate_package(root: Path) -> list[str]:
    errors=[f"missing {p}" for p in sorted(REQUIRED) if not (root / p).is_file()]
    if (root/'knowledge.md').is_file():
        check=validate_file(root/'knowledge.md')
        if not check['passed']: errors.append(f"math check failed: {len(check['issues'])} issue(s)")
    try:
        json.loads((root/'audit.json').read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f"audit.json unreadable: {exc}")
    return errors

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--package', required=True, type=Path); a=p.parse_args(); e=validate_package(a.package); print('PASS' if not e else '\n'.join(['FAIL', *e])); raise SystemExit(bool(e))
