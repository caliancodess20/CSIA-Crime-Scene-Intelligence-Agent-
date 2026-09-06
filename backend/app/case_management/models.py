"""
Core case/evidence schema — this is the foundation every other CSIA
module (timeline, NLP, image analysis, reports, dashboard) reads from
and writes to. Coordinate any change here with the rest of the team.
"""

import enum
import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class CaseStatus(str, enum.Enum):
    open = "open"
    under_investigation = "under_investigation"
    closed = "closed"
    archived = "archived"


class CasePriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class EvidenceType(str, enum.Enum):
    image = "image"
    video = "video"
    document = "document"
    witness_statement = "witness_statement"
    cctv_frame = "cctv_frame"
    physical = "physical"
    other = "other"


class Case(Base):
    __tablename__ = "cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    crime_type = Column(String(100), nullable=True, index=True)
    status = Column(Enum(CaseStatus), default=CaseStatus.open, index=True)
    priority = Column(Enum(CasePriority), default=CasePriority.medium, index=True)
    location = Column(String(255), nullable=True)
    assigned_investigator = Column(String(150), nullable=True, index=True)
    tags = Column(ARRAY(String), default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    evidence_items = relationship(
        "Evidence", back_populates="case", cascade="all, delete-orphan"
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False, index=True)

    evidence_type = Column(Enum(EvidenceType), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source = Column(String(255), nullable=True)  # e.g. "Shop CCTV camera 3"
    file_url = Column(String(500), nullable=True)  # link to stored file/image
    collected_by = Column(String(150), nullable=True)
    collected_at = Column(DateTime(timezone=True), nullable=True)

    # Free-form structured output from other modules (YOLOv8 detections,
    # OCR text, NLP entities, etc.) — keeps this schema flexible without
    # requiring a migration every time a new module adds fields.
    extra_metadata = Column(JSON, default=dict)

    chain_of_custody = Column(JSON, default=list)  # list of {by, timestamp, action}

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    case = relationship("Case", back_populates="evidence_items")
