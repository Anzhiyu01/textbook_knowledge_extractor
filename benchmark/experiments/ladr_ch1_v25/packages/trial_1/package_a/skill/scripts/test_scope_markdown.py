#!/usr/bin/env python3
"""Regression tests for scope_markdown.py."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scope_markdown import (
    index_headings,
    precheck_source,
    probe_lines,
    read_source,
    resolve_range,
    source_position,
    discover_candidates,
)


SOURCE = """# Book

~~~text
## Fake chapter
~~~

## Chapter One

Body.

### Exercise

Question.

## Chapter Two

End.

Appendix
========
"""


class ScopeMarkdownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "book.md"
        self.path.write_text(SOURCE, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_ignores_fenced_heading_and_resolves_next_peer(self) -> None:
        _, lines = read_source(self.path)
        headings = index_headings(lines, 16)
        self.assertEqual(
            [h.text for h in headings],
            ["Book", "Chapter One", "Exercise", "Chapter Two", "Appendix"],
        )
        start, end, end_line = resolve_range(
            headings, len(lines), "Chapter One", 1, None, 1
        )
        self.assertEqual(start.line, 7)
        self.assertEqual(end.text, "Chapter Two")
        self.assertEqual(end_line, 14)

    def test_explicit_end_heading(self) -> None:
        _, lines = read_source(self.path)
        headings = index_headings(lines, 0)
        start, end, end_line = resolve_range(
            headings, len(lines), "Chapter One", 1, "Chapter Two", 1
        )
        self.assertEqual((start.line, end.line, end_line), (7, 15, 14))

    def test_probe_returns_only_matching_prefixes(self) -> None:
        _, lines = read_source(self.path)
        matches = probe_lines(lines, re.compile(r"chapter", re.IGNORECASE), 12, 10)
        self.assertEqual(
            matches,
            [
                {"line": 7, "prefix": "## Chapter O"},
                {"line": 15, "prefix": "## Chapter T"},
            ],
        )

    def test_explicit_line_range_matches_heading_slice(self) -> None:
        heading_output = Path(self.temp.name) / "heading.md"
        heading_manifest = Path(self.temp.name) / "heading.json"
        line_output = Path(self.temp.name) / "line.md"
        line_manifest = Path(self.temp.name) / "line.json"

        self._run_extract(
            "--start-heading",
            "Chapter One",
            "--end-before-heading",
            "Chapter Two",
            "--output",
            str(heading_output),
            "--manifest",
            str(heading_manifest),
        )
        self._run_extract(
            "--start-line",
            "7",
            "--end-line",
            "14",
            "--output",
            str(line_output),
            "--manifest",
            str(line_manifest),
        )

        self.assertEqual(heading_output.read_bytes(), line_output.read_bytes())
        manifest = json.loads(line_manifest.read_text(encoding="utf-8"))
        self.assertEqual(manifest["selection_method"], "explicit-line-range")
        self.assertFalse(manifest["start_is_heading"])
        self.assertFalse(manifest["end_is_heading"])
        self.assertIsNone(manifest["start_heading"])
        self.assertIsNone(manifest["end_before_heading"])
        self.assertEqual((manifest["start_line"], manifest["end_line"]), (7, 14))

        legacy_manifest = json.loads(heading_manifest.read_text(encoding="utf-8"))
        self.assertTrue(legacy_manifest["start_is_heading"])
        self.assertTrue(legacy_manifest["end_is_heading"])

    def test_sample_lines_5_to_70_match_heading_slice(self) -> None:
        sample = Path(__file__).resolve().parents[3] / "benchmark" / "dev" / "input" / "sample_textbook.md"
        heading_output = Path(self.temp.name) / "sample-heading.md"
        line_output = Path(self.temp.name) / "sample-line.md"
        self._run_extract(
            "--start-heading",
            "第一章 数列",
            "--end-before-heading",
            "第二章 连续函数",
            "--output",
            str(heading_output),
            source=sample,
        )
        self._run_extract(
            "--start-line",
            "5",
            "--end-line",
            "70",
            "--output",
            str(line_output),
            source=sample,
        )
        self.assertEqual(heading_output.read_bytes(), line_output.read_bytes())

    def test_heading_start_can_mix_with_explicit_end_line(self) -> None:
        output = Path(self.temp.name) / "mixed.md"
        manifest_path = Path(self.temp.name) / "mixed.json"
        self._run_extract(
            "--start-heading",
            "Chapter One",
            "--end-line",
            "14",
            "--output",
            str(output),
            "--manifest",
            str(manifest_path),
        )
        self.assertEqual(
            output.read_text(encoding="utf-8"),
            "## Chapter One\n\nBody.\n\n### Exercise\n\nQuestion.\n\n",
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["selection_method"], "explicit-line-range")
        self.assertTrue(manifest["start_is_heading"])
        self.assertFalse(manifest["end_is_heading"])
        self.assertEqual(manifest["start_heading"]["text"], "Chapter One")
        self.assertIsNone(manifest["end_before_heading"])

    def test_explicit_line_range_rejects_out_of_bounds(self) -> None:
        output = Path(self.temp.name) / "out-of-bounds.md"
        result = self._run_extract(
            "--start-line",
            "0",
            "--end-line",
            "14",
            "--output",
            str(output),
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside source", result.stderr)
        self.assertFalse(output.exists())

    def test_explicit_line_range_rejects_reversed_bounds(self) -> None:
        output = Path(self.temp.name) / "reversed.md"
        result = self._run_extract(
            "--start-line",
            "14",
            "--end-line",
            "7",
            "--output",
            str(output),
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("reversed", result.stderr)
        self.assertFalse(output.exists())

    def test_explicit_line_range_rejects_start_inside_fence(self) -> None:
        fenced = Path(self.temp.name) / "fenced.md"
        fenced.write_text("# Book\n\n```text\ninside\n```\n", encoding="utf-8")
        output = Path(self.temp.name) / "inside.md"
        result = self._run_extract(
            "--start-line",
            "4",
            "--end-line",
            "4",
            "--output",
            str(output),
            check=False,
            source=fenced,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("fenced code block", result.stderr)
        self.assertFalse(output.exists())

    def test_loose_atx_is_off_by_default_and_tagged_when_enabled(self) -> None:
        loose = Path(self.temp.name) / "loose.md"
        loose.write_text(
            "#第1章 数列\n\n正文。\n\n## 第一节\n\n内容。\n",
            encoding="utf-8",
        )
        _, lines = read_source(loose)
        strict = index_headings(lines, 0)
        self.assertEqual(
            [heading.text for heading in strict],
            ["第一节"],
            "strict mode must not promote '#第1章' to a heading",
        )
        loose_headings = index_headings(lines, 0, loose_atx=True)
        self.assertEqual(
            [heading.text for heading in loose_headings],
            ["第1章 数列", "第一节"],
        )
        first = loose_headings[0]
        self.assertEqual(first.kind, "atx")
        self.assertEqual(first.matched_by, "loose")
        self.assertFalse(first.suspicious)
        self.assertEqual(loose_headings[1].matched_by, "strict")

    def test_index_cli_loose_atx_flag_and_kind_tags(self) -> None:
        loose = Path(self.temp.name) / "cli-loose.md"
        loose.write_text("#第1章 数列\n\n正文。\n", encoding="utf-8")
        result = self._run_tool(
            "index",
            "--loose-atx",
            source=loose,
        )
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["heading_count"], 1)
        heading = payload["headings"][0]
        self.assertEqual(heading["text"], "第1章 数列")
        self.assertEqual(heading["kind"], "atx")
        self.assertEqual(heading["matched_by"], "loose")

        strict = self._run_tool("index", source=loose)
        payload = json.loads(strict.stdout)
        self.assertEqual(payload["heading_count"], 0)

    def test_setext_headings_are_tagged_and_suspicious_detected(self) -> None:
        suspicious = Path(self.temp.name) / "suspicious.md"
        suspicious.write_text(
            "正文一行。\n---\n\n附录\n=======\n\n更多句子。第二句也在这里。\n---\n",
            encoding="utf-8",
        )
        _, lines = read_source(suspicious)
        headings = index_headings(lines, 0)
        self.assertEqual(
            [
                (heading.text, heading.kind, heading.matched_by, heading.suspicious)
                for heading in headings
            ],
            [
                ("正文一行。", "setext", "strict", True),
                ("附录", "setext", "strict", False),
                ("更多句子。第二句也在这里。", "setext", "strict", True),
            ],
        )

    def test_extract_warns_when_end_hits_suspicious_setext(self) -> None:
        suspicious = Path(self.temp.name) / "warn.md"
        suspicious.write_text(
            "# Book\n\n## Chapter One\n\nBody.\n\n正文一行。\n---\n\nEnd.\n",
            encoding="utf-8",
        )
        output = Path(self.temp.name) / "warn-slice.md"
        result = self._run_extract(
            "--start-heading",
            "Chapter One",
            "--output",
            str(output),
            source=suspicious,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("WARNING", result.stderr)
        self.assertIn("suspicious Setext heading", result.stderr)
        # The default rule still cut at the suspicious heading's line.
        self.assertEqual(
            output.read_text(encoding="utf-8"),
            "## Chapter One\n\nBody.\n\n",
        )

    def test_start_heading_tolerates_marker_and_whitespace(self) -> None:
        first = Path(self.temp.name) / "tolerant-a.md"
        second = Path(self.temp.name) / "tolerant-b.md"
        manifest = Path(self.temp.name) / "tolerant.json"
        self._run_extract(
            "--start-heading",
            "## Chapter One",
            "--end-before-heading",
            "Chapter Two",
            "--output",
            str(first),
            "--manifest",
            str(manifest),
        )
        self._run_extract(
            "--start-heading",
            "Chapter One ",
            "--end-before-heading",
            "Chapter Two",
            "--output",
            str(second),
        )
        self.assertEqual(first.read_bytes(), second.read_bytes())
        recorded = json.loads(manifest.read_text(encoding="utf-8"))
        # The index text stays the canonical identity.
        self.assertEqual(recorded["start_heading"]["text"], "Chapter One")

    def test_start_heading_still_rejects_unknown_text(self) -> None:
        output = Path(self.temp.name) / "unknown.md"
        result = self._run_extract(
            "--start-heading",
            "## 不存在的一章",
            "--output",
            str(output),
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("heading not found", result.stderr)
        self.assertFalse(output.exists())

    def test_precheck_reports_integrity_warnings(self) -> None:
        damaged = Path(self.temp.name) / "damaged.md"
        damaged.write_text(
            "# Book\n\n"
            "### 1.1 定义\n\n内容。\n\n"
            "### 1.3 定理\n\n内容。\n\n"
            "第三章 裸文本\n\n"
            "损坏字符 \ufffd 在这里。\n\n"
            "```python\n未闭合\n",
            encoding="utf-8",
        )
        _, lines = read_source(damaged)
        warnings = precheck_source(lines)
        types = {warning["type"] for warning in warnings}
        self.assertIn("heading_level_jump", types)
        self.assertIn("numbering_gap", types)
        self.assertIn("bare_chapter_marker", types)
        self.assertIn("replacement_char", types)
        self.assertIn("unclosed_fence", types)
        gap = next(w for w in warnings if w["type"] == "numbering_gap")
        self.assertIn("1.1", gap["message"])
        self.assertIn("1.3", gap["message"])

    def test_precheck_reports_conversion_artifacts_and_missing_label_reference(self) -> None:
        damaged = Path(self.temp.name) / "conversion-damaged.md"
        damaged.write_text(
            "# Book\n\n"
            "## 1.1 Definition\n\nA defnition with a ? placeholder.\n\n"
            "## 1.2 Example\n\nSee 1.13 for the operation.\n\n"
            "```text\nignore ? and defnition inside code\n```\n",
            encoding="utf-8",
        )
        _, lines = read_source(damaged)
        warnings = precheck_source(lines)
        by_type = {warning["type"]: warning for warning in warnings}
        self.assertIn("placeholder_question_mark", by_type)
        self.assertIn("ligature_damage", by_type)
        self.assertIn("numbering_label_loss", by_type)
        self.assertEqual(by_type["placeholder_question_mark"]["count"], 1)
        self.assertIn("1.13", by_type["numbering_label_loss"]["message"])

    def test_precheck_cli_and_clean_source(self) -> None:
        damaged = Path(self.temp.name) / "precheck-cli.md"
        damaged.write_text(
            "# Book\n\n## 1.1 First\n\nText.\n\n## 1.2 Second\n\nText.\n",
            encoding="utf-8",
        )
        result = self._run_tool("precheck", source=damaged)
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["warning_count"], 0)
        self.assertEqual(payload["warnings"], [])
        self.assertIn("never modified", payload["note"])

        _, lines = read_source(self.path)
        self.assertEqual(precheck_source(lines), [])

    def test_source_position_uses_container_marker_line(self) -> None:
        lines = ["> [!info] Note", "> result", "", "```txt", "x", "```"]
        callout = source_position(lines, 1, 2)
        self.assertEqual(callout["marker_start_line"], 1)
        self.assertEqual(callout["content_start_line"], 2)
        self.assertEqual(callout["container_type"], "callout")
        fenced = source_position(lines, 4, 6)
        self.assertEqual((fenced["content_start_line"], fenced["content_end_line"]), (5, 5))
        table = source_position(["<tr>", "<td>x</td>", "</table>"], 1, 3)
        self.assertEqual(table["container_type"], "html_table")

    def test_precheck_both_reports_slice_and_ignores_existing_cross_chapter_reference(self) -> None:
        source = Path(self.temp.name) / "both.md"
        source.write_text("# Book\n\n## 1.1 A\nSee 4.8.\n\n## 4.8 B\nText.\n", encoding="utf-8")
        result = self._run_tool("precheck", "--mode", "both", "--start-line", "3", "--end-line", "4", source=source)
        payload = json.loads(result.stdout)
        self.assertIn("whole", payload["reports"])
        self.assertIn("slice", payload["reports"])
        self.assertNotIn("numbering_label_loss", {w["type"] for w in payload["reports"]["slice"]})

    def test_slice_precheck_limits_ligature_warning_to_slice(self) -> None:
        source = Path(self.temp.name) / "ligature-scope.md"
        source.write_text("# Book\n\ndefnition outside\n\nfinite inside\n", encoding="utf-8")
        result = self._run_tool("precheck", "--mode", "slice", "--start-line", "5", "--end-line", "5", source=source)
        payload = json.loads(result.stdout)
        warnings = {w["type"]: w for w in payload["warnings"]}
        self.assertNotIn("ligature_damage", warnings)

    def test_candidate_discovery_covers_numbered_and_special_units(self) -> None:
        lines = [
            "# Chapter", "", "1.10 A statement", "", "Proof", "", 
            "> [!NOTE] callout", "", "$$", "x=1", "$$", "", "Exercises 1.1",
        ]
        rows = discover_candidates(lines)
        signals = {row["signal"] for row in rows}
        self.assertIn("bare_number_or_exclusion_label", signals)
        self.assertIn("callout", signals)
        self.assertIn("formula_container", signals)

    def _run_tool(
        self,
        command: str,
        *options: str,
        check: bool = True,
        source: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        argv = [
            sys.executable,
            str(Path(__file__).with_name("scope_markdown.py")),
            command,
            "--source",
            str(source or self.path),
            *options,
        ]
        return subprocess.run(
            argv,
            check=check,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def _run_extract(
        self,
        *options: str,
        check: bool = True,
        source: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(Path(__file__).with_name("scope_markdown.py")),
            "extract",
            "--source",
            str(source or self.path),
            *options,
        ]
        return subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
