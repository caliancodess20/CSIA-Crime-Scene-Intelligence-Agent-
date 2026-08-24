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
                parsed_timestamp = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M"
                )
            except ValueError:
                parsed_timestamp = None
        else:
            parsed_timestamp = None

        timeline.append((event_copy, parsed_timestamp))

    timeline.sort(
        key=lambda item: (
            item[1] is None,
            item[1] if item[1] else datetime.max
        )
    )

    return [event for event, _ in timeline]