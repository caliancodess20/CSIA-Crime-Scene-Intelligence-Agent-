# backend/app/timeline_suggestions/timeline_builder.py

"""
Orders case events chronologically.

IMPORTANT — confirmed from Anwesha's image_analysis output (evidence_pipeline.py
/ app.py): her raw response has NO timestamp field. It only returns
detected_objects / extracted_text plus status/filename/device_used.

That means this module can't get timestamps from image_analysis directly.
Timestamps must come from whatever wrapper Evidence Upload (Tanya) attaches
when she stores an evidence record — e.g. an "uploaded_at" or "timestamp"
field alongside Anwesha's payload. This file assumes each evidence record
looks like:

    {
        "id": "evidence_123",
        "case_id": "case_456",
        "evidence_type": "photo",
        "timestamp": "2026-08-31T21:00:00Z",   # <-- from Tanya's wrapper
        "description": "Shop CCTV frame",
        "analysis": { ... Anwesha's raw output above ... }
    }

CONFIRM this shape with Tanya before wiring this up to real data — the
field names here (timestamp, description, evidence_type) are our best
guess until format_spec.py is shared.
"""

from app.shared.utils import parse_timestamp, sort_by_timestamp, format_timestamp
from app.shared.exceptions import TimelineBuildError, InsufficientDataError


def build_timeline(evidence_list: list[dict]) -> list[dict]:
    """
    Takes a list of evidence records (from Case Management, each one
    already wrapped with a timestamp by Evidence Upload) and returns
    them ordered chronologically.
    """
    if not evidence_list:
        raise InsufficientDataError("No evidence available to build a timeline.")

    ordered = sort_by_timestamp(evidence_list, key="timestamp")

    timeline = []
    for item in ordered:
        ts = parse_timestamp(item.get("timestamp", ""))

        # Pull a human-readable summary from Anwesha's analysis output,
        # if present, so the timeline entry says something useful even
        # without a manually written description.
        analysis = item.get("analysis", {})
        detected = analysis.get("payload", {}).get("detected_objects", [])
        object_names = [obj.get("class_name") for obj in detected if obj.get("class_name")]

        description = item.get("description")
        if not description and object_names:
            description = f"Detected: {', '.join(object_names)}"
        elif not description:
            description = "Unknown event"

        timeline.append({
            "event": description,
            "timestamp": format_timestamp(ts) if ts else "Unknown time",
            "evidence_id": item.get("id"),
            "evidence_type": item.get("evidence_type", "unknown"),
        })

    return timeline
