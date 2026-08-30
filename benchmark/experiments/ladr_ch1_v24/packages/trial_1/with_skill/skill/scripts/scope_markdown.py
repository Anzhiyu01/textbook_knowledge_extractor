#!/usr/bin/env python3
"""Index Markdown headings, extract a verified chapter slice, and precheck.

The tool scans the source locally so the model only needs the compact heading
index before selecting a chapter. It ignores ATX headings inside fenced code.
An optional loose ATX mode recognises ``#``-prefixed lines without a space,
suspicious Setext headings are flagged, and ``precheck`` emits an advisory
integrity report without modifying the source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from contract import AUDIT_SCHEMA_VERSION, block_id_for_line


ATX_HEADING = re.compile(r"^( {0,3})(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
# Loose mode: the marker is followed directly by a non-``#``, non-whitespace
# character (e.g. ``#第1章``).  Strict matches win when both would apply, and
# loose records are tagged so callers know the match is less reliable.
LOOSE_ATX_HEADING = re.compile(r"^( {0,3})(#{1,6})([^\s#].*?)[ \t]*#*[ \t]*$")
SETEXT_UNDERLINE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
FENCE = re.compile(r"^ {0,3}((?:\x60){3,}|~{3,})(.*)$")

# A Setext underline whose source line ends with sentence punctuation, or
# contains two or more sentence terminators, is likely prose followed by a
# ``---`` separator rather than a real heading.  Advisory only.
SENTENCE_END_RE = re.compile(r"[。．.!?！？…\"”'」』）)\]】]\s*$")
MULTI_SENTENCE_RE = re.compile(r"[。．.!?！？…].*[。．.!?！？…]")

# Precheck signals.  Numbered headings use a dotted decimal prefix; bare
# chapter lines are text that looks like a chapter/section marker but is not
# an indexed heading.
NUMBERED_HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*)")
# Common OCR/conversion remnants caused by dropped ``fi``/``ffi`` ligatures.
# This is intentionally a conservative vocabulary: precheck is advisory and
# must never rewrite source text or classify arbitrary spellings as errors.
LIGATURE_DAMAGE_RE = re.compile(
    r"\b(?:defnition|defne|fnite|felds?|frst|fgure|diferent(?:iable)?|"
    r"satisfes|infnite|coefcients?|specif(?:cally|ed)|complexifcation|fnding)\b",
    re.IGNORECASE,
)
# References to a numbered item whose heading is absent are a useful signal
# for a conversion that dropped the item's label while keeping its content.
NUMBERED_REFERENCE_RE = re.compile(
    r"\b(?:see|参见|见)\s+(?:definition|example|theorem|proposition|remark|"
    r"定义|例|定理|命题|评注)?\s*(\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)
BARE_CHAPTER_RE = re.compile(
    r"^(?:第[一二三四五六七八九十百千〇0-9]+[章节]|Chapter\s+\d+|Section\s+\d+(?:\.\d+)*\b)",
    re.IGNORECASE,
)

# ``--start-heading``/``--end-before-heading`` tolerate a leading ATX marker
# and surrounding whitespace; exact index text always wins first.
HEADING_MARKER_PREFIX_RE = re.compile(r"^\s*#{1,6}[ \t]*")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str
    next_prefix: str | None = None
    kind: str = "atx"
    matched_by: str = "strict"
    suspicious: bool = False


def read_source(path: Path) -> tuple[bytes, list[str]]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"source is not UTF-8/UTF-8-BOM: {exc}") from exc
    return raw, text.splitlines()


def compact_prefix(lines: list[str], start: int, limit: int) -> str | None:
    for line in lines[start:]:
        stripped = line.strip()
        if stripped:
            return stripped[:limit]
    return None


def is_suspicious_setext(text: str) -> bool:
    """Return whether a Setext source line looks like prose, not a heading."""
    stripped = text.strip()
    if not stripped:
        return False
    if SENTENCE_END_RE.search(stripped):
        return True
    return bool(MULTI_SENTENCE_RE.search(stripped))


def index_headings(
    lines: list[str], preview_chars: int, loose_atx: bool = False
) -> list[Heading]:
    headings: list[Heading] = []
    fence_char: str | None = None
    fence_len = 0
    for offset, line in enumerate(lines):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is not None:
            continue
        match = ATX_HEADING.match(line)
        if match:
            prefix = (
                compact_prefix(lines, offset + 1, preview_chars)
                if preview_chars
                else None
            )
            headings.append(
                Heading(
                    line=offset + 1,
                    level=len(match.group(2)),
                    text=match.group(3).strip(),
                    next_prefix=prefix,
                    kind="atx",
                    matched_by="strict",
                )
            )
            continue
        if loose_atx:
            loose = LOOSE_ATX_HEADING.match(line)
            if loose:
                prefix = (
                    compact_prefix(lines, offset + 1, preview_chars)
                    if preview_chars
                    else None
                )
                headings.append(
                    Heading(
                        line=offset + 1,
                        level=len(loose.group(2)),
                        text=loose.group(3).strip(),
                        next_prefix=prefix,
                        kind="atx",
                        matched_by="loose",
                    )
                )
                continue
        setext = SETEXT_UNDERLINE.match(line)
        if setext and offset > 0:
            previous = lines[offset - 1].strip()
            previous_is_atx = bool(ATX_HEADING.match(lines[offset - 1])) or (
                loose_atx and bool(LOOSE_ATX_HEADING.match(lines[offset - 1]))
            )
            if previous and not previous_is_atx:
                prefix = (
                    compact_prefix(lines, offset + 1, preview_chars)
                    if preview_chars
                    else None
                )
                headings.append(
                    Heading(
                        line=offset,
                        level=1 if setext.group(1).startswith("=") else 2,
                        text=previous,
                        next_prefix=prefix,
                        kind="setext",
                        matched_by="strict",
                        suspicious=is_suspicious_setext(previous),
                    )
                )
    return headings


def probe_lines(
    lines: list[str], pattern: re.Pattern[str], prefix_chars: int, max_matches: int
) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    fence_char: str | None = None
    fence_len = 0
    for offset, line in enumerate(lines):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is None and pattern.search(line):
            matches.append({"line": offset + 1, "prefix": line.strip()[:prefix_chars]})
            if len(matches) >= max_matches:
                break
    return matches


def normalize_heading_text(text: str) -> str:
    """Strip an optional ATX marker and surrounding whitespace from a query.

    Index text remains the only canonical form; this fallback only makes
    user-supplied parameters such as ``"## 第一章 数列"`` or trailing spaces
    resolve to the same heading.
    """
    return HEADING_MARKER_PREFIX_RE.sub("", text).strip()


def _find_heading(headings: list[Heading], text: str) -> list[Heading]:
    """Exact heading matches first, then marker/whitespace-tolerant matches."""
    matches = [heading for heading in headings if heading.text == text]
    if matches:
        return matches
    normalized = normalize_heading_text(text)
    if normalized != text:
        return [heading for heading in headings if heading.text == normalized]
    return []


def resolve_heading(headings: list[Heading], text: str, occurrence: int) -> Heading:
    matches = _find_heading(headings, text)
    if not matches:
        raise ValueError(f"heading not found: {text!r}")
    if occurrence < 1 or occurrence > len(matches):
        raise ValueError(
            f"heading {text!r} has {len(matches)} occurrence(s), "
            f"requested occurrence {occurrence}"
        )
    return matches[occurrence - 1]


def resolve_range(
    headings: list[Heading],
    line_count: int,
    start_text: str,
    start_occurrence: int,
    end_before_text: str | None,
    end_occurrence: int,
) -> tuple[Heading, Heading | None, int]:
    start = resolve_heading(headings, start_text, start_occurrence)
    following = [heading for heading in headings if heading.line > start.line]
    if end_before_text:
        matches = _find_heading(following, end_before_text)
        if not matches:
            raise ValueError(
                f"end-before heading not found after start: {end_before_text!r}"
            )
        if end_occurrence < 1 or end_occurrence > len(matches):
            raise ValueError(
                f"end-before heading {end_before_text!r} has {len(matches)} "
                f"occurrence(s) after start, requested {end_occurrence}"
            )
        end_heading = matches[end_occurrence - 1]
    else:
        end_heading = next(
            (heading for heading in following if heading.level <= start.level),
            None,
        )
    end_line = end_heading.line - 1 if end_heading else line_count
    if end_line < start.line:
        raise ValueError("resolved range is empty")
    return start, end_heading, end_line


def validate_line_range(
    start_line: int, end_line: int, line_count: int
) -> tuple[int, int]:
    """Validate a 1-based, inclusive line range against the source."""
    if line_count < 1:
        raise ValueError("source contains no lines")
    if not 1 <= start_line <= line_count:
        raise ValueError(f"start line {start_line} is outside source (1..{line_count})")
    if not 1 <= end_line <= line_count:
        raise ValueError(f"end line {end_line} is outside source (1..{line_count})")
    if start_line > end_line:
        raise ValueError(
            f"line range is reversed: start line {start_line} > end line {end_line}"
        )
    return start_line, end_line


def line_is_inside_fence(lines: list[str], line_number: int) -> bool:
    """Return whether a 1-based line is inside a fenced code block.

    The state transition intentionally mirrors ``index_headings`` and
    ``probe_lines``: a fence marker opens/closes the state for subsequent
    lines, so an opening marker itself is not considered inside while a
    closing marker is.
    """
    if line_number < 1 or line_number > len(lines):
        raise ValueError(
            f"line number {line_number} is outside source (1..{len(lines)})"
        )
    fence_char: str | None = None
    fence_len = 0
    for offset, line in enumerate(lines, start=1):
        if offset == line_number:
            return fence_char is not None
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
    return False


def source_position(lines: list[str], start_line: int, end_line: int) -> dict[str, object]:
    """Describe a candidate span using the v2.2 marker-line convention.

    The marker line is always the first line of the supplied span.  Content
    starts after fenced/callout/table markers and otherwise at the marker line.
    """
    validate_line_range(start_line, end_line, len(lines))
    first = lines[start_line - 1].strip()
    last = lines[end_line - 1].strip()
    if FENCE.match(lines[start_line - 1]):
        ctype, content_start = "fenced_code", min(start_line + 1, end_line)
    elif first.startswith("> [!"):
        ctype, content_start = "callout", min(start_line + 1, end_line)
    elif re.match(r"<(?:table|tr)(?:\s|>)", first, re.IGNORECASE):
        ctype, content_start = "html_table", min(start_line + 1, end_line)
    elif ATX_HEADING.match(lines[start_line - 1]) or LOOSE_ATX_HEADING.match(lines[start_line - 1]):
        ctype, content_start = "heading", start_line
    elif first.startswith("$$") or first.startswith("\\["):
        ctype, content_start = "display_formula", start_line
    elif first.startswith("-") or first.startswith("*") or first.startswith("1."):
        ctype, content_start = "list", start_line
    else:
        ctype, content_start = "paragraph", start_line
    content_end = end_line
    if ctype == "fenced_code" and end_line > start_line and FENCE.match(lines[end_line - 1]):
        content_end = end_line - 1
    elif ctype == "html_table" and re.match(r"</table>\s*$", last, re.IGNORECASE):
        content_end = max(start_line, end_line - 1)
    return {
        "container_type": ctype,
        "marker_start_line": start_line,
        "marker_end_line": end_line,
        "content_start_line": content_start,
        "content_end_line": content_end,
    }


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def command_index(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    raw, lines = read_source(source)
    loose_atx = getattr(args, "loose_atx", False)
    headings = index_headings(lines, args.preview_chars, loose_atx=loose_atx)
    payload = {
        "source_file": str(source),
        "source_sha256": sha256(raw),
        "line_count": len(lines),
        "heading_count": len(headings),
        "headings": [asdict(heading) for heading in headings],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def discover_candidates(lines: list[str], start_line: int = 1, end_line: int | None = None) -> list[dict[str, object]]:
    """Generate a deterministic, source-derived inventory for a slice."""
    end_line = end_line or len(lines)
    rows: list[dict[str, object]] = []
    i = start_line - 1
    while i < end_line:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        start = i + 1
        kind = "paragraph"
        signal = "paragraph"
        j = i
        if FENCE.match(line):
            marker = FENCE.match(line).group(1)
            kind, signal = "fenced_code", "formula_fence" if "math" in line.lower() or "$" in line else "fence"
            j += 1
            while j < end_line and not (FENCE.match(lines[j]) and FENCE.match(lines[j]).group(1)[0] == marker[0]):
                j += 1
            if j < end_line:
                j += 1
        elif ATX_HEADING.match(line) or LOOSE_ATX_HEADING.match(line):
            kind = "heading"
            heading_text = (ATX_HEADING.match(line) or LOOSE_ATX_HEADING.match(line)).group(3 if ATX_HEADING.match(line) else 3).strip()
            signal = "exclusion_heading" if re.match(r"(?:proof|证明|exercises?|习题)\b", heading_text, re.I) else "heading"
        elif re.match(r"^\s*(?:\$\$|\\\[|\\begin\{|```(?:math|latex))", line, re.I):
            kind, signal = "display_formula", "formula_container"
            if stripped == "$$":
                j += 1
                while j < end_line and lines[j].strip() != "$$":
                    j += 1
                if j < end_line:
                    j += 1
        elif re.match(r"^\s*(?:>\s*\[!|>\s*|\[!)[A-Za-z]+", line):
            kind, signal = "callout", "callout"
        elif re.match(r"^\s*(?:<table\b|<tr\b)", line, re.I):
            kind, signal = "html_table", "html_table"
            while j + 1 < end_line and lines[j + 1].strip():
                j += 1
                if re.search(r"</table>\s*$", lines[j], re.I):
                    break
        elif re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line):
            kind, signal = "list", "list_or_numbered"
        elif re.match(r"^\s*(?:\d+(?:\.\d+)+|(?:Proof|证明|Exercises?|习题)\b)", line, re.I):
            kind, signal = "paragraph", "bare_number_or_exclusion_label"
        else:
            while j + 1 < end_line and lines[j + 1].strip():
                nxt = lines[j + 1]
                if (ATX_HEADING.match(nxt) or LOOSE_ATX_HEADING.match(nxt) or
                    FENCE.match(nxt) or re.match(r"^\s*(?:\d+(?:\.\d+)+|(?:Proof|证明|Exercises?|习题)\b)", nxt, re.I)):
                    break
                j += 1
        text = "\n".join(lines[i:j + 1])
        rows.append({
            "block_id": block_id_for_line(start),
            "source_start_line": start,
            "source_end_line": j + 1,
            "container_type": kind,
            "signal": signal,
            "text_anchor": stripped[:160],
        })
        i = j + 1
    return rows


def command_candidates(args: argparse.Namespace) -> int:
    slice_path = args.slice.resolve()
    raw, lines = read_source(slice_path)
    rows = discover_candidates(lines)
    source_offset = max(0, args.source_start_line - 1)
    if source_offset:
        for row in rows:
            row["source_start_line"] = int(row["source_start_line"]) + source_offset
            row["source_end_line"] = int(row["source_end_line"]) + source_offset
            row["block_id"] = block_id_for_line(int(row["source_start_line"]))
    payload = {
        "candidate_index_version": AUDIT_SCHEMA_VERSION,
        "slice_file": str(slice_path),
        "slice_sha256": sha256(raw),
        "slice_line_count": len(lines),
        "generator_version": AUDIT_SCHEMA_VERSION,
        "candidates": rows,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.manifest:
        args.manifest.resolve().parent.mkdir(parents=True, exist_ok=True)
        args.manifest.resolve().write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0


def command_extract(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    output = args.output.resolve()
    raw, lines = read_source(source)

    # ``getattr`` keeps direct callers that construct the pre-M1 Namespace
    # compatible while the CLI always supplies these attributes.
    start_line_arg = getattr(args, "start_line", None)
    end_line_arg = getattr(args, "end_line", None)
    start_heading_arg = getattr(args, "start_heading", None)
    end_heading_arg = getattr(args, "end_before_heading", None)
    start_occurrence = getattr(args, "start_occurrence", 1)
    end_occurrence = getattr(args, "end_occurrence", 1)
    manifest_arg = getattr(args, "manifest", None)

    if start_line_arg is not None and start_heading_arg is not None:
        raise ValueError("use either --start-line or --start-heading, not both")
    if end_line_arg is not None and end_heading_arg is not None:
        raise ValueError("use either --end-line or --end-before-heading, not both")

    start: Heading | None = None
    end_heading: Heading | None = None
    if start_line_arg is not None:
        # A line-selected range is deliberately independent of heading parsing;
        # this is the fallback for probe results and non-heading boundaries.
        if end_line_arg is None:
            raise ValueError("--end-line is required when --start-line is used")
        start_line, end_line = validate_line_range(
            start_line_arg, end_line_arg, len(lines)
        )
        if line_is_inside_fence(lines, start_line):
            raise ValueError(f"start line {start_line} is inside a fenced code block")
        selection_method = "explicit-line-range"
    else:
        if start_heading_arg is None:
            raise ValueError("one of --start-heading or --start-line is required")
        headings = index_headings(lines, 0)
        if end_line_arg is not None:
            start = resolve_heading(headings, start_heading_arg, start_occurrence)
            start_line, end_line = validate_line_range(
                start.line, end_line_arg, len(lines)
            )
            selection_method = "explicit-line-range"
        else:
            start, end_heading, end_line = resolve_range(
                headings,
                len(lines),
                start_heading_arg,
                start_occurrence,
                end_heading_arg,
                end_occurrence,
            )
            start_line = start.line
            selection_method = (
                "explicit-end-heading"
                if end_heading_arg
                else "next-heading-at-same-or-higher-level"
            )

    # Advisory only: a Setext underline under prose is often a ``---``
    # separator, not a real heading.  Warn without changing the cut.
    if start is not None and start.suspicious:
        print(
            f"WARNING: start heading {start.text!r} (line {start.line}) looks "
            f"like a suspicious Setext heading; the slice is still cut as resolved",
            file=sys.stderr,
        )
    if end_heading is not None and end_heading.suspicious:
        print(
            f"WARNING: end heading {end_heading.text!r} (line {end_heading.line}) "
            f"looks like a suspicious Setext heading; the slice is still cut as resolved",
            file=sys.stderr,
        )

    selected = lines[start_line - 1 : end_line]
    slice_text = "\n".join(selected) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(slice_text, encoding="utf-8", newline="\n")
    manifest = {
        "source_file": str(source),
        "source_sha256": sha256(raw),
        "source_line_count": len(lines),
        "start_heading": asdict(start) if start else None,
        "end_before_heading": asdict(end_heading) if end_heading else None,
        "start_line": start_line,
        "end_line": end_line,
        "slice_file": str(output),
        "slice_sha256": sha256(slice_text.encode("utf-8")),
        "slice_line_count": len(selected),
        "selection_method": selection_method,
        "start_is_heading": start is not None,
        "end_is_heading": end_heading is not None,
        "boundary_source_positions": {
            "start": source_position(lines, start_line, start_line),
            "end": source_position(lines, end_line, end_line),
        },
    }
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2)
    if manifest_arg:
        manifest_path = Path(manifest_arg).resolve()
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)
    return 0


def command_probe(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    raw, lines = read_source(source)
    try:
        pattern = re.compile(args.pattern, re.IGNORECASE if args.ignore_case else 0)
    except re.error as exc:
        raise ValueError(f"invalid probe pattern: {exc}") from exc
    matches = probe_lines(lines, pattern, args.prefix_chars, args.max_matches + 1)
    truncated = len(matches) > args.max_matches
    payload = {
        "source_file": str(source),
        "source_sha256": sha256(raw),
        "line_count": len(lines),
        "pattern": args.pattern,
        "truncated": truncated,
        "matches": matches[: args.max_matches],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def _line_in_range(line: int, start_line: int | None, end_line: int | None) -> bool:
    return (start_line is None or line >= start_line) and (end_line is None or line <= end_line)


def precheck_source(
    lines: list[str], start_line: int | None = None, end_line: int | None = None
) -> list[dict[str, object]]:
    """Emit advisory integrity warnings for a textbook source.

    The report is for the AI to decide whether to stop, run ``probe``, or
    proceed with a looser boundary tool.  It never modifies the source and
    never blocks extraction.
    """

    warnings: list[dict[str, object]] = []
    if (start_line is None) != (end_line is None):
        raise ValueError("start_line and end_line must be provided together")
    if start_line is not None and end_line is not None:
        validate_line_range(start_line, end_line, len(lines))
    headings = index_headings(lines, 0)
    scoped_headings = [h for h in headings if _line_in_range(h.line, start_line, end_line)]

    # 1. Heading level jumps (e.g. ``#`` straight to ``###``).
    for previous, current in zip(scoped_headings, scoped_headings[1:]):
        if current.level > previous.level + 1:
            warnings.append(
                {
                    "type": "heading_level_jump",
                    "line": current.line,
                    "message": (
                        f"heading level jumps from {previous.level} to {current.level} "
                        f"at line {current.line}: {current.text!r}"
                    ),
                }
            )

    # 2. Numbering continuity within the same parent (1.1 -> 1.3 misses 1.2).
    last_number: tuple[int, ...] | None = None
    last_text = ""
    last_section: tuple[int, ...] | None = None
    for heading in scoped_headings:
        # Continuity is meaningful only among headings at the same structural
        # level and parent.  Reset at a new top-level section/chapter.
        match = NUMBERED_HEADING_RE.match(heading.text)
        if not match:
            continue
        parts = tuple(int(part) for part in match.group(1).split("."))
        if last_number is not None and len(parts) != len(last_number):
            last_number = None
            last_text = ""
        if (
            last_number is not None
            and parts[:-1] == last_number[:-1]
            and parts[-1] > last_number[-1] + 1
        ):
            parent = ".".join(str(part) for part in parts[:-1])
            first_missing = (
                f"{parent}.{last_number[-1] + 1}"
                if parent
                else str(last_number[-1] + 1)
            )
            last_missing = f"{parent}.{parts[-1] - 1}" if parent else str(parts[-1] - 1)
            span = (
                first_missing
                if first_missing == last_missing
                else f"{first_missing}..{last_missing}"
            )
            warnings.append(
                {
                    "type": "numbering_gap",
                    "line": heading.line,
                    "message": (
                        f"numbering jumps from {last_text!r} to {heading.text!r} "
                        f"(missing {span})"
                    ),
                }
            )
        last_number = parts
        last_text = heading.text

    # 3. Bare chapter-like lines that are not indexed headings.
    heading_lines = {heading.line for heading in headings}
    fence_char: str | None = None
    fence_len = 0
    fence_open_line = 0
    for offset, line in enumerate(lines, start=1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
                fence_open_line = offset
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is not None:
            continue
        if offset in heading_lines:
            continue
        stripped = line.strip()
        if stripped and _line_in_range(offset, start_line, end_line) and BARE_CHAPTER_RE.match(stripped):
            # Directory/index pages commonly contain bare chapter labels and
            # should be advisory only rather than a boundary-loss signal.
            directory_like = bool(re.search(r"(?:\.\.\.|……|\.{2,})\s*\d+\s*$", stripped))
            warnings.append(
                {
                    "type": "bare_chapter_marker",
                    "line": offset,
                    "confidence": "low" if directory_like else "medium",
                    "directory_like": directory_like,
                    "message": (
                        f"chapter-like text is not an indexed heading: "
                        f"{stripped[:40]!r}; use probe --pattern to locate it, "
                        f"then extract --start-line"
                    ),
                }
            )

    # 4. Unclosed fenced code block.
    if fence_char is not None:
        warnings.append(
            {
                "type": "unclosed_fence",
                "line": fence_open_line,
                "message": (
                    f"fenced code block opened at line {fence_open_line} "
                    f"with {fence_char * fence_len} is never closed"
                ),
            }
        )

    # 5. U+FFFD replacement characters.
    scan_lines = lines[(start_line - 1 if start_line else 0) : end_line if end_line else len(lines)]
    replacement_total = sum(line.count("\ufffd") for line in scan_lines)
    if replacement_total:
        first_line = next(
            (i for i, line in enumerate(lines, start=1) if _line_in_range(i, start_line, end_line) and "\ufffd" in line),
            1,
        )
        warnings.append(
            {
                "type": "replacement_char",
                "line": first_line,
                "message": (
                    f"{replacement_total} U+FFFD replacement character(s) found "
                    f"(first on line {first_line}); the source may be corrupted"
                ),
            }
        )

    # 6. Literal question-mark placeholders and common ligature damage.
    # Scan outside fenced code blocks so examples containing source code do
    # not inflate the source-integrity report.
    placeholder_lines: list[int] = []
    ligature_hits: list[tuple[int, str]] = []
    fence_char = None
    fence_len = 0
    for offset, line in enumerate(lines, start=1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is not None:
            continue
        if _line_in_range(offset, start_line, end_line) and "?" in line:
            placeholder_lines.append(offset)
        if _line_in_range(offset, start_line, end_line):
            for match in LIGATURE_DAMAGE_RE.finditer(line):
                ligature_hits.append((offset, match.group(0)))
    if placeholder_lines:
        warnings.append(
            {
                "type": "placeholder_question_mark",
                "line": placeholder_lines[0],
                "count": sum(lines[line - 1].count("?") for line in placeholder_lines),
                "message": (
                    f"literal '?' placeholder(s) found on {len(placeholder_lines)} line(s) "
                    f"(first on line {placeholder_lines[0]}); do not silently restore"
                ),
            }
        )
    if ligature_hits:
        examples = ", ".join(f"{token}@{line}" for line, token in ligature_hits[:8])
        warnings.append(
            {
                "type": "ligature_damage",
                "line": ligature_hits[0][0],
                "count": len(ligature_hits),
                "message": (
                    f"possible fi/ffi ligature-loss token(s) ({examples}); "
                    "record any restoration in audit.source_artifacts"
                ),
            }
        )

    # 7. Numbered-item label loss signal.  A reference to 1.x without a
    # corresponding indexed heading is evidence that the label may have been
    # dropped during conversion.  The warning requests a manual ledger entry;
    # it does not invent a number or alter the candidate inventory.
    indexed_numbers = {
        match.group(1)
        for heading in headings
        if (match := NUMBERED_HEADING_RE.match(heading.text))
    }
    missing_references: list[tuple[int, str]] = []
    fence_char = None
    fence_len = 0
    for offset, line in enumerate(lines, start=1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = None, 0
            continue
        if fence_char is not None:
            continue
        if not _line_in_range(offset, start_line, end_line):
            continue
        for match in NUMBERED_REFERENCE_RE.finditer(line):
            target = match.group(1)
            # Cross-chapter references are not label-loss evidence when the
            # target exists anywhere in the source heading index.
            if target not in indexed_numbers:
                missing_references.append((offset, match.group(1)))
    if missing_references:
        unique = []
        seen = set()
        for line, number in missing_references:
            if number not in seen:
                unique.append(f"{number}@{line}")
                seen.add(number)
        warnings.append(
            {
                # Keep the v2.1 type for consumers while making the advisory
                # nature explicit through confidence/possible fields.
                "type": "numbering_label_loss",
                "possible": True,
                "confidence": "low",
                "line": missing_references[0][0],
                "count": len(missing_references),
                "message": (
                    "reference(s) target number(s) with no indexed heading "
                    f"({', '.join(unique[:8])}); inspect nearby unnumbered content "
                    "and register any label loss explicitly"
                ),
            }
        )

    return warnings


def command_precheck(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    raw, lines = read_source(source)
    if args.mode in {"slice", "both"} and (args.start_line is None or args.end_line is None):
        raise ValueError("--start-line and --end-line are required for mode=slice/both")
    if args.mode == "whole" and (args.start_line is not None or args.end_line is not None):
        raise ValueError("--start-line/--end-line require mode=slice or mode=both")
    modes = [args.mode] if args.mode != "both" else ["whole", "slice"]
    reports: dict[str, list[dict[str, object]]] = {}
    for mode in modes:
        if mode == "slice":
            reports[mode] = precheck_source(lines, args.start_line, args.end_line)
        else:
            reports[mode] = precheck_source(lines)
    warnings = reports[args.mode] if args.mode != "both" else [w for rows in reports.values() for w in rows]
    payload = {
        "source_file": str(source),
        "source_sha256": sha256(raw),
        "line_count": len(lines),
        "warning_count": len(warnings),
        "warnings": warnings,
        "mode": args.mode,
        "reports": reports if args.mode == "both" else None,
        "note": "advisory report only; the source is never modified",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    index = subparsers.add_parser("index", help="emit a compact heading index")
    index.add_argument("--source", required=True, type=Path)
    index.add_argument(
        "--preview-chars",
        type=int,
        default=0,
        choices=range(0, 161),
        metavar="0..160",
        help="include at most this many characters from the next nonblank line",
    )
    index.add_argument(
        "--loose-atx",
        action="store_true",
        help=(
            "also accept ATX headings whose marker is not followed by a space "
            "(e.g. '#第1章'); such records are tagged matched_by=loose"
        ),
    )
    index.set_defaults(func=command_index)

    candidates = subparsers.add_parser(
        "candidates", help="generate a deterministic candidate inventory from a slice"
    )
    candidates.add_argument("--slice", required=True, type=Path)
    candidates.add_argument("--manifest", type=Path)
    candidates.add_argument("--source-start-line", type=int, default=1, help="1-based source line corresponding to slice line 1")
    candidates.set_defaults(func=command_candidates)

    probe = subparsers.add_parser(
        "probe", help="emit bounded prefixes only for lines matching a chapter marker"
    )
    probe.add_argument("--source", required=True, type=Path)
    probe.add_argument("--pattern", required=True)
    probe.add_argument("--ignore-case", action="store_true")
    probe.add_argument("--prefix-chars", type=int, default=80, choices=range(1, 161))
    probe.add_argument("--max-matches", type=int, default=200, choices=range(1, 501))
    probe.set_defaults(func=command_probe)

    precheck = subparsers.add_parser(
        "precheck",
        help="emit advisory integrity warnings (headings, numbering, fences, "
        "bare chapter lines, replacement chars, placeholders, ligature damage) "
        "without modifying the source",
    )
    precheck.add_argument("--source", required=True, type=Path)
    precheck.add_argument("--mode", choices=["whole", "slice", "both"], default="whole")
    precheck.add_argument("--start-line", type=int, help="slice start line (required for mode=slice/both)")
    precheck.add_argument("--end-line", type=int, help="slice end line (required for mode=slice/both)")
    precheck.set_defaults(func=command_precheck)

    extract = subparsers.add_parser("extract", help="write a verified chapter slice")
    extract.add_argument("--source", required=True, type=Path)
    extract.add_argument(
        "--start-heading",
        help=(
            "heading text used as the start boundary (omit for line ranges); "
            "a leading '#{1,6}' marker and surrounding whitespace are tolerated"
        ),
    )
    extract.add_argument("--start-occurrence", type=int, default=1)
    extract.add_argument(
        "--end-before-heading",
        help="heading text before which the slice ends; marker/whitespace tolerant",
    )
    extract.add_argument("--end-occurrence", type=int, default=1)
    extract.add_argument(
        "--start-line",
        type=int,
        help="1-based inclusive start line; requires --end-line",
    )
    extract.add_argument(
        "--end-line",
        type=int,
        help="1-based inclusive end line",
    )
    extract.add_argument("--output", required=True, type=Path)
    extract.add_argument("--manifest", type=Path)
    extract.set_defaults(func=command_extract)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
