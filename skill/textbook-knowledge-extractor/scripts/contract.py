"""Shared v2.3 audit contract used by runtime checkers.

Keep identifiers and enums here so validators do not silently drift.
"""
from __future__ import annotations

import re

AUDIT_SCHEMA_VERSION = "2.3"
BLOCK_ID_PATTERN = r"^K-[0-9]{3,}$"
BLOCK_ID_RE = re.compile(BLOCK_ID_PATTERN)
KNOWLEDGE_BLOCK_RE = re.compile(r"(?m)^\s*#{0,6}[ \t]*(K-[0-9]{3,})\b")
DECISIONS = {"include", "exclude"}
CONTAINER_TYPES = {
    "heading", "paragraph", "display_formula", "fenced_code", "callout",
    "html_table", "list", "other",
}
MIXED_ROLES = {"setup", "result", "statement", "derivation", "verification", "proof", "explanation", "callout"}
ARTIFACT_CATEGORIES = {"symbol_restoration", "word_restoration", "arrow_restoration", "label_loss", "order_artifact", "paragraph_fragment_merge", "tex_tip_removal", "kept_as_source", "other"}
ARTIFACT_ACTIONS = {"restore", "flag_only", "remove_noncontent", "merge_fragment", "preserve", "register_conflict"}
BOUNDARY_RELIABILITIES = {"high", "medium", "low", "unknown"}


def valid_block_id(value: object) -> bool:
    return isinstance(value, str) and BLOCK_ID_RE.fullmatch(value) is not None


def block_id_for_line(line: int) -> str:
    return f"K-{line:03d}"
