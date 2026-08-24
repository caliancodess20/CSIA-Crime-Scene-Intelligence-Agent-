import unittest

from .next_step_rules import suggest_next_steps


class TestNextStepRules(unittest.TestCase):

    def test_evidence_requires_forensic_analysis(self):
        timeline = [
            {
                "event": "Case created",
                "timestamp": "2026-08-24 10:00"
            },
            {
                "event": "Evidence collected",
                "timestamp": "2026-08-24 15:30"
            }
        ]

        suggestions = suggest_next_steps(timeline)

        self.assertIn(
            "Perform forensic analysis on the collected evidence.",
            suggestions
        )

    def test_witness_statement_requires_suspect_interview(self):
        timeline = [
            {
                "event": "Witness statement",
                "timestamp": "2026-08-24 14:00"
            }
        ]

        suggestions = suggest_next_steps(timeline)

        self.assertIn(
            "Conduct a suspect interview based on available witness information.",
            suggestions
        )


if __name__ == "__main__":
    unittest.main()