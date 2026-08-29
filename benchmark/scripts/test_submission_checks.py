#!/usr/bin/env python3
"""Focused regression tests for M5/M6 submission checks."""

from __future__ import annotations

import unittest

try:
    from bilingual import BilingualTerm, validate_bilingual_terms
    from leak_patterns import EXERCISE_LEAK_RE, PROOF_LEAK_RE
    from score_sample import _fragment_hit
except ImportError:  # pragma: no cover - package-style test invocation
    from .bilingual import BilingualTerm, validate_bilingual_terms
    from .leak_patterns import EXERCISE_LEAK_RE, PROOF_LEAK_RE
    from .score_sample import _fragment_hit


class LeakPatternTests(unittest.TestCase):
    def test_proof_bilingual_and_tolerant_variants(self) -> None:
        leaking = (
            "## Proof",
            "## 证明",
            "## Proof（证明）",
            "## 证明 (Proof)",
            "## Proof.",
            "## Proof of Theorem 2",
            "## 证明细节",
        )
        self.assertTrue(all(PROOF_LEAK_RE.search(line) for line in leaking))
        self.assertIsNone(PROOF_LEAK_RE.search("## Proofreading"))

    def test_exercise_bilingual_and_numbered_variants(self) -> None:
        leaking = (
            "## Exercises",
            "## 课后习题",
            "## 习题 (Exercises)",
            "## Exercises (习题)",
            "## Exercises 3.2",
            "## Exercises: 3.2",
        )
        self.assertTrue(all(EXERCISE_LEAK_RE.search(line) for line in leaking))
        self.assertIsNone(EXERCISE_LEAK_RE.search("## Exercised"))


class BilingualFirstOccurrenceTests(unittest.TestCase):
    def test_configured_term_requires_pair_at_first_occurrence(self) -> None:
        term = BilingualTerm("收敛", "convergence", block_id="K-009")
        good = "## K-009 定义\n收敛（convergence）是重要概念。\n"
        bad = "## K-009 定义：收敛\n收敛是重要概念。\n"
        self.assertEqual(validate_bilingual_terms(good, [term]), [])
        errors = validate_bilingual_terms(bad, [term])
        self.assertTrue(any("术语双语缺失" in error and "第 1 行" in error for error in errors))

    def test_reverse_orientation_and_eight_character_tolerance(self) -> None:
        term = BilingualTerm("收敛", "convergence", block_id="K-009")
        reverse = "## K-009 定义\nconvergence（收敛）是重要概念。\n"
        near = "## K-009 定义\n收敛，见（convergence）是重要概念。\n"
        self.assertEqual(validate_bilingual_terms(reverse, [term]), [])
        self.assertEqual(validate_bilingual_terms(near, [term]), [])

    def test_only_global_first_occurrence_is_required(self) -> None:
        terms = [BilingualTerm("收敛", "convergence", block_id="K-009")]
        knowledge = (
            "## K-009 定义\n收敛（convergence）是重要概念。\n"
            "## K-019 定理\n收敛再次出现但不重复英文。\n"
        )
        self.assertEqual(validate_bilingual_terms(knowledge, terms), [])

    def test_can_limit_search_to_included_blocks(self) -> None:
        term = BilingualTerm("收敛", "convergence")
        knowledge = (
            "## K-023 证明\n收敛（convergence）。\n"
            "## K-009 定义\n收敛是正文。\n"
        )
        errors = validate_bilingual_terms(knowledge, [term], {"K-009"})
        self.assertTrue(any("术语双语缺失" in error for error in errors))

    def test_long_block_identifier_is_not_merged_with_prior_block(self) -> None:
        term = BilingualTerm("收敛", "convergence", block_id="K-1010")
        knowledge = (
            "## K-997 定义\n前一块没有该术语。\n"
            "## K-1010 定义\n收敛（convergence）是重要概念。\n"
        )
        self.assertEqual(validate_bilingual_terms(knowledge, [term]), [])


class ScoreFragmentTests(unittest.TestCase):
    def test_bilingual_any_accepts_bracket_width_and_spacing(self) -> None:
        fragment = "收敛（convergence）"
        self.assertTrue(_fragment_hit("收敛 (convergence)", fragment, True))
        self.assertTrue(_fragment_hit("收敛（convergence）", "收敛(convergence)", True))
        self.assertFalse(_fragment_hit("收敛 (convergence)", fragment, False))


if __name__ == "__main__":
    unittest.main()
