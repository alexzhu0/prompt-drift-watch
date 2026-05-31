# Prompt Drift Watch

Detect risky prompt and coding-agent instruction changes before they ship.

For maintainers reviewing AGENTS.md, Claude/Codex/Cursor rules, system prompts, and prompt files where normal diffs miss removed guardrails.

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --format github
```

## Why

Prompt and agent-instruction diffs often look harmless while removing guardrails, weakening permissions, relaxing sandbox boundaries, or adding vague behavior. Those changes can break an agent workflow before evals even run.

Prompt Drift Watch is a dependency-light CI gate for instruction drift. It catches risky edits first, then you can run `promptbeat-lite` for behavioral regression fixtures.

## Install

```bash
git clone https://github.com/alexzhu0/prompt-drift-watch.git
cd prompt-drift-watch
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --show-diff
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --show-diff
```

Agent instruction drift:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --show-diff
```

GitHub Actions annotation format:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --format github --fail-on-risk 80
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_prompt.md examples/changed_prompt.md --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m prompt_drift_watch --help`
- Main demo: `PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --show-diff`
- CI annotation: `PYTHONPATH=src python3 -m prompt_drift_watch examples/baseline_agents.md examples/changed_agents.md --format github --fail-on-risk 80`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Removed guardrail detection
- New vague-instruction detection
- Compact diff snippets for review
- JSON output for CI artifacts
- GitHub Actions annotation output
- Agent instruction risk categories: approval, citation, safety, scope, and verification
- Custom JSON rule packs
- Risk threshold exit codes

## API

The public Python surface is intentionally small:

```python
from prompt_drift_watch.core import analyze_prompt_drift
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

Star this if you review agent rules and want a deterministic first-pass risk signal before expensive evals or hosted tools.

## Related Tools

- Run `promptbeat-lite` after this gate for fixture-based regression checks.
- Use `repo-to-ai-brief` to include changed instruction files in agent review context.
- Use `context-window-doctor` when long instruction bundles become duplicated or contradictory.

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
