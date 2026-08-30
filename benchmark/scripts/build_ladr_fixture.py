"""Materialize the public LADR v2.4 fixture and explicit human-review gold."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def build(root: Path) -> None:
    source = root / "input" / "Linear Algebra Done Right_clear.md"
    index = json.loads((root / "input" / "candidate_index.json").read_text(encoding="utf-8-sig"))
    gold = {"status":"human_review_required","candidate_count":len(index["candidates"]),"items":[{"block_id":c["block_id"],"decision":None,"review":"required"} for c in index["candidates"]]}
    (root / "gold").mkdir(exist_ok=True)
    (root / "gold" / "candidate_gold.json").write_text(json.dumps(gold, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    metadata={"title":"Linear Algebra Done Right","author":"Sheldon Axler","edition":"4th edition","source":"cleaned Markdown source, lines 499-1663","license":"CC BY-NC 4.0","license_url":"https://creativecommons.org/licenses/by-nc/4.0/","target_lines":[499,1631],"boundary_context_lines":[1632,1663],"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest().upper()}
    (root / "input" / "source_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__": build(Path(__file__).resolve().parents[1] / "ladr_ch1")
