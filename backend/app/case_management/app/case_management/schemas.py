"""
Pydantic schemas — the JSON contract other modules (dashboard, timeline,
NLP, image analysis) should code against.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field

from .models import CaseStatus, CasePriority, EvidenceType


# ---------- Evidence ----------

class EvidenceBase(BaseModel):
    evidence_type: EvidenceType
    description: Optional[str] = None
    source: Optional[str] = None
    file_url: Optional[str] = None
    collected_by: Optional[str] = None
    collected_at: Optional[datetime] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceUpdate(BaseModel):
    evidence_type: Optional[EvidenceType] = None
    description: Optional[str] = None
    source: Optional[str] = None
    file_url: Optional[str] = None
    collected_by: Optional[str] = None
    collected_at: Optional[datetime] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class EvidenceOut(EvidenceBase):
    id: UUID
    case_id: UUID
    chain_of_custody: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Case ----------

class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    crime_type: Optional[str] = None
    status: CaseStatus = CaseStatus.open
    priority: CasePriority = CasePriority.medium
    location: Optional[str] = None
    assigned_investigator: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class CaseCreate(CaseBase):
    case_number: Optional[str] = None  # auto-generated if omitted


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crime_type: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    location: Optional[str] = None
    assigned_investigator: Optional[str] = None
    tags: Optional[List[str]] = None


class CaseOut(CaseBase):
    id: UUID
    case_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    evidence_items: List[EvidenceOut] = []

    class Config:
        from_attributes = True


class CaseSummaryOut(CaseBase):
    """Lighter payload for list/search results (no nested evidence)."""
    id: UUID
    case_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    evidence_count: int = 0

    class Config:
        from_attributes = True


class PaginatedCases(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[CaseSummaryOut]
