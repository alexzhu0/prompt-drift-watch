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


def removed_guardrail_lines(baseline: List[str], changed: List[str]) -> List[str]:
    changed_set = {line.lower() for line in changed}
    removed = []
    for line in baseline:
        if line.lower() not in changed_set and contains_any(line, GUARDRAIL_TERMS):
            removed.append(line)
    return removed


def newly_vague_lines(baseline: List[str], changed: List[str]) -> List[str]:
    baseline_set = {line.lower() for line in baseline}
    vague = []
    for line in changed:
        if line.lower() not in baseline_set and contains_any(line, VAGUE_TERMS):
            vague.append(line)
    return vague


def analyze_prompt_drift(baseline_text: str, changed_text: str) -> DriftReport:
    baseline = meaningful_lines(baseline_text)
    changed = meaningful_lines(changed_text)
    removed = removed_guardrail_lines(baseline, changed)
    vague = newly_vague_lines(baseline, changed)
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
        summary=summary,
    )
