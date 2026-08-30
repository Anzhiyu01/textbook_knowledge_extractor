"""Import user-produced arm results without connecting to model APIs."""
from __future__ import annotations
import json
from pathlib import Path

def import_result(experiment_dir: Path, trial: int, arm: str, result: dict) -> Path:
    if arm not in {"with_skill", "without_skill"}: raise ValueError("invalid arm")
    manifest = json.loads((experiment_dir / "manifest.json").read_text(encoding="utf-8-sig"))
    config = json.loads((experiment_dir / "experiment.json").read_text(encoding="utf-8-sig"))
    if manifest.get("config") != config: raise ValueError("manifest/config mismatch; regenerate packages")
    if trial not in [x["trial"] for x in manifest.get("trials", [])]: raise ValueError("trial not in frozen manifest")
    result = dict(result); result.update({"experiment_id": experiment_dir.name, "trial": trial, "arm": arm, "model": config["model"], "reasoning_effort": config["reasoning_effort"]})
    path = experiment_dir / "results" / f"trial_{trial}_{arm}.json"; path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8"); return path

def headline_allowed(experiment_dir: Path) -> bool:
    config=json.loads((experiment_dir/"experiment.json").read_text(encoding="utf-8-sig")); gold=experiment_dir.parent.parent/'ladr_ch1'/'gold'/'candidate_gold.json'
    return config.get("reasoning_effort") not in {"unknown"} and (not gold.exists() or json.loads(gold.read_text(encoding='utf-8')).get('status') != 'human_review_required')
