# backend/app/timeline_suggestions/test_next_steps.py

"""
Unit tests for next_step_rules.py.

Replaces the old Flask-era test_next_steps.py (which tested static rules
like "Case Created -> collect evidence"). The real engine now reacts to
Anwesha's actual 2-class model output (knife/backpack) stored in
Evidence.extra_metadata.yolo_detections, confirmed via dataset.yaml and
sample_case.json.

Run with:
    pytest backend/app/timeline_suggestions/test_next_steps.py -v
"""

import pytest

from app.timeline_suggestions.next_step_rules import generate_suggestions
from app.shared.exceptions import InsufficientDataError


def make_evidence(evidence_type="image", yolo_detections=None, nlp_entities=None):
    return {
        "evidence_type": evidence_type,
        "extra_metadata": {
            "yolo_detections": yolo_detections or [],
            "nlp_entities": nlp_entities or {},
        },
    }


class TestEvidenceBasedSuggestions:
    """Suggestions triggered by detected objects (knife/backpack)."""

    def test_knife_detected_suggests_documentation(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["knife"])]

        suggestions = generate_suggestions(evidence)

        assert any("knife" in s.lower() for s in suggestions)

    def test_backpack_detected_suggests_recovery_check(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["backpack"])]

        suggestions = generate_suggestions(evidence)

        assert any("bag" in s.lower() for s in suggestions)

    def test_knife_without_cctv_suggests_checking_cctv(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["knife"])]

        suggestions = generate_suggestions(evidence, existing_evidence_types=["image"])

        assert any("cctv" in s.lower() for s in suggestions)

    def test_knife_with_cctv_already_present_does_not_repeat_suggestion(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["knife"])]

        suggestions = generate_suggestions(evidence, existing_evidence_types=["image", "cctv_frame"])

        assert not any("cctv" in s.lower() for s in suggestions)


class TestWitnessBasedSuggestions:
    """Suggestions triggered by presence/absence of witness_statement evidence."""

    def test_physical_evidence_without_witness_statement_suggests_followup(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["backpack"])]

        suggestions = generate_suggestions(evidence, existing_evidence_types=["image"])

        assert any("witness" in s.lower() for s in suggestions)

    def test_physical_evidence_with_witness_statement_present_no_followup(self):
        evidence = [make_evidence(evidence_type="image", yolo_detections=["backpack"])]

        suggestions = generate_suggestions(evidence, existing_evidence_types=["image", "witness_statement"])

        assert not any("witness" in s.lower() for s in suggestions)


class TestFullFlow:
    """Combined scenarios and edge cases."""

    def test_no_objects_detected_returns_generic_fallback(self):
        evidence = [make_evidence(evidence_type="witness_statement", yolo_detections=[])]

        suggestions = generate_suggestions(evidence)

        assert suggestions == ["No specific next steps triggered by this evidence. Manual review recommended."]

    def test_empty_evidence_list_raises(self):
        with pytest.raises(InsufficientDataError):
            generate_suggestions([])

    def test_multiple_evidence_items_combine_detections(self):
        evidence = [
            make_evidence(evidence_type="image", yolo_detections=["knife"]),
            make_evidence(evidence_type="witness_statement"),
        ]

        suggestions = generate_suggestions(evidence)

        # witness_statement already present, so witness-followup rule should NOT fire
        assert not any("witness" in s.lower() for s in suggestions)
        assert any("knife" in s.lower() for s in suggestions)
