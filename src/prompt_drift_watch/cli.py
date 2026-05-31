"""CLI for prompt-drift-watch."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import DriftReport, analyze_prompt_drift


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
    return parser


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def format_text(report: DriftReport) -> str:
    lines = [
        f"Risk score: {report.risk_score}",
        f"Status: {report.status}",
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
    lines.append(report.summary)
    return "\n".join(lines).rstrip()


def run(baseline_path: str, changed_path: str, output_format: str = "text") -> str:
    report = analyze_prompt_drift(read_file(baseline_path), read_file(changed_path))
    if output_format == "json":
        return report.to_json()
    return format_text(report)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report = analyze_prompt_drift(read_file(args.baseline), read_file(args.changed))
    print(report.to_json() if args.format == "json" else format_text(report))
    if args.fail_on_risk is not None and report.risk_score >= args.fail_on_risk:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

