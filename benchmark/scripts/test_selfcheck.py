#!/usr/bin/env python3
"""Regression tests for the deterministic pre-acceptance checklist."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from selfcheck import run_checks


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


class SelfcheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "book.md"
        self.source_text = "# Book\n\n## Chapter\n\n### Definition\n\nA statement.\n\n## Next\n\nEnd.\n"
        self.source.write_text(self.source_text, encoding="utf-8")
        lines = self.source_text.splitlines()
        selected = "\n".join(lines[2:6]) + "\n"
        self.case_path = self.root / "case.json"
        self.case_path.write_text(
            json.dumps(
                {
                    "case_id": "selfcheck-test",
                    "source_file": "book.md",
                    "source_sha256": _sha(self.source.read_bytes()),
                    "target": {
                        "start_heading": "## Chapter",
                        "end_before_heading": "## Next",
                        "expected_start_line": 3,
                        "expected_end_line": 6,
                    },
                    "block_id_format": "K-{source_start_line:03d}",
                }
            ),
            encoding="utf-8",
        )
        self.submission = self.root / "submission"
        self.submission.mkdir()
        self._write_submission(selected)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_submission(self, selected: str) -> None:
        self.submission.joinpath("knowledge.md").write_text(
            "## K-005 Definition\n\nA statement.\n", encoding="utf-8"
        )
        self.submission.joinpath("audit.json").write_text(
            json.dumps(
                {
                    "case_id": "selfcheck-test",
                    "source_sha256": _sha(self.source.read_bytes()),
                    "boundaries": {
                        "start_heading": "## Chapter",
                        "end_before_heading": "## Next",
                        "start_line": 3,
                        "end_line": 6,
                    },
                    "scope_preprocessing": {
                        "slice_sha256": _sha(selected.encode("utf-8")),
                        "slice_line_count": 4,
                    },
                    "candidates": [
                        {
                            "block_id": "K-005",
                            "kind": "definition",
                            "source_start_line": 5,
                            "source_end_line": 6,
                            "decision": "include",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    def test_passes_valid_hashes_spans_and_id_order(self) -> None:
        report, code = run_checks(self.case_path, self.submission)
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failure_count"], 0)

    def test_reports_audit_range_and_heading_leak(self) -> None:
        audit_path = self.submission / "audit.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        audit["boundaries"]["end_line"] = 5
        audit_path.write_text(json.dumps(audit), encoding="utf-8")
        self.submission.joinpath("knowledge.md").write_text(
            "## K-005 Definition\n\nA statement.\n\n## Proof\n\nleak\n", encoding="utf-8"
        )
        report, code = run_checks(self.case_path, self.submission)
        self.assertEqual(code, 1)
        failures = "\n".join(report["failures"])
        self.assertIn("boundary_end_line", failures)
        self.assertIn("proof_leaks", failures)

    def test_line_selection_does_not_require_a_heading_at_start(self) -> None:
        case = json.loads(self.case_path.read_text(encoding="utf-8"))
        case["target"]["expected_start_line"] = 4
        case["target"]["expected_end_line"] = 6
        case["target"]["start_heading"] = "## Chapter"
        self.case_path.write_text(json.dumps(case), encoding="utf-8")
        audit = json.loads((self.submission / "audit.json").read_text(encoding="utf-8"))
        selected = "\n".join(self.source_text.splitlines()[3:6]) + "\n"
        audit["boundaries"]["start_line"] = 4
        audit["boundaries"]["end_line"] = 6
        audit["scope_preprocessing"]["slice_sha256"] = _sha(selected.encode("utf-8"))
        audit["scope_preprocessing"]["slice_line_count"] = 3
        audit["candidates"][0]["source_start_line"] = 5
        audit["candidates"][0]["source_end_line"] = 6
        (self.submission / "audit.json").write_text(json.dumps(audit), encoding="utf-8")
        report, code = run_checks(self.case_path, self.submission)
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "PASS")

    def test_bilingual_check_ignores_excluded_block_evidence(self) -> None:
        """A proof block must not satisfy a term required in an included block."""
        audit_path = self.submission / "audit.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        audit["candidates"].append(
            {
                "block_id": "K-004",
                "kind": "proof",
                "source_start_line": 4,
                "source_end_line": 4,
                "decision": "exclude",
                "exclusion_reason": "proof",
            }
        )
        audit["bilingual_terms"] = [
            {"term": "陈述", "english": "statement", "block_id": "K-005"}
        ]
        audit_path.write_text(json.dumps(audit), encoding="utf-8")
        self.submission.joinpath("knowledge.md").write_text(
            "## K-004 Supporting note\n陈述（statement）\n\n"
            "## K-005 Definition\n\n陈述是正文。\n",
            encoding="utf-8",
        )
        report, code = run_checks(
            self.case_path, self.submission, require_bilingual=True
        )
        self.assertEqual(code, 1)
        self.assertIn("bilingual_first_occurrence", "\n".join(report["failures"]))

    def test_accepts_four_digit_block_ids(self) -> None:
        case = json.loads(self.case_path.read_text(encoding="utf-8"))
        case["block_id_format"] = "K-{candidate_ordinal:03d}"
        self.case_path.write_text(json.dumps(case), encoding="utf-8")
        audit_path = self.submission / "audit.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        audit["candidates"][0]["block_id"] = "K-1005"
        audit_path.write_text(json.dumps(audit), encoding="utf-8")
        self.submission.joinpath("knowledge.md").write_text(
            "## K-1005 Definition\n\nA statement.\n", encoding="utf-8"
        )
        report, code = run_checks(self.case_path, self.submission)
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
