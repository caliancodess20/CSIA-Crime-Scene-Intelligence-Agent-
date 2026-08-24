import unittest

from .timeline_builder import build_timeline


class TestTimelineBuilder(unittest.TestCase):

    def test_timeline_is_sorted_by_timestamp(self):
        events = [
            {
                "event": "Evidence collected",
                "timestamp": "2026-08-24 15:30"
            },
            {
                "event": "Witness statement",
                "timestamp": "2026-08-24 14:00"
            },
            {
                "event": "Case created",
                "timestamp": "2026-08-24 10:00"
            }
        ]

        result = build_timeline(events)

        self.assertEqual(result[0]["event"], "Case created")
        self.assertEqual(result[1]["event"], "Witness statement")
        self.assertEqual(result[2]["event"], "Evidence collected")


if __name__ == "__main__":
    unittest.main()