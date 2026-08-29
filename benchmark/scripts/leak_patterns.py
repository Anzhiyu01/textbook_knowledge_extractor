"""Shared heading-leak patterns used by the validator and sample scorer.

The extraction output may be translated, so proof and exercise headings can
contain a source-language label, a target-language label, punctuation, or an
item number.  Keep these expressions in one module so the validator and the
development scorer cannot silently disagree about contamination.
"""

from __future__ import annotations

import re


# The optional heading marker intentionally accepts both ``## Proof`` and a
# bare ``Proof`` line, preserving the old validator's behaviour.  ``proof``
# uses a word boundary so a prose heading such as ``Proofreading`` is not
# treated as a proof section, while the Chinese marker is a prefix because
# forms such as ``证明细节`` are common.
PROOF_LEAK_RE = re.compile(
    r"^[ \t]*#{0,6}[ \t]*(?:proof\b|证明)[^\r\n]*\r?$",
    re.IGNORECASE | re.MULTILINE,
)

# ``习题`` is included in addition to ``课后习题`` because bilingual output
# commonly uses ``习题 (Exercises)``.  The English alternative is bounded so
# unrelated words such as ``exercised`` do not trigger a leak.
EXERCISE_LEAK_RE = re.compile(
    r"^[ \t]*#{0,6}[ \t]*(?:exercises?\b|课后习题|习题)[^\r\n]*\r?$",
    re.IGNORECASE | re.MULTILINE,
)

# Descriptive aliases make the public names easy to discover for callers that
# previously kept their own local expression.
PROOF_HEADING_RE = PROOF_LEAK_RE
EXERCISE_HEADING_RE = EXERCISE_LEAK_RE


def proof_leak_matches(text: str) -> list[re.Match[str]]:
    """Return all proof-heading matches in *text*."""

    return list(PROOF_LEAK_RE.finditer(text))


def exercise_leak_matches(text: str) -> list[re.Match[str]]:
    """Return all exercise-heading matches in *text*."""

    return list(EXERCISE_LEAK_RE.finditer(text))
