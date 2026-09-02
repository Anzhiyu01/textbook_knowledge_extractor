from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from aggregate_pairs import aggregate_pairs
from experiments import freeze_manifest
from import_results import import_result
from package_builder import build_packages
from score_outcome import score_submission
from validate_public_submission import validate_public_submission


class PublicContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.md"
        self.source.write_text("# Chapter\n\nDefinition A.\n\nExample B.\n", encoding="utf-8")
        self.case = self.root / "case.json"
        self.case.write_text(
            json.dumps({
                "public_case_version": "2.5",
                "case_id": "case_x",
                "source_file": "source.md",
                "submission_files": ["knowledge.md", "audit.json"],
            }),
            encoding="utf-8",
        )
        self.submission = self.root / "submission"
        self.submission.mkdir()
        self.submission.joinpath("knowledge.md").write_text(
            "# Chapter\n\n## B-001 Definition\n\nDefinition A.\n\n"
            "## B-002 Example\n\nExample B.\n",
            encoding="utf-8",
        )
        self.submission.joinpath("audit.json").write_text(
            json.dumps({
                "public_audit_version": "2.5",
                "case_id": "case_x",
                "entries": [
                    {
                        "output_id": "B-001",
                        "kind": "definition",
                        "source": {"relative_start_line": 3, "relative_end_line": 3},
                    },
                    {
                        "output_id": "B-002",
                        "kind": "example",
                        "source": {"text_anchor": "Example B."},
                    },
                ],
            }),
            encoding="utf-8",
        )
        self.gold = self.root / "gold.json"
        self.gold.write_text(
            json.dumps({
                "gold_version": "2.5",
                "case_id": "case_x",
                "status": "reviewed",
                "items": [
                    {"block_id": "K-003", "decision": "include", "kind": "definition", "weight": 1},
                    {"block_id": "K-005", "decision": "include", "kind": "example", "weight": 1},
                ],
            }),
            encoding="utf-8",
        )
        self.review = self.root / "review.json"
        self.review.write_text(
            json.dumps({
                "review_version": "2.5",
                "status": "reviewed",
                "items": [
                    {"gold_id": "K-003", "coverage": 1, "fidelity_math": 1},
                    {"gold_id": "K-005", "coverage": 1, "fidelity_math": 1},
                ],
                "exclusion_fraction": 1,
                "structure_fraction": 1,
                "unsupported_extra_count": 0,
                "mathematical_error_count": 0,
            }),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_public_validator_accepts_result_only_audit(self) -> None:
        report, code = validate_public_submission(self.case, self.submission)
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["audit_trace_fraction"], 1.0)

    def test_full_reviewed_artifact_scores_100_without_process_fields(self) -> None:
        report = score_submission(self.case, self.submission, self.gold, self.review)
        same_artifact_other_arm = score_submission(
            self.case, self.submission, self.gold, self.review
        )
        self.assertTrue(report["headline_eligible"])
        self.assertEqual(report["total_points"], 100.0)
        self.assertEqual(report, same_artifact_other_arm)
        self.assertNotIn("arm", report)
        self.assertNotIn("workflow", report["dimension_scores_diagnostic"])

    def test_missing_audit_only_removes_traceability_points(self) -> None:
        self.submission.joinpath("audit.json").unlink()
        report = score_submission(self.case, self.submission, self.gold, self.review)
        self.assertTrue(report["headline_eligible"])
        self.assertEqual(report["dimension_scores_diagnostic"]["traceability"], 0.0)
        self.assertEqual(report["total_points"], 95.0)

    def test_partial_and_omitted_items_are_reported(self) -> None:
        review = json.loads(self.review.read_text(encoding="utf-8"))
        review["items"][0]["coverage"] = 0.5
        review["items"][1]["coverage"] = 0
        self.review.write_text(json.dumps(review), encoding="utf-8")
        report = score_submission(self.case, self.submission, self.gold, self.review)
        self.assertEqual(report["partial_hit_count"], 1)
        self.assertEqual(report["omitted_count"], 1)
        self.assertEqual(report["dimension_scores_diagnostic"]["coverage"], 15.0)

    def test_unreviewed_gold_cannot_emit_headline_total(self) -> None:
        gold = json.loads(self.gold.read_text(encoding="utf-8"))
        gold["status"] = "human_review_required"
        self.gold.write_text(json.dumps(gold), encoding="utf-8")
        report = score_submission(self.case, self.submission, self.gold, self.review)
        self.assertFalse(report["headline_eligible"])
        self.assertNotIn("total_points", report)

    def test_explicit_proof_leak_caps_exclusion_score(self) -> None:
        path = self.submission / "knowledge.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n## Proof\n\nLeaked.\n", encoding="utf-8")
        report = score_submission(self.case, self.submission, self.gold, self.review)
        self.assertEqual(report["proof_leak_count"], 1)
        self.assertEqual(report["dimension_scores_diagnostic"]["exclusion"], 12.0)


class PackageIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.experiment = self.root / "experiment_x"
        self.experiment.mkdir()
        self.experiment.joinpath("experiment.json").write_text(
            json.dumps({"model": "model-x", "reasoning_effort": "high", "trials": 2}),
            encoding="utf-8",
        )
        self.backend_case = self.root / "backend_case.json"
        self.backend_case.write_text("{}\n", encoding="utf-8")
        self.public_case = self.root / "public_case.json"
        self.public_case.write_text(
            json.dumps({"case_id": "x", "source_file": "source.md"}) + "\n",
            encoding="utf-8",
        )
        self.source = self.root / "source.md"
        self.source.write_text("# Source\n", encoding="utf-8")
        self.prompt = self.root / "prompt.md"
        self.prompt.write_text("Extract the requested knowledge list.\n", encoding="utf-8")
        self.schema = self.root / "public_audit.schema.json"
        self.schema.write_text("{}\n", encoding="utf-8")
        self.scoring = self.root / "scoring.md"
        self.scoring.write_text("Outcome score.\n", encoding="utf-8")
        self.gold = self.root / "gold.json"
        self.gold.write_text('{"status":"human_review_required"}\n', encoding="utf-8")
        self.capability = self.root / "capability_source"
        self.capability.mkdir()
        self.capability.joinpath("SKILL.md").write_text("capability data\n", encoding="utf-8")
        freeze_manifest(
            self.experiment,
            backend_case=self.backend_case,
            public_case=self.public_case,
            source_file=self.source,
            prompt_file=self.prompt,
            public_schema=self.schema,
            scoring_file=self.scoring,
            gold_file=self.gold,
            skill_dir=self.capability,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _build(self) -> list[Path]:
        return build_packages(
            self.experiment,
            public_case=self.public_case,
            source=self.source,
            skill_dir=self.capability,
            prompt=self.prompt,
            public_schema=self.schema,
            scoring=self.scoring,
        )

    def test_packages_are_anonymous_and_shared_files_match(self) -> None:
        outputs = self._build()
        self.assertEqual(len(outputs), 4)
        self.assertTrue((self.experiment / "packages/trial_1/package_a/skill").is_dir())
        self.assertFalse((self.experiment / "packages/trial_1/package_b/skill").exists())
        self.assertFalse((self.experiment / "packages/trial_2/package_a/skill").exists())
        self.assertTrue((self.experiment / "packages/trial_2/package_b/skill").is_dir())
        for trial in (1, 2):
            left = self.experiment / f"packages/trial_{trial}/package_a"
            right = self.experiment / f"packages/trial_{trial}/package_b"
            for name in ("prompt.md", "case.json", "source.md", "public_audit.schema.json"):
                self.assertEqual((left / name).read_bytes(), (right / name).read_bytes())
            self.assertFalse((left / "package_manifest.json").exists())
            self.assertFalse((right / "package_manifest.json").exists())
        self.assertTrue((self.experiment / "control/package_mapping.json").is_file())
        self.assertTrue(all("with_skill" not in str(path) and "without_skill" not in str(path) for path in outputs))

    def test_import_and_aggregate_use_backend_mapping(self) -> None:
        self._build()
        full = {
            "headline_eligible": True,
            "total_points": 90.0,
            "dimension_scores_diagnostic": {
                "coverage": 35.0, "fidelity_math": 27.0, "exclusion": 14.0,
                "structure": 9.0, "traceability": 5.0,
            },
        }
        lower = {
            "headline_eligible": True,
            "total_points": 80.0,
            "dimension_scores_diagnostic": {
                "coverage": 30.0, "fidelity_math": 24.0, "exclusion": 13.0,
                "structure": 8.0, "traceability": 5.0,
            },
        }
        import_result(self.experiment, 1, "package_a", {"score_report": full})
        import_result(self.experiment, 1, "package_b", {"score_report": lower})
        import_result(self.experiment, 2, "package_a", {"score_report": lower})
        import_result(self.experiment, 2, "package_b", {"score_report": full})
        report = aggregate_pairs(self.experiment)
        self.assertEqual(report["valid_pair_count"], 2)
        self.assertEqual(report["mean_net_gain"], 10.0)
        self.assertEqual(report["sample_variance"], 0.0)


class RepositoryLeakageTests(unittest.TestCase):
    def test_real_public_files_do_not_disclose_experiment_method(self) -> None:
        benchmark = Path(__file__).resolve().parents[1]
        paths = [
            benchmark / "prompt.md",
            benchmark / "ladr_ch1/input/public_case.json",
            benchmark / "schemas/public_audit.schema.json",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
        forbidden = (
            "skill", "技能", "scope_markdown", "候选索引", "自验收",
            "评分器", "gold", "manifest", "with_skill", "without_skill",
            "控制组", "工具轨迹",
        )
        for token in forbidden:
            self.assertNotIn(token.lower(), combined, token)

    def test_default_catalog_is_explicit_about_unavailable_cases(self) -> None:
        benchmark = Path(__file__).resolve().parents[1]
        catalog = json.loads((benchmark / "default_cases.json").read_text(encoding="utf-8"))
        self.assertEqual(
            catalog["default_case_ids"],
            ["ladr_ch1_v25", "rudin_ch2_v25", "probability_ch1_v25"],
        )
        cases = {case["case_id"]: case for case in catalog["cases"]}
        self.assertEqual(cases["probability_ch1_v25"]["status"], "blocked_missing_source")
        self.assertEqual(cases["ladr_ch1_v25"]["status"], "blocked_until_gold_review")


if __name__ == "__main__":
    unittest.main()
