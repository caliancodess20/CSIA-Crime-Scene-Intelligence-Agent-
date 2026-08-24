from timeline_builder import build_timeline
from next_step_rules import suggest_next_steps


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


print("=== INVESTIGATION TIMELINE ===")

for event in timeline:
    print(
        event["timestamp"],
        "->",
        event["event"]
    )


print("\n=== SUGGESTED NEXT STEPS ===")

for suggestion in suggestions:
    print("-", suggestion)
