import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db

router = APIRouter(prefix="/api/v1", tags=["Case Management"])


# ---------------------------------------------------------------------------
# CASE CRUD
# ---------------------------------------------------------------------------

@router.post("/cases", response_model=schemas.CaseOut, status_code=201)
def create_case(case_in: schemas.CaseCreate, db: Session = Depends(get_db)):
    """Create a new case."""
    return crud.create_case(db, case_in)


@router.get("/cases", response_model=schemas.PaginatedCases)
def list_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all cases, paginated."""
    skip = (page - 1) * page_size
    cases = crud.list_cases(db, skip=skip, limit=page_size)
    total = crud.count_cases(db)
    results = [
        schemas.CaseSummaryOut(
            **schemas.CaseOut.from_orm(c).dict(exclude={"evidence_items"}),
            evidence_count=len(c.evidence_items),
        )
        for c in cases
    ]
    return schemas.PaginatedCases(total=total, page=page, page_size=page_size, results=results)


@router.get("/cases/{case_id}", response_model=schemas.CaseOut)
def get_case(case_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve a single case with its evidence."""
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/cases/{case_id}", response_model=schemas.CaseOut)
def update_case(case_id: uuid.UUID, updates: schemas.CaseUpdate, db: Session = Depends(get_db)):
    """Update fields on an existing case (partial update)."""
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return crud.update_case(db, case, updates)


@router.delete("/cases/{case_id}", status_code=204)
def delete_case(case_id: uuid.UUID, db: Session = Depends(get_db)):
    """Delete a case and its associated evidence."""
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    crud.delete_case(db, case)
    return None


# ---------------------------------------------------------------------------
# EVIDENCE
# ---------------------------------------------------------------------------

@router.post("/cases/{case_id}/evidence", response_model=schemas.EvidenceOut, status_code=201)
def add_evidence(case_id: uuid.UUID, evidence_in: schemas.EvidenceCreate, db: Session = Depends(get_db)):
    """Attach a new piece of evidence to a case."""
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return crud.add_evidence(db, case_id, evidence_in)


@router.get("/evidence/{evidence_id}", response_model=schemas.EvidenceOut)
def get_evidence(evidence_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve a single evidence item."""
    evidence = crud.get_evidence(db, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


# ---------------------------------------------------------------------------
# SEARCH & FILTER
# ---------------------------------------------------------------------------

@router.get("/search/cases", response_model=schemas.PaginatedCases)
def search_cases(
    q: Optional[str] = Query(None, description="Free-text search across title/description/case_number/location"),
    status: Optional[models.CaseStatus] = None,
    crime_type: Optional[str] = None,
    priority: Optional[models.CasePriority] = None,
    assigned_investigator: Optional[str] = None,
    tag: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search and filter cases by any combination of criteria."""
    skip = (page - 1) * page_size
    cases, total = crud.search_cases(
        db,
        query=q,
        status=status,
        crime_type=crime_type,
        priority=priority,
        assigned_investigator=assigned_investigator,
        tag=tag,
        skip=skip,
        limit=page_size,
    )
    results = [
        schemas.CaseSummaryOut(
            **schemas.CaseOut.from_orm(c).dict(exclude={"evidence_items"}),
            evidence_count=len(c.evidence_items),
        )
        for c in cases
    ]
    return schemas.PaginatedCases(total=total, page=page, page_size=page_size, results=results)


@router.get("/search/evidence")
def search_evidence(
    q: Optional[str] = Query(None, description="Free-text search across description/source"),
    evidence_type: Optional[models.EvidenceType] = None,
    case_id: Optional[uuid.UUID] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search and filter evidence across all cases (or within one case)."""
    skip = (page - 1) * page_size
    items, total = crud.search_evidence(
        db, query=q, evidence_type=evidence_type, case_id=case_id, skip=skip, limit=page_size
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": [schemas.EvidenceOut.from_orm(e) for e in items],
    }
