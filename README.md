# Prompt Drift Watch

Detect risky prompt and agent instruction changes before they ship.

## Why

Prompt diffs often look harmless while removing guardrails, weakening safety wording, or adding vague behavior.

This is a flagship HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/prompt-drift-watch.git
cd prompt-drift-watch
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --show-diff
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --show-diff
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m prompt_drift_watch --help`
- Main demo: `PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --show-diff`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Removed guardrail detection
- New vague-instruction detection
- Compact diff snippets for review
- JSON output for CI artifacts
- Custom JSON rule packs
- Risk threshold exit codes

## API

The public Python surface is intentionally small:

```python
from prompt_drift_watch.core import analyze_prompt_drift
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It gives prompt reviewers a deterministic first-pass risk signal without needing a hosted eval stack.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
