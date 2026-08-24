import unittest

from .timeline_builder import build_timeline
from .next_step_rules import suggest_next_steps


class TestFullInvestigationFlow(unittest.TestCase):

    def test_timeline_and_next_steps(self):
        events = [
            {
                "event": "Evidence collected",
                "timestamp": "2026-08-24 15:30"
            },
            {
                "event": "Case created",
                "timestamp": "2026-08-24 10:00"
            },
            {
                "event": "Witness statement",
                "timestamp": "2026-08-24 14:00"
            }
        ]

        timeline = build_timeline(events)
        suggestions = suggest_next_steps(timeline)

        self.assertEqual(
            timeline[0]["event"],
            "Case created"
        )

        self.assertIn(
            "Perform forensic analysis on the collected evidence.",
            suggestions
        )

        self.assertIn(
            "Conduct a suspect interview based on available witness information.",
            suggestions
        )


if __name__ == "__main__":
    unittest.main()