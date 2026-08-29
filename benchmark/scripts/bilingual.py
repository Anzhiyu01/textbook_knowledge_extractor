"""Bilingual first-occurrence checks for extraction submissions.

The benchmark deliberately performs a format-level check only.  It does not
try to decide whether a Chinese phrase is the *right* translation of an
English term; that semantic decision remains part of human review.  A term
record can optionally carry its expected English spelling and the source
block/line where its first occurrence is expected.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable
import sys
from pathlib import Path

_SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skill" / "textbook-knowledge-extractor" / "scripts"
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))

try:
    from contract import KNOWLEDGE_BLOCK_RE
except ImportError:  # pragma: no cover
    from .contract import KNOWLEDGE_BLOCK_RE


# Keep the token classes intentionally conservative.  They accept ordinary
# textbook terms (including spaces, apostrophes, slashes, and hyphens) while
# avoiding a parenthesised mathematical expression being mistaken for an
# English translation.
_ZH_TOKEN = r"[\u3400-\u4dbf\u4e00-\u9fff][\u3400-\u4dbf\u4e00-\u9fff·、，。！？：；（）《》“”‘’…-]*"
_EN_TOKEN = r"[A-Za-z][A-Za-z0-9]*(?:[ \t]+[A-Za-z0-9][A-Za-z0-9'./_-]*)*"

BILINGUAL_PAIR_RE = re.compile(
    rf"(?:{_ZH_TOKEN})[ \t]*[（(][ \t]*{_EN_TOKEN}[ \t]*[）)]"
    rf"|(?:{_EN_TOKEN})[ \t]*[（(][ \t]*{_ZH_TOKEN}[ \t]*[）)]"
)

_ZH_RUN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff][\u3400-\u4dbf\u4e00-\u9fff·-]*")
_BLOCK_ID_RE = KNOWLEDGE_BLOCK_RE

# Labels and generic nouns are not useful term candidates by themselves.  The
# list is deliberately small; explicit ``bilingual_terms`` always takes
# precedence over this fallback.
_GENERIC_TERM_PARTS = {
    "定义",
    "公理",
    "约定",
    "记号",
    "命题",
    "引理",
    "定理",
    "推论",
    "性质",
    "判别法",
    "恒等式",
    "公式",
    "构造",
    "例",
    "反例",
    "备注",
    "评注",
    "数列",
    "函数",
    "集合",
}


@dataclass(frozen=True)
class BilingualTerm:
    """Normalised term information read from ``audit.bilingual_terms``."""

    term: str
    english: str | None = None
    first_occurrence_line: int | None = None
    block_id: str | None = None
    explicit: bool = True


def _first_string(record: dict[str, Any], keys: Iterable[str]) -> str | None:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _first_int(record: dict[str, Any], keys: Iterable[str]) -> int | None:
    for key in keys:
        value = record.get(key)
        # bool is an int subclass but is not a meaningful line number.
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def _records_from_raw(raw: Any) -> tuple[list[dict[str, Any]], list[str]]:
    """Accept the documented list form plus lenient audit-friendly variants."""

    if raw is None:
        return [], []
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)], [
            "bilingual_terms entries must be objects" for item in raw if not isinstance(item, dict)
        ]
    if not isinstance(raw, dict):
        return [], ["bilingual_terms must be an array or object"]

    # Preferred container form: {"terms": [...]} ("items" is accepted for
    # compatibility with early hand-written audits).
    for key in ("terms", "items"):
        if key in raw:
            value = raw[key]
            if not isinstance(value, list):
                return [], [f"bilingual_terms.{key} must be an array"]
            return _records_from_raw(value)

    # A single record is convenient for tiny fixtures.
    if any(key in raw for key in ("term", "target_term", "chinese", "target")):
        return [raw], []

    # Finally accept a mapping keyed by the target-language term:
    # {"收敛": {"english": "convergence", ...}}.
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for term, value in raw.items():
        if not isinstance(term, str) or not term.strip():
            errors.append("bilingual_terms mapping keys must be non-empty strings")
            continue
        if isinstance(value, str):
            records.append({"term": term, "english": value})
        elif isinstance(value, dict):
            # The mapping key is the authoritative target-language term.  Do
            # not let an accidental nested ``term`` field silently replace it.
            records.append({**value, "term": term})
        else:
            errors.append(f"bilingual_terms entry for {term!r} must be an object or string")
    return records, errors


def normalise_terms(raw: Any) -> tuple[list[BilingualTerm], list[str]]:
    """Parse audit records and return terms plus deterministic format errors."""

    records, errors = _records_from_raw(raw)
    terms: list[BilingualTerm] = []
    for index, record in enumerate(records, start=1):
        term = _first_string(record, ("term", "target_term", "chinese", "target"))
        if not term:
            errors.append(f"bilingual_terms[{index}] is missing a non-empty term")
            continue
        english = _first_string(
            record,
            ("english", "source_term", "source", "translation", "source_text"),
        )
        line = _first_int(
            record,
            (
                "first_occurrence_line",
                "first_line",
                "knowledge_line",
                "line",
            ),
        )
        block_id = _first_string(record, ("block_id", "candidate_id"))
        terms.append(BilingualTerm(term, english, line, block_id, explicit=True))
    return terms, errors


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _normalise_english(value: str) -> str:
    return " ".join(value.casefold().split())


def _pair_at_first_occurrence(
    text: str,
    offset: int,
    term: BilingualTerm,
) -> bool:
    """Return whether a bilingual pair touches the first term occurrence.

    The opening parenthesis must be no more than eight characters after the
    target term (the reverse orientation is also accepted, with the same
    eight-character tolerance).  This makes the check match the benchmark's
    ``term + 8`` rule without requiring a particular bracket width.
    """

    term_end = offset + len(term.term)
    # Search the complete current line so a long English phrase cannot be
    # truncated by an arbitrary context limit.  The positional check below
    # still enforces the eight-character trigger window.
    window_start = text.rfind("\n", 0, offset) + 1
    newline = text.find("\n", term_end)
    window_end = len(text) if newline < 0 else newline
    for match in BILINGUAL_PAIR_RE.finditer(text, window_start, window_end):
        if not (match.start() <= offset + 8 and match.end() >= offset):
            continue
        # The pair may contain a longer Chinese phrase, but it must actually
        # contain this configured term rather than merely touching it.
        paired_text = match.group(0)
        term_rel = paired_text.find(term.term)
        if term_rel < 0:
            continue
        term_start = match.start() + term_rel
        # Locate the parenthesis that separates the two language sides.  The
        # regex guarantees one opening and one closing bracket, but accepting
        # either width makes mixed full-/half-width source material work too.
        open_rel = min(
            (index for index in (paired_text.find("（"), paired_text.find("(")) if index >= 0),
            default=-1,
        )
        if open_rel < 0:
            continue
        open_abs = match.start() + open_rel
        if term_start < open_abs:
            gap = open_abs - (offset + len(term.term))
        else:
            gap = offset - (open_abs + 1)
        if gap < 0 or gap > 8:
            continue
        if term.english:
            expected = _normalise_english(term.english)
            # Strip brackets and compare against the English-looking portions
            # of the pair.  A longer source phrase is allowed to contain the
            # configured term (e.g. ``convergence sequence``).
            english_parts = re.findall(r"[A-Za-z][A-Za-z0-9'./_-]*(?:[ \t]+[A-Za-z0-9][A-Za-z0-9'./_-]*)*", paired_text)
            if not any(expected in _normalise_english(part) for part in english_parts):
                continue
        return True
    return False


def _candidate_sections(knowledge: str) -> dict[str, tuple[int, int]]:
    matches = list(_BLOCK_ID_RE.finditer(knowledge))
    sections: dict[str, tuple[int, int]] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(knowledge)
        sections.setdefault(match.group(1), (start, end))
    return sections


def _first_occurrence(text: str, term: BilingualTerm, start: int, end: int) -> int:
    """Find the first term occurrence outside its own ``K-`` heading.

    A block identifier line can contain Chinese labels (for example
    ``K-009 定义：收敛数列``); those labels are metadata, not a translated
    occurrence.  Searching after the first newline avoids a false failure for
    the common heading-plus-body layout while retaining source order.
    """

    first = text.find(term.term, start, end)
    heading_end = text.find("\n", start, end)
    # Explicit audit terms describe the reader-facing terminology and thus
    # count a heading occurrence.  Inferred terms are more conservative: an
    # unpaired title label is metadata, while a paired heading is a valid first
    # occurrence.
    if first >= 0 and (heading_end < 0 or first < heading_end):
        if term.explicit or _pair_at_first_occurrence(text, first, term):
            return first
    body_start = heading_end
    if body_start >= 0:
        body_start += 1
    else:
        body_start = start
    return text.find(term.term, body_start, end)


def _first_term_occurrence(
    text: str,
    term: BilingualTerm,
    sections: dict[str, tuple[int, int]],
    *,
    restrict_to_sections: bool = False,
) -> tuple[int, str | None]:
    """Find a term's first occurrence in source order across included blocks."""

    if sections:
        ordered = sorted(sections.items(), key=lambda item: item[1][0])
        for block_id, (start, end) in ordered:
            offset = _first_occurrence(text, term, start, end)
            if offset >= 0:
                return offset, block_id
        return -1, None
    if restrict_to_sections:
        # An explicitly supplied empty allow-list means that no retained block
        # exists; do not fall back to searching headings or excluded material.
        return -1, None
    return _first_occurrence(text, term, 0, len(text)), None


