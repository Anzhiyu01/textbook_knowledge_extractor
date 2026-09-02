#!/usr/bin/env python3
"""Aggregate valid anonymous paired results into descriptive net effects."""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


DIMENSIONS = ("coverage", "fidelity_math", "exclusion", "structure", "traceability")


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _report(result: dict[str, Any]) -> dict[str, Any]:
    value = result.get("score_report", result)
    return value if isinstance(value, dict) else {}


def aggregate_pairs(experiment_dir: Path) -> dict[str, Any]:
    manifest = _object(experiment_dir / "manifest.json")
    control = _object(experiment_dir / "control" / "package_mapping.json")
    config = _object(experiment_dir / "experiment.json")
    pairs: list[dict[str, Any]] = []
    total_deltas: list[float] = []
    dimension_deltas: dict[str, list[float]] = {name: [] for name in DIMENSIONS}

    for trial in manifest.get("trials", []):
        number = trial.get("trial")
        mapping = control.get("trials", {}).get(str(number), {})
        arm_to_package = {arm: package for package, arm in mapping.items()}
        reasons: list[str] = []
        if set(arm_to_package) != {"with_skill", "without_skill"}:
            reasons.append("control mapping is incomplete")
        results: dict[str, dict[str, Any]] = {}
        for arm in ("with_skill", "without_skill"):
            package_id = arm_to_package.get(arm)
            path = experiment_dir / "results" / f"trial_{number}_{package_id}.json"
            try:
                result = _object(path)
                results[arm] = result
            except Exception as exc:
                reasons.append(f"cannot read {arm} result: {exc}")
                continue
            if result.get("package_id") != package_id:
                reasons.append(f"{arm} result package_id mismatch")
            if result.get("contaminated") is True:
                reasons.append(f"{arm} result is marked contaminated")
            if result.get("model") != config.get("model"):
                reasons.append(f"{arm} model mismatch")
            if result.get("reasoning_effort") != config.get("reasoning_effort"):
                reasons.append(f"{arm} reasoning setting mismatch")
            if result.get("public_hashes") != manifest.get("hashes", {}).get("public"):
                reasons.append(f"{arm} public input hashes mismatch")
            if not _report(result).get("headline_eligible"):
                reasons.append(f"{arm} score is not headline-eligible")

        pair: dict[str, Any] = {"trial": number, "valid": not reasons, "invalid_reasons": reasons}
        if not reasons:
            with_report = _report(results["with_skill"])
            without_report = _report(results["without_skill"])
            total_delta = round(with_report["total_points"] - without_report["total_points"], 4)
            dimensions = {
                name: round(
                    with_report["dimension_scores_diagnostic"][name]
                    - without_report["dimension_scores_diagnostic"][name],
                    4,
                )
                for name in DIMENSIONS
            }
            pair.update({"total_delta": total_delta, "dimension_deltas": dimensions})
            total_deltas.append(total_delta)
            for name, value in dimensions.items():
                dimension_deltas[name].append(value)
        pairs.append(pair)

    summary: dict[str, Any] = {
        "experiment_id": experiment_dir.name,
        "valid_pair_count": len(total_deltas),
        "invalid_pair_count": len(pairs) - len(total_deltas),
        "pairs": pairs,
        "note": "Descriptive statistics only; no significance claim.",
    }
    if total_deltas:
        summary["mean_net_gain"] = round(statistics.mean(total_deltas), 4)
        summary["worst_net_gain"] = round(min(total_deltas), 4)
        summary["sample_variance"] = round(statistics.variance(total_deltas), 4) if len(total_deltas) > 1 else None
        summary["mean_dimension_deltas"] = {
            name: round(statistics.mean(values), 4) for name, values in dimension_deltas.items()
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-dir", required=True, type=Path)
    args = parser.parse_args()
    report = aggregate_pairs(args.experiment_dir.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["invalid_pair_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
