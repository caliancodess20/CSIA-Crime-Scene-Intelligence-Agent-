# backend/app/timeline_suggestions/test_timeline.py

"""
Unit tests for timeline_builder.py.

Replaces the old Flask-era test_timeline.py, which tested a manually
posted {"event": ..., "timestamp": ...} shape against a Flask endpoint.
These test the real function directly against the actual evidence schema
(collected_at, extra_metadata) confirmed from case_management/models.py
and sample_case.json.

Run with:
    pytest backend/app/timeline_suggestions/test_timeline.py -v
"""

import pytest

from app.timeline_suggestions.timeline_builder import build_timeline
from app.shared.exceptions import InsufficientDataError


def make_evidence(evidence_id, collected_at, description=None, evidence_type="image", extra_metadata=None):
    """Small helper to build a plain-dict evidence record for tests."""
    return {
        "id": evidence_id,
        "case_id": "case-1",
        "evidence_type": evidence_type,
        "description": description,
        "collected_at": collected_at,
        "extra_metadata": extra_metadata or {},
    }


class TestBuildTimelineCleanCase:
    """Clean case: all evidence has valid, distinct timestamps."""

    def test_orders_events_chronologically(self):
        evidence = [
            make_evidence("e3", "2026-08-24T15:30:00Z", "Evidence collected"),
            make_evidence("e1", "2026-08-24T10:00:00Z", "Case created"),
            make_evidence("e2", "2026-08-24T14:00:00Z", "Witness statement"),
        ]

        timeline = build_timeline(evidence)

        assert [item["evidence_id"] for item in timeline] == ["e1", "e2", "e3"]
        assert timeline[0]["event"] == "Case created"
        assert timeline[-1]["event"] == "Evidence collected"

    def test_uses_yolo_detections_when_description_missing(self):
        evidence = [
            make_evidence(
                "e1", "2026-08-24T11:00:00Z",
                description=None,
                extra_metadata={"yolo_detections": ["knife", "backpack"]},
            )
        ]

        timeline = build_timeline(evidence)

        assert timeline[0]["event"] == "Detected: knife, backpack"


class TestBuildTimelineMessyCase:
    """Messy case: missing/malformed timestamp — the required 'messy case' scenario."""

    def test_missing_timestamp_goes_last_not_crash(self):
        evidence = [
            make_evidence("e1", "2026-08-24T10:00:00Z", "Case created"),
            make_evidence("e2", None, "Undated evidence"),  # missing timestamp
        ]

        timeline = build_timeline(evidence)

        assert len(timeline) == 2
        assert timeline[-1]["evidence_id"] == "e2"
        assert timeline[-1]["timestamp"] == "Unknown time"

    def test_malformed_timestamp_does_not_crash(self):
        evidence = [
            make_evidence("e1", "not-a-real-date", "Bad timestamp"),
            make_evidence("e2", "2026-08-24T10:00:00Z", "Good timestamp"),
        ]

        timeline = build_timeline(evidence)

        assert len(timeline) == 2
        assert timeline[-1]["evidence_id"] == "e1"  # unparseable pushed to end

    def test_empty_evidence_list_raises(self):
        with pytest.raises(InsufficientDataError):
            build_timeline([])

    def test_falls_back_to_unknown_event_when_no_description_or_detections(self):
        evidence = [make_evidence("e1", "2026-08-24T10:00:00Z", description=None)]

        timeline = build_timeline(evidence)

        assert timeline[0]["event"] == "Unknown event"
