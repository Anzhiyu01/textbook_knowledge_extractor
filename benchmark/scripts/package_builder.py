"""Build offline paired benchmark packages from a frozen manifest."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

def build_packages(experiment_dir: Path, *, case: Path, textbook: Path, skill_dir: Path, prompt: Path) -> list[Path]:
    manifest = json.loads((experiment_dir / "manifest.json").read_text(encoding="utf-8"))
    if json.loads((experiment_dir / "experiment.json").read_text(encoding="utf-8")) != manifest["config"]:
        raise ValueError("experiment.json changed; regenerate manifest")
    outputs=[]
    for trial in manifest["trials"]:
        for arm in trial["arms"]:
            dest=experiment_dir / "packages" / f"trial_{trial['trial']}" / arm; dest.mkdir(parents=True, exist_ok=True)
            for source in (case,textbook,prompt): shutil.copy2(source, dest / source.name)
            if arm == "with_skill": shutil.copytree(skill_dir, dest / "skill", dirs_exist_ok=True)
            package_manifest={"experiment_id":experiment_dir.name,"trial":trial["trial"],"arm":arm,"files":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file()}}
            (dest / "package_manifest.json").write_text(json.dumps(package_manifest, indent=2)+"\n", encoding="utf-8"); outputs.append(dest)
    return outputs
