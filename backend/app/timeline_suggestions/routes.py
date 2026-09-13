# backend/app/timeline_suggestions/routes.py

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.case_management.database import get_db
from app.case_management import crud
from app.shared.auth import get_current_user
from app.shared.exceptions import CaseNotFoundError, InsufficientDataError

from .timeline_builder import build_timeline
from .next_step_rules import generate_suggestions

router = APIRouter(prefix="/cases/{case_id}", tags=["timeline_suggestions"])


def _get_case_or_404(db: Session, case_id: str):
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise CaseNotFoundError(case_id)

    case = crud.get_case(db, case_uuid)
    if case is None:
        raise CaseNotFoundError(case_id)
    return case


@router.get("/timeline")
def get_case_timeline(
    case_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Returns the case's evidence ordered chronologically by collected_at.

    GET /cases/{case_id}/timeline
    """
    case = _get_case_or_404(db, case_id)

    if not case.evidence_items:
        raise InsufficientDataError(f"Case {case_id} has no evidence yet — nothing to build a timeline from.")

    timeline = build_timeline(case.evidence_items)
    return {"success": True, "case_id": case_id, "timeline": timeline}


@router.get("/next-steps")
def get_case_next_steps(
    case_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Returns rule-based next-step suggestions for the case, based on what's
    been detected/extracted in its evidence so far.

    GET /cases/{case_id}/next-steps
    """
    case = _get_case_or_404(db, case_id)

    if not case.evidence_items:
        raise InsufficientDataError(f"Case {case_id} has no evidence yet — nothing to base suggestions on.")

    suggestions = generate_suggestions(case.evidence_items)
    return {"success": True, "case_id": case_id, "next_steps": suggestions}


@router.get("/timeline-and-next-steps")
def get_timeline_and_next_steps(
    case_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Convenience endpoint returning both together — useful for the
    frontend's Timeline component to fetch in a single request.

    GET /cases/{case_id}/timeline-and-next-steps
    """
    case = _get_case_or_404(db, case_id)

    if not case.evidence_items:
        raise InsufficientDataError(f"Case {case_id} has no evidence yet.")

    return {
        "success": True,
        "case_id": case_id,
        "timeline": build_timeline(case.evidence_items),
        "next_steps": generate_suggestions(case.evidence_items),
    }
        