def infer_terms(knowledge: str, included_block_ids: Iterable[str]) -> list[BilingualTerm]:
    """Infer one conservative target-language term per included block.

    This fallback is intentionally modest and is used only when strict mode is
    explicitly requested and no audit term table is present.  A block heading
    such as ``定义：收敛数列`` yields ``收敛``; otherwise the first non-mathematical
    Chinese run in the block is used.  Ambiguous blocks are skipped rather than
    fabricating a term.
    """

    sections = _candidate_sections(knowledge)
    inferred: list[BilingualTerm] = []
    for block_id in included_block_ids:
        span = sections.get(block_id)
        if not span:
            continue
        start, end = span
        block = knowledge[start:end]
        heading_end = block.find("\n")
        heading = block if heading_end < 0 else block[:heading_end]
        # Prefer the text after a heading colon; remove common generic suffixes
        # so ``收敛数列`` becomes the term ``收敛``.
        title = re.split(r"[：:]", heading, maxsplit=1)[-1]
        title = re.sub(r"^\s*(?:\d+(?:\.\d+)*[ \t]*)?", "", title)
        runs = _ZH_RUN_RE.findall(title)
        candidates = [run for run in runs if run not in _GENERIC_TERM_PARTS]
        if candidates:
            term_text = candidates[0]
            for suffix in ("数列", "函数", "集合", "定理", "性质", "构造"):
                if term_text.endswith(suffix) and len(term_text) > len(suffix):
                    term_text = term_text[: -len(suffix)]
                    break
            if term_text:
                # Only infer a term when the body actually contains it.  A
                # title-only label (``极限的唯一性``) is metadata and should
                # not create an impossible bilingual requirement.
                body_start = heading_end + 1 if heading_end >= 0 else 0
                local = block.find(term_text, body_start)
                if local < 0:
                    continue
                inferred.append(
                    BilingualTerm(
                        term_text,
                        first_occurrence_line=_line_number(knowledge, start + local),
                        block_id=block_id,
                        explicit=False,
                    )
                )
                continue
        # Fall back to the first Chinese run in body text, excluding the ID
        # heading itself and one-character labels.
        body = block[heading_end + 1 :] if heading_end >= 0 else block
        body_match = next((m for m in _ZH_RUN_RE.finditer(body) if len(m.group(0)) >= 2), None)
        if body_match:
            term_text = body_match.group(0)
            absolute = start + (heading_end + 1 if heading_end >= 0 else 0) + body_match.start()
            inferred.append(
                BilingualTerm(
                    term_text,
                    first_occurrence_line=_line_number(knowledge, absolute),
                    block_id=block_id,
                    explicit=False,
                )
            )
    return inferred


