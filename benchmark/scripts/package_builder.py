"""Build anonymous, model-visible v2.5 packages and a backend-only mapping."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

try:
    from experiments import digest_file, digest_tree
except ImportError:  # pragma: no cover
    from .experiments import digest_file, digest_tree


PACKAGE_IDS = ("package_a", "package_b")


def _mapping_for_trial(number: int) -> dict[str, str]:
    if number % 2:
        return {"package_a": "with_skill", "package_b": "without_skill"}
    return {"package_a": "without_skill", "package_b": "with_skill"}


def _verify_public_hashes(
    manifest: dict[str, Any], *, public_case: Path, source: Path, prompt: Path,
    public_schema: Path, scoring: Path,
) -> None:
    expected = manifest.get("hashes", {}).get("public", {})
    actual = {
        "prompt": digest_file(prompt),
        "case": digest_file(public_case),
        "source": digest_file(source),
        "schema": digest_file(public_schema),
        "scoring": digest_file(scoring),
    }
    if actual != expected:
        raise ValueError("public inputs changed after manifest freeze")


def build_packages(
    experiment_dir: Path,
    *,
    public_case: Path,
    source: Path,
    skill_dir: Path,
    prompt: Path,
    public_schema: Path,
    scoring: Path,
) -> list[Path]:
    manifest = json.loads(
        (experiment_dir / "manifest.json").read_text(encoding="utf-8-sig")
    )
    config = json.loads(
        (experiment_dir / "experiment.json").read_text(encoding="utf-8-sig")
    )
    if manifest.get("manifest_version") != "2.5" or config != manifest.get("config"):
        raise ValueError("experiment configuration drift; freeze a new v2.5 manifest")
    _verify_public_hashes(
        manifest, public_case=public_case, source=source, prompt=prompt,
        public_schema=public_schema, scoring=scoring,
    )
    expected_skill = manifest.get("hashes", {}).get("backend", {}).get("skill")
    if digest_tree(skill_dir) != expected_skill:
        raise ValueError("capability package changed after manifest freeze")

    packages_root = experiment_dir / "packages"
    if packages_root.exists():
        shutil.rmtree(packages_root)
    packages_root.mkdir(parents=True)
    control_dir = experiment_dir / "control"
    control_dir.mkdir(parents=True, exist_ok=True)
    mapping_path = control_dir / "package_mapping.json"
    if mapping_path.exists():
        mapping_path.unlink()

    outputs: list[Path] = []
    control_trials: dict[str, dict[str, str]] = {}
    public_case_data = json.loads(public_case.read_text(encoding="utf-8-sig"))
    source_name = public_case_data.get("source_file")
    if not isinstance(source_name, str) or Path(source_name).name != source_name:
        raise ValueError("public case source_file must be a plain filename")

    for trial in manifest.get("trials", []):
        number = trial["trial"]
        mapping = _mapping_for_trial(number)
        control_trials[str(number)] = mapping
        trial_root = packages_root / f"trial_{number}"
        for package_id in PACKAGE_IDS:
            destination = trial_root / package_id
            destination.mkdir(parents=True)
            shutil.copy2(prompt, destination / "prompt.md")
            shutil.copy2(public_case, destination / "case.json")
            shutil.copy2(source, destination / source_name)
            shutil.copy2(public_schema, destination / "public_audit.schema.json")
            if mapping[package_id] == "with_skill":
                shutil.copytree(
                    skill_dir,
                    destination / "skill",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".ruff_cache"),
                )
            outputs.append(destination)

    control = {
        "control_version": "2.5",
        "experiment_id": experiment_dir.name,
        "public_hashes": manifest["hashes"]["public"],
        "trials": control_trials,
    }
    mapping_path.write_text(
        json.dumps(control, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-dir", required=True, type=Path)
    parser.add_argument("--public-case", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--skill-dir", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--public-schema", required=True, type=Path)
    parser.add_argument("--scoring", required=True, type=Path)
    args = parser.parse_args()
    outputs = build_packages(
        args.experiment_dir.resolve(), public_case=args.public_case.resolve(),
        source=args.source.resolve(), skill_dir=args.skill_dir.resolve(),
        prompt=args.prompt.resolve(), public_schema=args.public_schema.resolve(),
        scoring=args.scoring.resolve(),
    )
    print(json.dumps([str(path) for path in outputs], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
