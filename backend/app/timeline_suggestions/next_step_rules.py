# backend/app/timeline_suggestions/next_step_rules.py

"""
Rule-based next-step suggestion engine — deliberately NOT machine learning,
per the project brief ("rule-based only").

Consumes the structured output shape produced by Anwesha's
image_analysis pipeline (evidence_pipeline.py / app.py):

    {
        "status": "success",
        "device_used": "cpu",
        "filename": "test.jpg",
        "payload": {
            "detected_objects": [
                {"class_name": "knife", "confidence": 0.87, "bounding_box": [...]}
            ],
            "extracted_text": [
                {"text": "SHARMA STORE", "confidence": 0.94, "bounding_box": [...]}
            ]
        }
    }

and a list of evidence_type strings already present on the case (e.g.
from Case Management), to decide what to recommend next.
"""

from app.shared.exceptions import InsufficientDataError


# ---------------------------------------------------------------------------
# Rule table — object class (from YOLO) -> suggestion
# ---------------------------------------------------------------------------
# NOTE: yolov8n.pt is trained on the COCO dataset (80 classes). COCO does NOT
# include "knife" or "weapon" as a class — closest real COCO labels are
# things like "knife" is actually NOT in COCO80, but common near-matches are
# "scissors", "baseball bat", "backpack", "handbag", "cell phone", "bottle".
# Confirm with Anwesha whether she's using a custom-trained/fine-tuned model
# for weapon detection, or stock yolov8n — the rules below are written to be
# easy to extend either way.

OBJECT_SUGGESTION_RULES = {
    "knife": "A knife was detected in the evidence. Suggest documenting it as physical evidence and checking for nearby CCTV coverage.",
    "scissors": "A sharp object (scissors) was detected. Flag for manual review — verify if relevant to the case.",
    "baseball bat": "A blunt object was detected. Flag for manual review as a potential weapon.",
    "backpack": "A bag was detected in the frame. Suggest checking if it was recovered or left at the scene.",
    "handbag": "A bag was detected in the frame. Suggest checking if it was recovered or left at the scene.",
    "cell phone": "A phone was detected. Suggest checking if it belongs to a witness or suspect — could hold call/location records.",
    "car": "A vehicle was detected. Suggest cross-checking against any nearby CCTV or ANPR (license plate) footage.",
    "person": "A person was detected in the frame. Suggest comparing against witness descriptions for identification.",
}

# Evidence-type gap rules — "if X was detected but Y evidence type doesn't
# exist yet for this case, suggest collecting Y."
EVIDENCE_GAP_RULES = [
    {
        "trigger_objects": {"knife", "scissors", "baseball bat"},
        "missing_evidence_type": "cctv_footage",
        "suggestion": "A potential weapon was detected but no CCTV footage has been uploaded for this case yet. Suggest checking nearby CCTV.",
    },
    {
        "trigger_objects": {"person"},
        "missing_evidence_type": "witness_statement",
        "suggestion": "A person was detected in image evidence but no witness statement exists yet. Suggest following up for a statement.",
    },
]


def generate_suggestions(image_analysis_output: dict, existing_evidence_types: list[str] | None = None) -> list[str]:
    """
    Takes the raw output dict from image_analysis (Anwesha's module) plus
    a list of evidence types already on the case, and returns a list of
    plain-language next-step suggestions.

    existing_evidence_types example: ["photo", "witness_statement"]
    """
    if not image_analysis_output:
        raise InsufficientDataError("No image analysis output provided to generate suggestions.")

    payload = image_analysis_output.get("payload", {})
    detected_objects = payload.get("detected_objects", [])
    existing_evidence_types = set(existing_evidence_types or [])

    detected_classes = {obj["class_name"] for obj in detected_objects if "class_name" in obj}

    suggestions: list[str] = []

    # Direct object -> suggestion rules
    for class_name in detected_classes:
        if class_name in OBJECT_SUGGESTION_RULES:
            suggestions.append(OBJECT_SUGGESTION_RULES[class_name])

    # Evidence-gap rules (needs case context, not just this one image)
    for rule in EVIDENCE_GAP_RULES:
        objects_present = rule["trigger_objects"] & detected_classes
        evidence_missing = rule["missing_evidence_type"] not in existing_evidence_types
        if objects_present and evidence_missing:
            suggestions.append(rule["suggestion"])

    if not suggestions:
        suggestions.append("No specific next steps triggered by this evidence. Manual review recommended.")

    return suggestions
          