def validate_bilingual_terms(
    knowledge: str,
    terms: Iterable[BilingualTerm],
    included_block_ids: Iterable[str] | None = None,
) -> list[str]:
    """Validate first occurrences and return human-readable deterministic errors."""

    errors: list[str] = []
    sections = _candidate_sections(knowledge)
    restricted = included_block_ids is not None
    if included_block_ids is not None:
        allowed = set(included_block_ids)
        sections = {
            block_id: span for block_id, span in sections.items() if block_id in allowed
        }
    seen_terms: set[str] = set()
    for term in terms:
        # A term is required only at its first occurrence in the knowledge
        # list.  This matters when a later theorem repeats a term introduced
        # by an earlier definition.
        if term.term in seen_terms:
            continue
        seen_terms.add(term.term)
        offset, actual_block_id = _first_term_occurrence(
            knowledge, term, sections, restrict_to_sections=restricted
        )
        if offset < 0:
            errors.append(f"术语双语缺失: {term.term}（知识清单中未找到，块 {term.block_id or '全局'}）")
            continue
        actual_line = _line_number(knowledge, offset)
        if term.block_id and actual_block_id and term.block_id != actual_block_id:
            errors.append(
                f"术语首现块不一致: {term.term}（审计 {term.block_id}，实际 {actual_block_id}）"
            )
        if term.first_occurrence_line is not None and term.first_occurrence_line != actual_line:
            errors.append(
                f"术语首现行号不一致: {term.term}（审计 {term.first_occurrence_line}，实际 {actual_line}）"
            )
        if not _pair_at_first_occurrence(knowledge, offset, term):
            errors.append(f"术语双语缺失: {term.term}（knowledge.md 第 {actual_line} 行）")
    return errors
