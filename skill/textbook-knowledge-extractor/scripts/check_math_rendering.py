"""Markdown-aware checks for v2.4 math delimiters and common TeX leaks."""
from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class MathIssue:
    line: int
    code: str
    text: str

_BARE = re.compile(r"(?<![\\$])(?:\\begin\{|\\mathbf\b|\\operatorname\b)")
_MONEY = re.compile(r"\$\d+(?:\.\d{1,2})?(?:\s|$)")
_BARE_SUBSCRIPT = re.compile(r"(?<![$\\\w])([A-Za-z])_([A-Za-z0-9])")

def check_markdown(text: str) -> list[MathIssue]:
    issues: list[MathIssue] = []
    in_fence = False
    display = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.strip() == "$$":
            display = not display
            continue
        if "$$" in line and line.strip() != "$$":
            issues.append(MathIssue(line_no, "display_not_independent", "display math must use independent $$ lines"))
        if _BARE.search(line):
            issues.append(MathIssue(line_no, "bare_latex", "LaTeX command outside math delimiters"))
        if _BARE_SUBSCRIPT.search(line) and "$" not in line:
            issues.append(MathIssue(line_no, "bare_subscript", "subscript outside math delimiters"))
        if _MONEY.search(line):
            continue
        dollars = re.sub(r"\\\$", "", line).count("$")
        if dollars % 2:
            issues.append(MathIssue(line_no, "unpaired_inline_dollar", "unpaired $ delimiter"))
        if "\\begin{" in line or "\\end{" in line:
            if not ("$$" in line or "$" in line):
                issues.append(MathIssue(line_no, "environment_outside_math", "math environment must be delimited"))
        if line.count("{") != line.count("}"):
            issues.append(MathIssue(line_no, "unbalanced_braces", "unbalanced curly braces"))
    if display:
        issues.append(MathIssue(max(1, len(text.splitlines())), "unclosed_display", "unclosed $$ display math"))
    return issues

def validate_file(path) -> dict:
    text = path.read_text(encoding="utf-8")
    issues = check_markdown(text)
    return {"passed": not issues, "issues": [issue.__dict__ for issue in issues]}

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser(); p.add_argument("--file", required=True)
    result = validate_file(__import__("pathlib").Path(p.parse_args().file))
    print(json.dumps(result, ensure_ascii=False, indent=2)); raise SystemExit(0 if result["passed"] else 1)
