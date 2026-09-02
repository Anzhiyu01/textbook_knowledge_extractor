"""Import manually produced anonymous-package results without model APIs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def import_result(
    experiment_dir: Path,
    trial: int,
    package_id: str,
    result: dict[str, Any],
) -> Path:
    if package_id not in {"package_a", "package_b"}:
        raise ValueError("invalid anonymous package_id")
    manifest = _object(experiment_dir / "manifest.json")
    config = _object(experiment_dir / "experiment.json")
    control = _object(experiment_dir / "control" / "package_mapping.json")
    if manifest.get("config") != config:
        raise ValueError("manifest/config mismatch; regenerate packages")
    trial_numbers = [item.get("trial") for item in manifest.get("trials", [])]
    if trial not in trial_numbers:
        raise ValueError("trial not in frozen manifest")
    mapping = control.get("trials", {}).get(str(trial), {})
    if package_id not in mapping:
        raise ValueError("package_id not present in backend control mapping")
    imported = dict(result)
    imported.update({
        "experiment_id": experiment_dir.name,
        "trial": trial,
        "package_id": package_id,
        "arm": mapping[package_id],
        "model": config["model"],
        "reasoning_effort": config["reasoning_effort"],
        "public_hashes": manifest["hashes"]["public"],
    })
    path = experiment_dir / "results" / f"trial_{trial}_{package_id}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(
        json.dumps(imported, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


def headline_allowed(experiment_dir: Path, gold_file: Path) -> bool:
    config = _object(experiment_dir / "experiment.json")
    gold = _object(gold_file)
    return config.get("reasoning_effort") != "unknown" and gold.get("status") == "reviewed"
