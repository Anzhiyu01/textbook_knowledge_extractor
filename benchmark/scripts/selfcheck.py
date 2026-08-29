#!/usr/bin/env python3
"""Deterministic pre-acceptance checks for an extraction run.

``validate_submission.py`` remains the benchmark-facing validator.  This
small companion is intended to be run *before every acceptance round* in the
model's run directory.  It reports facts that can be recomputed from the
case, source, audit and knowledge files (rather than relying on an AI's
self-report): source/slice hashes, candidate spans, heading parameters,
heading leaks and block-id order.

The default output is a stable, human-readable checklist.  ``--json`` emits
the same checklist as machine-readable JSON for a run log or orchestrator.
Exit status is 0 when every check passes, 1 when one or more checks fail, and
2 when the inputs cannot be read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

_SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skill" / "textbook-knowledge-extractor" / "scripts"
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))

try:  # Script execution (``python scripts/selfcheck.py``).
    from bilingual import infer_terms, normalise_terms, validate_bilingual_terms
    from leak_patterns import exercise_leak_matches, proof_leak_matches
except ImportError:  # pragma: no cover - package import fallback
    from .bilingual import infer_terms, normalise_terms, validate_bilingual_terms
    from .leak_patterns import exercise_leak_matches, proof_leak_matches

try:
    from contract import BLOCK_ID_RE, KNOWLEDGE_BLOCK_RE, CONTAINER_TYPES, valid_block_id
except ImportError:  # pragma: no cover
    from .contract import BLOCK_ID_RE, KNOWLEDGE_BLOCK_RE, CONTAINER_TYPES, valid_block_id

from scope_markdown import discover_candidates


BLOCK_ID_RE = KNOWLEDGE_BLOCK_RE
HEADING_PARAM_RE = re.compile(r"^\s*#{1,6}(?:[ \t]|$)")
ATX_LINE_RE = re.compile(r"^\s*#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
CONTAINER_TYPES = {"heading", "paragraph", "display_formula", "fenced_code", "callout", "html_table", "list", "other"}


@dataclass(frozen=True)
class Check:
    """One deterministic check in the emitted checklist."""

    name: str
    passed: bool
    detail: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _target_line(target: dict[str, Any], name: str) -> int | None:
    # v2 cases call these expected_*; a small number of hand-written cases use
    # start_line/end_line directly.  Supporting both keeps selfcheck useful
    # without changing the frozen case format.
    value = target.get(f"expected_{name}", target.get(name))
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _target_heading(target: dict[str, Any], name: str) -> str | None:
    value = target.get(name)
    return value.strip() if isinstance(value, str) else None


def _heading_text(line: str) -> str | None:
    match = ATX_LINE_RE.match(line)
    if match:
        return match.group(1).strip()
    return None


def _add(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name=name, passed=bool(passed), detail=str(detail)))


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _candidate_id_number(block_id: str) -> int | None:
    match = re.fullmatch(r"K-(\d{3,})", block_id)
    return int(match.group(1)) if match else None


def _format_failures(checks: Iterable[Check]) -> list[str]:
    return [f"{check.name}: {check.detail}" for check in checks if not check.passed]


def run_checks(
    case_path: Path,
    submission: Path,
    *,
    requested_start_heading: str | None = None,
    requested_end_heading: str | None = None,
    require_bilingual: bool = False,
) -> tuple[dict[str, Any], int]:
    """Run all checks and return ``(report, exit_code)``.

    Input/read errors are represented by exit code 2.  A malformed audit is a
    normal failed checklist (exit code 1), which is useful when repairing a
    run and preserves all available evidence in the report.
    """

    checks: list[Check] = []
    try:
        case = _read_json(case_path)
    except Exception as exc:
        return {
            "status": "ERROR",
            "case_file": str(case_path),
            "checks": [],
            "failures": [f"cannot read case: {exc}"],
        }, 2

    submission = submission.resolve()
    audit_path = submission / "audit.json"
    knowledge_path = submission / "knowledge.md"
    try:
        audit = _read_json(audit_path)
    except Exception as exc:
        audit = {}
        _add(checks, "audit_json", False, f"cannot read audit.json: {exc}")
    try:
        knowledge = knowledge_path.read_text(encoding="utf-8")
    except Exception as exc:
        knowledge = ""
        _add(checks, "knowledge_utf8", False, f"cannot read knowledge.md: {exc}")

    source_rel = case.get("source_file")
    source_path = (case_path.parent / source_rel).resolve() if isinstance(source_rel, str) else None
    source_bytes = b""
    source_lines: list[str] = []
    if source_path is None:
        _add(checks, "source_readable", False, "case.source_file is missing")
    else:
        try:
            source_bytes = source_path.read_bytes()
            source_text = source_bytes.decode("utf-8-sig")
            source_lines = source_text.splitlines()
            _add(checks, "source_readable", True, f"{len(source_lines)} lines, UTF-8")
        except Exception as exc:
            _add(checks, "source_readable", False, f"cannot read source: {exc}")

    expected_source_hash = str(case.get("source_sha256", "")).upper()
    actual_source_hash = _sha256(source_bytes) if source_bytes else ""
    _add(
        checks,
        "source_sha256",
        bool(actual_source_hash and expected_source_hash and actual_source_hash == expected_source_hash),
        f"expected {expected_source_hash or '<missing>'}; actual {actual_source_hash or '<unavailable>'}",
    )

    target = case.get("target") if isinstance(case.get("target"), dict) else {}
    start_line = _target_line(target, "start_line")
    end_line = _target_line(target, "end_line")
    target_start_heading = _target_heading(target, "start_heading")
    target_end_heading = _target_heading(target, "end_before_heading")
    boundaries = audit.get("boundaries") if isinstance(audit.get("boundaries"), dict) else {}
    scope = audit.get("scope_preprocessing") if isinstance(audit.get("scope_preprocessing"), dict) else {}
    strict_v22 = str(audit.get("audit_schema_version", "")) == "2.2"
    strict_v23 = str(audit.get("audit_schema_version", "")) == "2.3"

    if start_line is None or end_line is None:
        _add(checks, "target_range", False, "case.target must provide integer start_line/end_line")
    else:
        range_ok = bool(source_lines) and 1 <= start_line <= end_line <= len(source_lines)
        _add(checks, "target_range", range_ok, f"requested {start_line}..{end_line}; source has {len(source_lines)} lines")

    if source_lines and start_line is not None and end_line is not None and 1 <= start_line <= end_line <= len(source_lines):
        slice_text = "\n".join(source_lines[start_line - 1 : end_line]) + "\n"
        actual_slice_hash = _sha256(slice_text.encode("utf-8"))
        recorded_slice_hash = str(scope.get("slice_sha256", "")).upper()
        _add(
            checks,
            "slice_sha256",
            bool(recorded_slice_hash and recorded_slice_hash == actual_slice_hash),
            f"expected {actual_slice_hash}; recorded {recorded_slice_hash or '<missing>'}",
        )
        recorded_count = scope.get("slice_line_count")
        _add(
            checks,
            "slice_line_count",
            recorded_count == end_line - start_line + 1,
            f"expected {end_line - start_line + 1}; recorded {recorded_count!r}",
        )
        # A line-range selection may intentionally start in prose.  Only
        # compare a canonical heading when the selected source line actually
        # parses as an ATX heading; arbitrary line boundaries remain valid.
        if target_start_heading and _heading_text(source_lines[start_line - 1]) is not None:
            actual = _heading_text(source_lines[start_line - 1])
            # Case manifests historically store the ATX marker in the target
            # heading.  Compare both the literal line and its normalized text.
            normalized_target = re.sub(r"^\s*#{1,6}[ \t]*", "", target_start_heading).strip()
            _add(
                checks,
                "start_boundary_heading",
                actual == normalized_target or source_lines[start_line - 1].strip() == target_start_heading,
                f"expected {target_start_heading!r}; source line {start_line} is {source_lines[start_line - 1]!r}",
            )

    # A stale or hand-edited audit should be visible even when the source hash
    # check already failed.
    if expected_source_hash:
        _add(
            checks,
            "audit_source_sha256",
            str(audit.get("source_sha256", "")).upper() == expected_source_hash,
            f"audit {audit.get('source_sha256', '<missing>')!r}; case {expected_source_hash}",
        )
    for field, expected in (
        ("start_heading", target_start_heading),
        ("end_before_heading", target_end_heading),
    ):
        actual = boundaries.get(field)
        _add(checks, f"boundary_{field}", expected is None or actual == expected, f"expected {expected!r}; recorded {actual!r}")
    for field, expected in (("start_line", start_line), ("end_line", end_line)):
        actual = boundaries.get(field)
        _add(checks, f"boundary_{field}", expected is None or actual == expected, f"expected {expected!r}; recorded {actual!r}")
    if strict_v23:
        evidence = boundaries.get("evidence")
        evidence_ok = isinstance(evidence, list) and len(evidence) >= 2
        evidence_errors: list[str] = []
        if evidence_ok:
            for item in evidence:
                if not isinstance(item, dict) or not all(k in item for k in ("kind", "line", "text", "reliability", "relation")):
                    evidence_errors.append("boundary evidence requires kind/line/text/reliability/relation")
                    continue
                line = item.get("line")
                if not isinstance(line, int) or not 1 <= line <= len(source_lines):
                    evidence_errors.append(f"boundary evidence line out of range: {line!r}")
        _add(checks, "boundary_evidence", evidence_ok and not evidence_errors, "; ".join(evidence_errors) or "multiple boundary evidence records")

    # Heading arguments passed to scope_markdown are plain heading text.  The
    # canonical case boundary may include ``##`` for backwards compatibility,
    # so only explicit request/parameter fields are failures here.
    parameter_values: list[tuple[str, str | None]] = [
        ("requested_start_heading", requested_start_heading),
        ("requested_end_before_heading", requested_end_heading),
    ]
    for key in ("start_heading_param", "end_before_heading_param", "requested_start_heading", "requested_end_before_heading"):
        value = scope.get(key)
        if isinstance(value, str):
            parameter_values.append((key, value))
    for name, value in parameter_values:
        if value is not None:
            ok = not bool(HEADING_PARAM_RE.match(value))
            _add(checks, f"heading_parameter_{name}", ok, f"{value!r} should omit the Markdown # prefix")
    if not any(value is not None for _, value in parameter_values):
        _add(checks, "heading_parameters_recorded", True, "no explicit tool parameters recorded; canonical boundary text retained")

    candidates = audit.get("candidates") if isinstance(audit.get("candidates"), list) else []
    _add(checks, "candidate_inventory", bool(candidates), f"{len(candidates)} candidate record(s)")
    seen_ids: set[str] = set()
    candidate_spans: list[tuple[int, int, str]] = []
    candidate_errors: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            candidate_errors.append("candidate is not an object")
            continue
        block_id = candidate.get("block_id")
        start = candidate.get("source_start_line")
        end = candidate.get("source_end_line")
        if not valid_block_id(block_id):
            candidate_errors.append(f"invalid block_id {block_id!r}")
            continue
        if block_id in seen_ids:
            candidate_errors.append(f"duplicate block_id {block_id}")
        seen_ids.add(block_id)
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or start > end:
            candidate_errors.append(f"invalid span for {block_id}")
            continue
        candidate_spans.append((start, end, block_id))
        if source_lines and (start < 1 or end > len(source_lines)):
            candidate_errors.append(f"{block_id} span {start}..{end} is outside source")
        if start_line is not None and end_line is not None and (start < start_line or end > end_line):
            candidate_errors.append(f"{block_id} span {start}..{end} is outside target {start_line}..{end_line}")
        numeric_id = _candidate_id_number(block_id)
        if case.get("block_id_format") == "K-{source_start_line:03d}" and numeric_id is not None and numeric_id != start:
            candidate_errors.append(f"{block_id} does not encode source_start_line {start}")
        if candidate.get("decision") not in {"include", "exclude"}:
            candidate_errors.append(f"{block_id} has invalid decision {candidate.get('decision')!r}")
        position = candidate.get("source_position")
        if strict_v22 and not isinstance(position, dict):
            candidate_errors.append(f"{block_id} missing source_position in audit v2.2")
        if isinstance(position, dict):
            marker_start = position.get("marker_start_line")
            marker_end = position.get("marker_end_line", marker_start)
            content_start = position.get("content_start_line", marker_start)
            content_end = position.get("content_end_line", marker_end)
            ctype = position.get("container_type", candidate.get("container_type"))
            if ctype not in CONTAINER_TYPES:
                candidate_errors.append(f"{block_id} invalid container_type {ctype!r}")
            if marker_start != start or not all(isinstance(v, int) for v in (marker_start, marker_end, content_start, content_end)):
                candidate_errors.append(f"{block_id} source_position marker_start_line must equal source_start_line")
            elif not (start <= marker_end <= end and start <= content_start <= content_end <= end):
                candidate_errors.append(f"{block_id} source_position ranges are outside candidate span")
        for subspan in candidate.get("source_subspans", []) if isinstance(candidate.get("source_subspans"), list) else []:
            if not isinstance(subspan, dict):
                candidate_errors.append(f"{block_id} has non-object source_subspan")
                continue
            ss, se = subspan.get("source_start_line"), subspan.get("source_end_line")
            if not isinstance(ss, int) or not isinstance(se, int) or ss > se or ss < start or se > end:
                candidate_errors.append(f"{block_id} has invalid source_subspan span")
            for key in ("start_column", "end_column"):
                if key in subspan and (not isinstance(subspan[key], int) or isinstance(subspan[key], bool) or subspan[key] < 1):
                    candidate_errors.append(f"{block_id} source_subspan {key} must be a positive integer")
            if "start_column" in subspan or "end_column" in subspan:
                if not ("start_column" in subspan and "end_column" in subspan and subspan["start_column"] < subspan["end_column"]):
                    candidate_errors.append(f"{block_id} source_subspan columns must be 1-based half-open")
        if strict_v23 and candidate.get("mixed") is True:
            for field in ("retained_conclusion_anchor", "excluded_intervals", "formula_token_map", "source_subspans"):
                if field not in candidate:
                    candidate_errors.append(f"{block_id} mixed candidate missing {field}")
            if not isinstance(candidate.get("retained_conclusion_anchor"), str) or not candidate["retained_conclusion_anchor"].strip():
                candidate_errors.append(f"{block_id} retained conclusion anchor is empty")
            for interval in candidate.get("excluded_intervals", []) if isinstance(candidate.get("excluded_intervals"), list) else []:
                if not isinstance(interval, dict) or not all(k in interval for k in ("start_line", "end_line", "reason")):
                    candidate_errors.append(f"{block_id} invalid excluded interval")
            for token in candidate.get("formula_token_map", []) if isinstance(candidate.get("formula_token_map"), list) else []:
                if not isinstance(token, dict) or not token.get("source") or not token.get("retained"):
                    candidate_errors.append(f"{block_id} invalid formula token map entry")
    _add(checks, "candidate_spans", not candidate_errors, "; ".join(candidate_errors) or "all spans and decisions are in range")

    if strict_v23 and source_lines and start_line is not None and end_line is not None:
        generated = discover_candidates(source_lines, start_line, end_line)
        declared = [
            {k: c.get(k) for k in ("block_id", "source_start_line", "source_end_line", "container_type", "signal", "text_anchor")}
            for c in candidates if isinstance(c, dict)
        ]
        expected = [{k: row.get(k) for k in ("block_id", "source_start_line", "source_end_line", "container_type", "signal", "text_anchor")} for row in generated]
        _add(checks, "independent_candidate_index", declared == expected, f"generated {len(expected)} unit(s); declared {len(declared)}")
        discovery = audit.get("candidate_discovery") if isinstance(audit.get("candidate_discovery"), dict) else {}
        index_ok = False
        if isinstance(discovery.get("index_file"), str):
            try:
                index_bytes = (submission / discovery["index_file"]).resolve().read_bytes()
                index_ok = str(discovery.get("index_sha256", "")).upper() == _sha256(index_bytes)
            except OSError:
                pass
        _add(checks, "candidate_index_artifact", index_ok, "candidate index file and hash verified" if index_ok else "candidate index artifact missing or hash mismatch")

    ordered_candidates = sorted(candidate_spans, key=lambda item: (item[0], item[1], item[2]))
    inventory_order_ok = candidate_spans == ordered_candidates
    _add(checks, "candidate_source_order", inventory_order_ok, "candidate records are in source order" if inventory_order_ok else "candidate records are not in source order")

    proof_matches = proof_leak_matches(knowledge)
    exercise_matches = exercise_leak_matches(knowledge)
    proof_detail = "none" if not proof_matches else ", ".join(f"line {_line_number(knowledge, m.start())}: {m.group(0).strip()}" for m in proof_matches)
    exercise_detail = "none" if not exercise_matches else ", ".join(f"line {_line_number(knowledge, m.start())}: {m.group(0).strip()}" for m in exercise_matches)
    _add(checks, "proof_leaks", not proof_matches, proof_detail)
    _add(checks, "exercise_leaks", not exercise_matches, exercise_detail)

    knowledge_ids = [match.group(1) for match in BLOCK_ID_RE.finditer(knowledge)]
    included = [
        (start, block_id)
        for start, _end, block_id in candidate_spans
        if next((c for c in candidates if isinstance(c, dict) and c.get("block_id") == block_id and c.get("decision") == "include"), None)
    ]
    expected_ids = [block_id for _start, block_id in sorted(included)]
    order_ok = knowledge_ids == expected_ids
    detail = f"included audit ids {expected_ids}; found {knowledge_ids}"
    _add(checks, "included_id_order", order_ok, detail)
    # v2.1 report name retained for downstream runlog parsers.
    _add(checks, "k_id_order", order_ok, detail)

    judgments = audit.get("extraction_judgments")
    if strict_v22:
        judgment_errors = []
        if not isinstance(judgments, list):
            judgment_errors.append("audit v2.2 requires extraction_judgments array")
        else:
            for item in judgments:
                if not isinstance(item, dict):
                    judgment_errors.append("v2.2 extraction_judgments entries must be objects")
                    continue
                for field in ("judgment_id", "source_start_line", "source_end_line", "classification", "decision", "basis"):
                    if field not in item:
                        judgment_errors.append(f"judgment missing {field}")
        _add(checks, "extraction_judgments", not judgment_errors, "; ".join(judgment_errors) or "v2.2 judgments are structured")
        discovery = audit.get("candidate_discovery")
        _add(checks, "candidate_discovery", isinstance(discovery, dict) and discovery.get("all_slice_units_accounted") is True, "v2.2 candidate discovery is explicit" if isinstance(discovery, dict) else "audit v2.2 requires candidate_discovery")

    if require_bilingual:
        raw_terms = audit.get("bilingual_terms")
        terms, term_errors = normalise_terms(raw_terms)
        if raw_terms is not None and not terms:
            term_errors.append(
                "双语术语表为空: --require-bilingual 至少需要一条 bilingual_terms 记录"
            )
        elif raw_terms is None and not terms:
            terms = infer_terms(knowledge, expected_ids)
            if not terms:
                term_errors.append(
                    "双语术语表缺失: --require-bilingual 需要 audit.bilingual_terms，且无法从纳入块推断术语"
                )
        for term in terms:
            if term.block_id and term.block_id not in set(expected_ids):
                term_errors.append(
                    f"双语术语块不是纳入候选: {term.term}（{term.block_id}）"
                )
        bilingual_errors = term_errors + validate_bilingual_terms(
            knowledge, terms, included_block_ids=set(expected_ids)
        )
        _add(checks, "bilingual_first_occurrence", not bilingual_errors, "; ".join(bilingual_errors) or f"validated {len(terms)} term(s)")

    failures = _format_failures(checks)
    report = {
        "status": "PASS" if not failures else "FAIL",
        "structural_status": "pass" if not failures else "fail",
        "coverage_status": "independently-indexed; human content review still required" if strict_v23 and not failures else "not independently confirmed",
        "human_review_status": "required",
        "case_id": case.get("case_id"),
        "case_file": str(case_path.resolve()),
        "submission": str(submission),
        "checks": [asdict(check) for check in checks],
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, 0 if not failures else 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, type=Path, help="case manifest JSON")
    parser.add_argument("--submission", required=True, type=Path, help="run/submission directory")
    parser.add_argument("--start-heading", dest="requested_start_heading", help="optional tool parameter to audit")
    parser.add_argument("--end-before-heading", dest="requested_end_heading", help="optional tool parameter to audit")
    parser.add_argument(
        "--require-bilingual",
        "--bilingual",
        dest="require_bilingual",
        action="store_true",
        help="also check configured bilingual first occurrences",
    )
    parser.add_argument("--json", action="store_true", help="emit a JSON checklist instead of text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report, exit_code = run_checks(
        args.case.resolve(),
        args.submission.resolve(),
        requested_start_heading=args.requested_start_heading,
        requested_end_heading=args.requested_end_heading,
        require_bilingual=args.require_bilingual,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"SELF-CHECK {report['status']}")
        for check in report.get("checks", []):
            marker = "PASS" if check["passed"] else "FAIL"
            print(f"[{marker}] {check['name']}: {check['detail']}")
        if report.get("failures"):
            print("Failures:")
            for failure in report["failures"]:
                print(f"- {failure}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
