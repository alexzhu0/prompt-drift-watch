"""Prompt drift analysis primitives."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from typing import Iterable, List


GUARDRAIL_TERMS = [
    "must",
    "never",
    "do not",
    "only",
    "required",
    "refuse",
    "validate",
    "verify",
    "test",
    "approval",
    "permission",
    "privacy",
    "private",
    "security",
    "secret",
    "credential",
    "source",
    "citation",
]

VAGUE_TERMS = [
    "best effort",
    "maybe",
    "try to",
    "as needed",
    "where appropriate",
    "reasonable",
    "helpful",
    "if possible",
    "generally",
]


@dataclass(frozen=True)
class DriftReport:
    risk_score: int
    status: str
    removed_guardrails: List[str]
    vague_additions: List[str]
    diff: List[str]
    rule_pack: str
    summary: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def normalize_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line.strip())
    line = line.strip("-*#> ").strip()
    line = line.replace("**", "").replace("__", "")
    return line.strip()


def meaningful_lines(text: str) -> List[str]:
    lines = []
    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if line:
            lines.append(line)
    return lines


def contains_any(line: str, terms: Iterable[str]) -> bool:
    lower = line.lower()
    return any(term in lower for term in terms)


def removed_guardrail_lines(
    baseline: List[str],
    changed: List[str],
    guardrail_terms: Iterable[str] = GUARDRAIL_TERMS,
) -> List[str]:
    changed_set = {line.lower() for line in changed}
    removed = []
    for line in baseline:
        if line.lower() not in changed_set and contains_any(line, guardrail_terms):
            removed.append(line)
    return removed


def newly_vague_lines(
    baseline: List[str],
    changed: List[str],
    vague_terms: Iterable[str] = VAGUE_TERMS,
) -> List[str]:
    baseline_set = {line.lower() for line in baseline}
    vague = []
    for line in changed:
        if line.lower() not in baseline_set and contains_any(line, vague_terms):
            vague.append(line)
    return vague


def diff_snippets(baseline: List[str], changed: List[str], limit: int = 12) -> List[str]:
    baseline_set = {line.lower() for line in baseline}
    changed_set = {line.lower() for line in changed}
    snippets = [f"- {line}" for line in baseline if line.lower() not in changed_set]
    snippets.extend(f"+ {line}" for line in changed if line.lower() not in baseline_set)
    return snippets[:limit]


def analyze_prompt_drift(
    baseline_text: str,
    changed_text: str,
    guardrail_terms: Iterable[str] = GUARDRAIL_TERMS,
    vague_terms: Iterable[str] = VAGUE_TERMS,
    rule_pack: str = "default",
) -> DriftReport:
    baseline = meaningful_lines(baseline_text)
    changed = meaningful_lines(changed_text)
    removed = removed_guardrail_lines(baseline, changed, guardrail_terms)
    vague = newly_vague_lines(baseline, changed, vague_terms)
    score = min(100, len(removed) * 45 + len(vague) * 10)

    if score >= 80:
        status = "block"
    elif score >= 40:
        status = "review"
    else:
        status = "pass"

    summary = (
        f"{len(removed)} removed guardrail(s), "
        f"{len(vague)} vague addition(s), risk {score}."
    )
    return DriftReport(
        risk_score=score,
        status=status,
        removed_guardrails=removed,
        vague_additions=vague,
        diff=diff_snippets(baseline, changed),
        rule_pack=rule_pack,
        summary=summary,
    )
