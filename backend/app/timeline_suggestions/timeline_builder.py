# backend/app/timeline_suggestions/timeline_builder.py

"""
Orders case events chronologically.

Field names below are confirmed against the REAL schema, not guessed:
  - backend/app/case_management/models.py  (Evidence.collected_at, Evidence.extra_metadata)
  - backend/sample_case.json               (actual stored evidence shape)

Real evidence record shape (as returned by SQLAlchemy / stored in DB):

    {
        "id": "9c4e2b10-...",
        "case_id": "3fa85f64-...",
        "evidence_type": "image",              # Enum: image/video/document/
                                                #       witness_statement/cctv_frame/
                                                #       physical/other
        "description": "Photo of forced cash register",
        "source": "Investigator phone camera",
        "file_url": "https://...",
        "collected_by": "Const. P. Verma",
        "collected_at": "2026-08-24T11:00:00Z",  # <-- the real timestamp field
        "extra_metadata": {
            "yolo_detections": ["crowbar", "cash_register"],   # Anwesha's output, flattened
            "nlp_entities": {"names": [...], "locations": [...], "time_mentions": [...]}  # Anmol's output
        },
        "chain_of_custody": [{"action": "collected", "by": "...", "timestamp": "..."}],
        "created_at": "...",
        "updated_at": null
    }

"""

from app.shared.utils import parse_timestamp, sort_by_timestamp, format_timestamp
from app.shared.exceptions import TimelineBuildError, InsufficientDataError


def _evidence_to_dict(evidence) -> dict:
    """
    Normalizes a SQLAlchemy Evidence ORM object (or a plain dict, e.g. in
    tests) into a plain dict so the rest of this module doesn't care which
    one it received.
    """
    if isinstance(evidence, dict):
        return evidence

    return {
        "id": str(evidence.id),
        "case_id": str(evidence.case_id),
        "evidence_type": evidence.evidence_type.value if hasattr(evidence.evidence_type, "value") else evidence.evidence_type,
        "description": evidence.description,
        "source": evidence.source,
        "collected_by": evidence.collected_by,
        "collected_at": evidence.collected_at.isoformat() if evidence.collected_at else None,
        "extra_metadata": evidence.extra_metadata or {},
    }


def build_timeline(evidence_list: list) -> list[dict]:
    """
    Takes a list of evidence (ORM objects OR plain dicts — e.g. Case.evidence_items
    straight from case_management) and returns them ordered chronologically.

    Evidence with a missing/unparseable collected_at is placed at the end
    rather than raising, since real evidence often has missing timestamps
    (explicitly one of the required "messy case" test scenarios).
    """
    if not evidence_list:
        raise InsufficientDataError("No evidence available to build a timeline.")

    normalized = [_evidence_to_dict(e) for e in evidence_list]
    ordered = sort_by_timestamp(normalized, key="collected_at")

    timeline = []
    for item in ordered:
        ts = parse_timestamp(item.get("collected_at") or "")

        metadata = item.get("extra_metadata", {}) or {}
        detected_objects = metadata.get("yolo_detections", [])
        nlp_entities = metadata.get("nlp_entities", {})

        description = item.get("description")
        if not description and detected_objects:
            description = f"Detected: {', '.join(detected_objects)}"
        elif not description and nlp_entities.get("names"):
            description = f"Statement mentions: {', '.join(nlp_entities['names'])}"
        elif not description:
            description = "Unknown event"

        timeline.append({
            "event": description,
            "timestamp": format_timestamp(ts) if ts else "Unknown time",
            "evidence_id": item.get("id"),
            "evidence_type": item.get("evidence_type", "unknown"),
        })

    return timeline
