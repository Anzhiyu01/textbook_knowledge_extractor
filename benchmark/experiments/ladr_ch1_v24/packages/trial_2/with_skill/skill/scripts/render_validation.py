"""Run deterministic math checks and optional fixed KaTeX/MathJax engines."""
from __future__ import annotations
import json, re, shutil, subprocess
from pathlib import Path
try:
    from .check_math_rendering import check_markdown
except ImportError:
    from check_math_rendering import check_markdown

def validate(path: Path) -> dict:
    result = {"math_check": {"passed": False, "issues": []}, "katex": {"status": "unavailable"}, "mathjax": {"status": "unavailable"}}
    result["math_check"] = {"passed": not bool(check_markdown(path.read_text(encoding="utf-8"))), "issues": [x.__dict__ for x in check_markdown(path.read_text(encoding="utf-8"))]}
    node = shutil.which("node")
    if node:
        for engine, package in (("katex", "katex"), ("mathjax", "mathjax-full")):
            probe = subprocess.run([node, "-e", f"try{{require.resolve('{package}');process.exit(0)}}catch(e){{process.exit(1)}}"], capture_output=True)
            result[engine] = {"status": "available" if probe.returncode == 0 else "unavailable", "version": "fixed-by-environment"}
    result["passed"] = result["math_check"]["passed"] and all(result[e]["status"] == "available" for e in ("katex", "mathjax"))
    return result

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--file", required=True); args=p.parse_args(); out=validate(Path(args.file)); print(json.dumps(out, ensure_ascii=False, indent=2)); raise SystemExit(0 if out["passed"] else 1)
