import unittest

from prompt_drift_watch.core import analyze_prompt_drift, meaningful_lines


class PromptDriftTests(unittest.TestCase):
    def test_flags_removed_guardrails_and_vague_additions(self):
        baseline = """
        You must cite sources.
        Never reveal secrets, credentials, or private user data.
        Answer concisely.
        """
        changed = """
        You must cite sources.
        Try to be helpful where appropriate.
        Answer concisely.
        """
        report = analyze_prompt_drift(baseline, changed)

        self.assertEqual(report.status, "review")
        self.assertGreaterEqual(report.risk_score, 50)
        self.assertEqual(
            report.removed_guardrails,
            ["Never reveal secrets, credentials, or private user data."],
        )
        self.assertEqual(report.vague_additions, ["Try to be helpful where appropriate."])

    def test_passes_when_no_risky_change_is_detected(self):
        baseline = "You must cite sources.\nAnswer concisely."
        changed = "You must cite sources.\nAnswer concisely.\nUse bullet points."
        report = analyze_prompt_drift(baseline, changed)

        self.assertEqual(report.status, "pass")
        self.assertEqual(report.risk_score, 0)

    def test_meaningful_lines_strips_markdown_markers(self):
        self.assertEqual(meaningful_lines("- **Never** reveal secrets."), ["Never reveal secrets."])

    def test_report_includes_diff_snippets(self):
        report = analyze_prompt_drift("Never reveal secrets.", "Try to be helpful.")

        self.assertIn("- Never reveal secrets.", report.diff)
        self.assertIn("+ Try to be helpful.", report.diff)

    def test_agent_instruction_categories_are_reported(self):
        baseline = """
        You must stay inside the workspace sandbox.
        Ask for approval before destructive git reset commands.
        Verify tests before claiming completion.
        """
        changed = """
        Feel free to change files as needed.
        Probably run tests if possible.
        """

        report = analyze_prompt_drift(baseline, changed)

        self.assertEqual(report.status, "block")
        self.assertIn("approval", report.risk_categories)
        self.assertIn("scope", report.risk_categories)
        self.assertIn("verification", report.risk_categories)


if __name__ == "__main__":
    unittest.main()
