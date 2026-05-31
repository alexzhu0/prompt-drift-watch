import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from prompt_drift_watch.cli import main, run


class CliTests(unittest.TestCase):
    def test_run_outputs_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "baseline.md"
            changed = root / "changed.md"
            baseline.write_text("Never expose secrets.\n", encoding="utf-8")
            changed.write_text("Try to be helpful where appropriate.\n", encoding="utf-8")

            payload = json.loads(run(str(baseline), str(changed), "json"))

        self.assertEqual(payload["status"], "review")
        self.assertEqual(payload["risk_score"], 55)

    def test_fail_on_risk_returns_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "baseline.md"
            changed = root / "changed.md"
            baseline.write_text("Never expose secrets.\n", encoding="utf-8")
            changed.write_text("Try to be helpful where appropriate.\n", encoding="utf-8")

            with redirect_stdout(StringIO()):
                code = main([str(baseline), str(changed), "--fail-on-risk", "50"])

        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
