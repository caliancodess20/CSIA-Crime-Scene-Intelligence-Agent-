import uuid
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas


def _generate_case_number(db: Session) -> str:
    year = datetime.now(timezone.utc).year
    count = db.query(models.Case).count() + 1
    return f"CSIA-{year}-{count:05d}"


def create_case(db: Session, case_in: schemas.CaseCreate) -> models.Case:
    case = models.Case(
        case_number=case_in.case_number or _generate_case_number(db),
        title=case_in.title,
        description=case_in.description,
        crime_type=case_in.crime_type,
        status=case_in.status,
        priority=case_in.priority,
        location=case_in.location,
        assigned_investigator=case_in.assigned_investigator,
        tags=case_in.tags or [],
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def get_case(db: Session, case_id: uuid.UUID) -> Optional[models.Case]:
    return db.query(models.Case).filter(models.Case.id == case_id).first()


def get_case_by_number(db: Session, case_number: str) -> Optional[models.Case]:
    return db.query(models.Case).filter(models.Case.case_number == case_number).first()


def list_cases(db: Session, skip: int = 0, limit: int = 20) -> List[models.Case]:
    return (
        db.query(models.Case)
        .order_by(models.Case.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_cases(db: Session) -> int:
    return db.query(models.Case).count()


def update_case(
    db: Session, case: models.Case, updates: schemas.CaseUpdate
) -> models.Case:
    data = updates.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(case, field, value)

    if updates.status == models.CaseStatus.closed and case.closed_at is None:
        case.closed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(case)
    return case


def delete_case(db: Session, case: models.Case) -> None:
    db.delete(case)
    db.commit()


def add_evidence(
    db: Session, case_id: uuid.UUID, evidence_in: schemas.EvidenceCreate
) -> models.Evidence:
    evidence = models.Evidence(
        case_id=case_id,
        evidence_type=evidence_in.evidence_type,
        description=evidence_in.description,
        source=evidence_in.source,
        file_url=evidence_in.file_url,
        collected_by=evidence_in.collected_by,
        collected_at=evidence_in.collected_at,
        extra_metadata=evidence_in.extra_metadata or {},
        chain_of_custody=[
            {
                "action": "collected",
                "by": evidence_in.collected_by,
                "timestamp": (evidence_in.collected_at or datetime.now(timezone.utc)).isoformat(),
            }
        ],
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


def get_evidence(db: Session, evidence_id: uuid.UUID) -> Optional[models.Evidence]:
    return db.query(models.Evidence).filter(models.Evidence.id == evidence_id).first()


def search_cases(
    db: Session,
    query: Optional[str] = None,
    status: Optional[models.CaseStatus] = None,
    crime_type: Optional[str] = None,
    priority: Optional[models.CasePriority] = None,
    assigned_investigator: Optional[str] = None,
    tag: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
):
    q = db.query(models.Case)

    if query:
        like = f"%{query}%"
        q = q.filter(
            or_(
                models.Case.title.ilike(like),
                models.Case.description.ilike(like),
                models.Case.case_number.ilike(like),
                models.Case.location.ilike(like),
            )
        )
    if status:
        q = q.filter(models.Case.status == status)
    if crime_type:
        q = q.filter(models.Case.crime_type.ilike(f"%{crime_type}%"))
    if priority:
        q = q.filter(models.Case.priority == priority)
    if assigned_investigator:
        q = q.filter(models.Case.assigned_investigator.ilike(f"%{assigned_investigator}%"))
    if tag:
        q = q.filter(models.Case.tags.any(tag))

    total = q.count()
    results = q.order_by(models.Case.created_at.desc()).offset(skip).limit(limit).all()
    return results, total


def search_evidence(
    db: Session,
    query: Optional[str] = None,
    evidence_type: Optional[models.EvidenceType] = None,
    case_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 20,
):
    q = db.query(models.Evidence)

    if query:
        like = f"%{query}%"
        q = q.filter(
            or_(
                models.Evidence.description.ilike(like),
                models.Evidence.source.ilike(like),
            )
        )
    if evidence_type:
        q = q.filter(models.Evidence.evidence_type == evidence_type)
    if case_id:
        q = q.filter(models.Evidence.case_id == case_id)

    total = q.count()
    results = q.order_by(models.Evidence.created_at.desc()).offset(skip).limit(limit).all()
    return results, total
