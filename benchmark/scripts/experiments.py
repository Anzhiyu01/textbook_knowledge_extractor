"""Offline v2.5 experiment configuration and frozen manifest helpers."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
REQUIRED_CONFIG = {"model", "reasoning_effort", "trials"}
IGNORED_TREE_PARTS = {"__pycache__", ".ruff_cache"}


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(config) != REQUIRED_CONFIG:
        errors.append("experiment.json must contain exactly model, reasoning_effort, trials")
    if not isinstance(config.get("model"), str) or not config.get("model", "").strip():
        errors.append("model is required")
    effort = config.get("reasoning_effort")
    if not isinstance(effort, str) or not effort.strip():
        errors.append("reasoning_effort must be a nonempty string")
    trials = config.get("trials")
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        errors.append("trials must be a positive integer")
    return errors


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    files = [
        item for item in path.rglob("*")
        if item.is_file()
        and not any(part in IGNORED_TREE_PARTS for part in item.relative_to(path).parts)
        and item.suffix.lower() not in {".pyc", ".pyo"}
    ]
    for item in sorted(files, key=lambda value: value.relative_to(path).as_posix()):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        data = item.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def init_experiment(root: Path, experiment_id: str) -> Path:
    if not ID_RE.fullmatch(experiment_id):
        raise ValueError("experiment_id must be ASCII snake_case")
    path = root / experiment_id
    path.mkdir(parents=True, exist_ok=False)
    config = {"model": "exact-model-name", "reasoning_effort": "unknown", "trials": 3}
    (path / "experiment.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    return path


def freeze_manifest(
    experiment_dir: Path,
    *,
    backend_case: Path,
    public_case: Path,
    source_file: Path,
    prompt_file: Path,
    public_schema: Path,
    scoring_file: Path,
    gold_file: Path,
    skill_dir: Path,
) -> dict[str, Any]:
    config = json.loads(
        (experiment_dir / "experiment.json").read_text(encoding="utf-8-sig")
    )
    errors = validate_config(config)
    if errors:
        raise ValueError("; ".join(errors))
    manifest = {
        "manifest_version": "2.5",
        "experiment_id": experiment_dir.name,
        "config": config,
        "hashes": {
            "public": {
                "prompt": digest_file(prompt_file),
                "case": digest_file(public_case),
                "source": digest_file(source_file),
                "schema": digest_file(public_schema),
                "scoring": digest_file(scoring_file),
            },
            "backend": {
                "case": digest_file(backend_case),
                "gold": digest_file(gold_file),
                "skill": digest_tree(skill_dir),
            },
        },
        "trials": [
            {"trial": number, "package_ids": ["package_a", "package_b"]}
            for number in range(1, config["trials"] + 1)
        ],
    }
    (experiment_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def verify_manifest(experiment_dir: Path) -> bool:
    manifest = json.loads(
        (experiment_dir / "manifest.json").read_text(encoding="utf-8-sig")
    )
    config = json.loads(
        (experiment_dir / "experiment.json").read_text(encoding="utf-8-sig")
    )
    return manifest.get("manifest_version") == "2.5" and manifest.get("config") == config


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("root", type=Path)
    init_parser.add_argument("experiment_id")
    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("experiment_dir", type=Path)
    freeze_parser.add_argument("--backend-case", required=True, type=Path)
    freeze_parser.add_argument("--public-case", required=True, type=Path)
    freeze_parser.add_argument("--source", required=True, type=Path)
    freeze_parser.add_argument("--prompt", required=True, type=Path)
    freeze_parser.add_argument("--public-schema", required=True, type=Path)
    freeze_parser.add_argument("--scoring", required=True, type=Path)
    freeze_parser.add_argument("--gold", required=True, type=Path)
    freeze_parser.add_argument("--skill-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "init":
        print(init_experiment(args.root, args.experiment_id))
        return 0
    manifest = freeze_manifest(
        args.experiment_dir.resolve(),
        backend_case=args.backend_case.resolve(),
        public_case=args.public_case.resolve(),
        source_file=args.source.resolve(),
        prompt_file=args.prompt.resolve(),
        public_schema=args.public_schema.resolve(),
        scoring_file=args.scoring.resolve(),
        gold_file=args.gold.resolve(),
        skill_dir=args.skill_dir.resolve(),
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
