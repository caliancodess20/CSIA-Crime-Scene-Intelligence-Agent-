from timeline_builder import build_timeline


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

for event in result:
    print(event["timestamp"], "->", event["event"])