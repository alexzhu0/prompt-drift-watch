"""CLI for prompt-drift-watch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .core import GUARDRAIL_TERMS, VAGUE_TERMS, DriftReport, analyze_prompt_drift


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect risky changes in AI prompt and agent instruction files."
    )
    parser.add_argument("baseline", help="Baseline prompt or instruction file")
    parser.add_argument("changed", help="Changed prompt or instruction file")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--fail-on-risk",
        type=int,
        default=None,
        metavar="SCORE",
        help="Exit with code 2 when risk score is at least SCORE",
    )
    parser.add_argument(
        "--rules",
        default=None,
        help="Optional JSON rule pack with guardrail_terms and vague_terms arrays",
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Include compact removed/added line snippets in text output",
    )
    return parser


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_rule_pack(path: str | None) -> tuple[str, list[str], list[str]]:
    if not path:
        return "default", list(GUARDRAIL_TERMS), list(VAGUE_TERMS)
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    name = str(payload.get("name") or Path(path).stem)
    guardrails = [str(item) for item in payload.get("guardrail_terms", GUARDRAIL_TERMS)]
    vague = [str(item) for item in payload.get("vague_terms", VAGUE_TERMS)]
    return name, guardrails, vague


def format_text(report: DriftReport, show_diff: bool = False) -> str:
    lines = [
        f"Risk score: {report.risk_score}",
        f"Status: {report.status}",
        f"Rule pack: {report.rule_pack}",
        "",
    ]
    if report.removed_guardrails:
        lines.append("Removed guardrails:")
        lines.extend(f"- {line}" for line in report.removed_guardrails)
        lines.append("")
    if report.vague_additions:
        lines.append("Vague additions:")
        lines.extend(f"- {line}" for line in report.vague_additions)
        lines.append("")
    if show_diff and report.diff:
        lines.append("Diff snippets:")
        lines.extend(report.diff)
        lines.append("")
    lines.append(report.summary)
    return "\n".join(lines).rstrip()


def run(
    baseline_path: str,
    changed_path: str,
    output_format: str = "text",
    rules_path: str | None = None,
    show_diff: bool = False,
) -> str:
    rule_pack, guardrails, vague = load_rule_pack(rules_path)
    report = analyze_prompt_drift(
        read_file(baseline_path),
        read_file(changed_path),
        guardrail_terms=guardrails,
        vague_terms=vague,
        rule_pack=rule_pack,
    )
    if output_format == "json":
        return report.to_json()
    return format_text(report, show_diff=show_diff)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    rule_pack, guardrails, vague = load_rule_pack(args.rules)
    report = analyze_prompt_drift(
        read_file(args.baseline),
        read_file(args.changed),
        guardrail_terms=guardrails,
        vague_terms=vague,
        rule_pack=rule_pack,
    )
    print(report.to_json() if args.format == "json" else format_text(report, args.show_diff))
    if args.fail_on_risk is not None and report.risk_score >= args.fail_on_risk:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
