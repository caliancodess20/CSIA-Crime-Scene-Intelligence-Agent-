from next_step_rules import suggest_next_steps


timeline = [
    {
        "event": "Case created",
        "timestamp": "2026-08-24 10:00"
    },
    {
        "event": "Witness statement",
        "timestamp": "2026-08-24 14:00"
    }
]


suggestions = suggest_next_steps(timeline)

print("Suggested Next Steps:")

for suggestion in suggestions:
    print("-", suggestion)
