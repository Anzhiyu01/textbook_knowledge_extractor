"""Deterministic, ASCII-only output package naming."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

_VALID = re.compile(r"^extraction_[a-z0-9]+(?:_[a-z0-9]+)*$")

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")

def source_slug(source: Path, supplied: str | None = None, metadata_title: str | None = None) -> str:
    for value in (supplied, metadata_title):
        if value and slugify(value):
            return slugify(value)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:8]
    return f"source_{digest}"

def chapter_slug(number: int | str | None = None, start: int | None = None, end: int | None = None) -> str:
    if start is not None and end is not None and start != end:
        return f"chapter_{start}_to_{end}"
    if number is None:
        raise ValueError("chapter number is required")
    return f"chapter_{int(number)}"

def package_name(source: Path, chapter: str, supplied_source_slug: str | None = None, metadata_title: str | None = None) -> str:
    name = f"extraction_{source_slug(source, supplied_source_slug, metadata_title)}_{slugify(chapter)}"
    if not _VALID.fullmatch(name):
        raise ValueError(f"invalid output package name: {name}")
    return name

def next_available(root: Path, name: str) -> Path:
    candidate = root / name
    if not candidate.exists() or not any(candidate.iterdir()):
        return candidate
    index = 2
    while True:
        candidate = root / f"{name}_run_{index}"
        if not candidate.exists() or not any(candidate.iterdir()):
            return candidate
        index += 1

def create_run_package(root: Path, source: Path, chapter: str, *, source_slug_value: str | None = None, metadata_title: str | None = None) -> Path:
    """Create an isolated v2.4 package skeleton without overwriting prior runs."""
    name = package_name(source, chapter, source_slug_value, metadata_title)
    target = next_available(root, name); (target / "work").mkdir(parents=True)
    (target / "knowledge.md").write_text("", encoding="utf-8")
    (target / "audit.json").write_text(json.dumps({"audit_schema_version":"2.4","resolved_defaults":{"language":"zh","bilingual":True,"output_directory":str(target)},"output_package":{"path":str(target)},"render_validation":{"status":"pending"}}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (target / "runlog.md").write_text("# Run log\n", encoding="utf-8")
    for name in ("slice.md", "scope.json", "candidate_index.json", "math_check.json"):
        (target / "work" / name).write_text("{}\n" if name.endswith(".json") else "", encoding="utf-8")
    return target
