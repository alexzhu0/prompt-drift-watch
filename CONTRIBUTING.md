# Contributing

Good contributions include:

- A concrete prompt diff that should be flagged.
- A false positive that should not be flagged.
- A focused rule improvement with tests.
- Documentation that makes the quickstart clearer.

Please avoid:

- Broad rewrites without an issue.
- Promotion-only issues or comments.
- Adding external services without a clear reason.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

