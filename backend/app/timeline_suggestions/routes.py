from flask import Blueprint, request, jsonify

from .timeline_builder import build_timeline
from .next_step_rules import suggest_next_steps

timeline_bp = Blueprint(
    "timeline_suggestions",
    __name__,
    url_prefix="/timeline"
)


@timeline_bp.route("/suggestions", methods=["POST"])
def timeline_suggestions():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    events = data.get("events", [])

    if not isinstance(events, list):
        return jsonify({
            "error": "events must be a list"
        }), 400

    timeline = build_timeline(events)

    suggestions = suggest_next_steps(timeline)

    return jsonify({
        "timeline": timeline,
        "next_steps": suggestions
    })