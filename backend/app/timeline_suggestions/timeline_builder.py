# backend/app/timeline_suggestions/timeline_builder.py

"""
Timeline builder.

Canonical input:
    Case Management evidence records.

Case Management fields:
    id
    case_id
    evidence_type
    description
    source
    file_url
    collected_at
    extra_metadata

For compatibility with the existing timeline engine we normalize:
    collected_at -> timestamp
    extra_metadata.image_analysis -> analysis
"""

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


def normalize_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    """
    Convert one Case Management EvidenceOut record into the
    internal format expected by the timeline/suggestion modules.
    """

    if not isinstance(evidence, dict):
        raise TimelineBuildError("Evidence record must be a dictionary.")

    extra_metadata = evidence.get("extra_metadata") or {}

    if not isinstance(extra_metadata, dict):
        extra_metadata = {}

    image_analysis = extra_metadata.get("image_analysis") or {}

    # Preserve the complete Case Management record while adding
    # compatibility aliases used by the timeline engine.
    normalized = dict(evidence)

    normalized["timestamp"] = (
        evidence.get("collected_at")
        or evidence.get("created_at")
    )

    normalized["analysis"] = image_analysis

    return normalized


def normalize_evidence_list(
    evidence_list: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Normalize all Case Management evidence records."""

    return [
        normalize_evidence(evidence)
        for evidence in evidence_list
    ]


def build_timeline(
    evidence_list: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Build a chronological timeline from Case Management evidence.

    Case Management is the source of truth for timestamps and evidence IDs.
    """

    if not evidence_list:
        raise InsufficientDataError(
            "No evidence available to build a timeline."
        )

    normalized = normalize_evidence_list(evidence_list)

    # Keep records even when timestamp is missing.
    # sort_by_timestamp handles the timestamp ordering used by
    # the existing shared utilities.
    try:
        ordered = sort_by_timestamp(
            normalized,
            key="timestamp",
        )
    except Exception as exc:
        raise TimelineBuildError(
            f"Unable to sort evidence by timestamp: {exc}"
        ) from exc

    timeline: list[dict[str, Any]] = []

    for item in ordered:

        raw_timestamp = item.get("timestamp")

        try:
            ts = parse_timestamp(str(raw_timestamp or ""))
        except Exception:
            ts = None

        # -----------------------------------------
        # Extract Image Analysis information
        # -----------------------------------------

        analysis = item.get("analysis") or {}

        if not isinstance(analysis, dict):
            analysis = {}

        payload = analysis.get("payload") or {}

        if not isinstance(payload, dict):
            payload = {}

        detected = payload.get("detected_objects") or []

        if not isinstance(detected, list):
            detected = []

        object_names = []

        for obj in detected:
            if isinstance(obj, dict):
                class_name = obj.get("class_name")

                if class_name:
                    object_names.append(str(class_name))

        # -----------------------------------------
        # Generate human-readable event description
        # -----------------------------------------

        description = item.get("description")

        if description:
            description = str(description)

        elif object_names:
            description = (
                "Image analysis detected: "
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

        # -----------------------------------------
        # Timeline output
        # -----------------------------------------

        timeline.append(
            {
                "event": description,

                "timestamp": (
                    format_timestamp(ts)
                    if ts
                    else "Unknown time"
                ),

                "evidence_id": str(
                    item.get("id")
                ) if item.get("id") else None,

                "evidence_type": str(
                    item.get("evidence_type", "unknown")
                ),

                "case_id": str(
                    item.get("case_id")
                ) if item.get("case_id") else None,

                "source": item.get("source"),

                "file_url": item.get("file_url"),
            }
        )

    return timeline
