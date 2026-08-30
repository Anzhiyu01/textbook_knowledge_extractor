"""Offline experiment configuration and frozen manifest helpers."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
REQUIRED = {"model", "reasoning_effort", "trials"}

def validate_config(config: dict) -> list[str]:
    errors = []
    if set(config) != REQUIRED: errors.append("experiment.json must contain exactly model, reasoning_effort, trials")
    if not isinstance(config.get("model"), str) or not config.get("model", "").strip(): errors.append("model is required")
    if config.get("reasoning_effort") not in {"not_configurable", "unknown"} and not isinstance(config.get("reasoning_effort"), str): errors.append("reasoning_effort must be a string")
    if not isinstance(config.get("trials"), int) or isinstance(config.get("trials"), bool) or config.get("trials", 0) < 1: errors.append("trials must be a positive integer")
    return errors

def init_experiment(root: Path, experiment_id: str) -> Path:
    if not ID_RE.fullmatch(experiment_id): raise ValueError("experiment_id must be ASCII snake_case")
    path = root / experiment_id; path.mkdir(parents=True, exist_ok=False)
    (path / "experiment.json").write_text(json.dumps({"model":"exact-model-name","reasoning_effort":"unknown","trials":3}, indent=2)+"\n", encoding="utf-8")
    return path

def freeze_manifest(experiment_dir: Path, *, case_file: Path, source_file: Path, skill_dir: Path | None = None, trials: int | None = None) -> dict:
    config = json.loads((experiment_dir / "experiment.json").read_text(encoding="utf-8-sig")); errors = validate_config(config)
    if errors: raise ValueError("; ".join(errors))
    def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
    count = trials if trials is not None else config["trials"]
    manifest = {"manifest_version":"2.4", "experiment_id":experiment_dir.name, "config":config, "hashes":{"case":digest(case_file),"source":digest(source_file)}, "trials":[{"trial":i,"arms":["with_skill","without_skill"]} for i in range(1,count+1)]}
    if skill_dir: manifest["hashes"]["skill"] = hashlib.sha256(b"".join(p.read_bytes() for p in sorted(skill_dir.rglob("*")) if p.is_file())).hexdigest()
    (experiment_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return manifest

def verify_manifest(experiment_dir: Path) -> bool:
    manifest=json.loads((experiment_dir/"manifest.json").read_text(encoding="utf-8-sig")); config=json.loads((experiment_dir/"experiment.json").read_text(encoding="utf-8-sig")); return manifest.get("config") == config

if __name__ == "__main__":
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); i=sub.add_parser("init"); i.add_argument("root",type=Path); i.add_argument("experiment_id"); args=p.parse_args()
    if args.cmd == "init": print(init_experiment(args.root,args.experiment_id))
