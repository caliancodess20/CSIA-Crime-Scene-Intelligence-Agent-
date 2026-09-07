# backend/app/timeline_suggestions/timeline_builder.py

from typing import Any

from app.shared.utils import (
    parse_timestamp,
    sort_by_timestamp,
    format_timestamp,
)
from app.shared.exceptions import (
    TimelineBuildError,
    InsufficientDataError,
)


def normalize_evidence(
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert Case Management evidence into the internal
    structure expected by the Timeline/Suggestion modules.

    Case Management:
        collected_at
        extra_metadata.image_analysis

    Timeline:
        timestamp
        analysis
    """

    if not isinstance(evidence, dict):
        raise TimelineBuildError(
            "Evidence must be a dictionary."
        )

    extra_metadata = (
        evidence.get("extra_metadata") or {}
    )

    if not isinstance(extra_metadata, dict):
        extra_metadata = {}

    image_analysis = (
        extra_metadata.get("image_analysis") or {}
    )

    if not isinstance(image_analysis, dict):
        image_analysis = {}

    normalized = dict(evidence)

    # Case Management → Timeline
    normalized["timestamp"] = (
        evidence.get("collected_at")
        or evidence.get("created_at")
    )

    # Case Management → Image Analysis
    normalized["analysis"] = image_analysis

    return normalized


def normalize_evidence_list(
    evidence_list: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Normalize all Case Management evidence."""

    return [
        normalize_evidence(evidence)
        for evidence in evidence_list
    ]


def build_timeline(
    evidence_list: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Build chronological timeline from Case Management evidence.
    """

    if not evidence_list:
        raise InsufficientDataError(
            "No evidence available to build a timeline."
        )

    normalized = normalize_evidence_list(
        evidence_list
    )

    try:
        ordered = sort_by_timestamp(
            normalized,
            key="timestamp",
        )

    except Exception as exc:
        raise TimelineBuildError(
            f"Unable to sort evidence: {exc}"
        ) from exc

    timeline = []

    for item in ordered:

        timestamp = item.get("timestamp")

        try:
            parsed_timestamp = parse_timestamp(
                str(timestamp or "")
            )
        except Exception:
            parsed_timestamp = None

        # --------------------------------------------
        # Image Analysis
        # --------------------------------------------

        analysis = item.get(
            "analysis"
        ) or {}

        if not isinstance(analysis, dict):
            analysis = {}

        payload = analysis.get(
            "payload"
        ) or {}

        if not isinstance(payload, dict):
            payload = {}

        detected_objects = payload.get(
            "detected_objects"
        ) or []

        if not isinstance(
            detected_objects,
            list,
        ):
            detected_objects = []

        object_names = []

        for obj in detected_objects:

            if not isinstance(obj, dict):
                continue

            class_name = obj.get(
                "class_name"
            )

            if class_name:
                object_names.append(
                    str(class_name)
                )

        # --------------------------------------------
        # Description
        # --------------------------------------------

        description = item.get(
            "description"
        )

        if description:

            description = str(
                description
            )

        elif object_names:

            description = (
                "Detected: "
                + ", ".join(object_names)
            )

        else:

            evidence_type = item.get(
                "evidence_type",
                "evidence",
            )

            description = (
                f"{str(evidence_type).replace('_', ' ').title()} "
                "added to the case"
            )

        # --------------------------------------------
        # Timeline event
        # --------------------------------------------

        timeline.append(
            {
                "event": description,

                "timestamp": (
                    format_timestamp(
                        parsed_timestamp
                    )
                    if parsed_timestamp
                    else "Unknown time"
                ),

                "evidence_id": item.get(
                    "id"
                ),

                "evidence_type": item.get(
                    "evidence_type",
                    "unknown",
                ),

                "case_id": item.get(
                    "case_id"
                ),

                "source": item.get(
                    "source"
                ),

                "file_url": item.get(
                    "file_url"
                ),
            }
        )

    return timeline
