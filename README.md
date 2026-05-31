# Prompt Drift Watch

Detect risky changes in AI prompt and agent instruction files before they ship.

## Why

Prompt and agent instruction diffs are easy to skim and hard to judge. A small wording change can remove a guardrail, soften a requirement, or add vague language that makes downstream behavior less reliable.

`prompt-drift-watch` compares a baseline prompt with a changed prompt and highlights:

- Removed guardrail lines.
- Newly added vague instructions.
- A simple risk score that can be used in review or CI.

It is intentionally local and dependency-free.

## Install

```bash
git clone https://github.com/alexzhu0/prompt-drift-watch.git
cd prompt-drift-watch
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md
```

Example output:

```text
Risk score: 55
Status: review

Removed guardrails:
- Never reveal secrets, credentials, or private user data.

Vague additions:
- Try to be helpful where appropriate.
```

## Examples

Write JSON for a CI step:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --format json
```

Fail when risk is high:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --fail-on-risk 50
```

## API

The public Python API is small:

```python
from prompt_drift_watch.core import analyze_prompt_drift

result = analyze_prompt_drift(baseline_text, changed_text)
print(result.risk_score)
```

`analyze_prompt_drift` returns a `DriftReport` dataclass with:

- `risk_score`
- `status`
- `removed_guardrails`
- `vague_additions`
- `summary`

## FAQ

**Does this call an AI model?**

No. The first version is deterministic and standard-library only.

**Does this replace human prompt review?**

No. It is a pre-review signal that catches easy-to-miss risk.

**Can I tune the rules?**

The first version ships with fixed heuristics. Rule configuration is a good `v0.2.0` candidate after real examples arrive.

## Contributing

Issues and pull requests are welcome when they include a concrete prompt diff and expected output.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT

