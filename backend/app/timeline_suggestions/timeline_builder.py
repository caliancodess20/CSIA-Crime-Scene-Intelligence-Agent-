from datetime import datetime


def build_timeline(events):
    if not events:
        return []

    timeline = []

    for event in events:
        event_copy = event.copy()

        timestamp = event_copy.get("timestamp")

        if timestamp:
            try:
                event_copy["_parsed_timestamp"] = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M"
                )
            except ValueError:
                event_copy["_parsed_timestamp"] = None
        else:
            event_copy["_parsed_timestamp"] = None

        timeline.append(event_copy)

    timeline.sort(
        key=lambda event: (
            event["_parsed_timestamp"] is None,
            event["_parsed_timestamp"]
            if event["_parsed_timestamp"]
            else datetime.max
        )
    )

    return timeline