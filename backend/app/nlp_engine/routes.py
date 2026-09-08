"""
backend/app/nlp_engine/routes.py
---------------------------------
CSIA — NLP Engine + Relationship Graph track (Anmol Panjwani)

Exposes the entity_extraction logic as API endpoints, versioned the same
way as case_management (/api/v1/...), so Sanskruti can import this router
into app/main.py alongside the other modules' routers.

Expected wiring in app/main.py (for reference — don't add this yourself,
the team lead combines it there):

    from app.nlp_engine.routes import router as nlp_router
    app.include_router(nlp_router, prefix="/api/v1/nlp", tags=["nlp"])
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.nlp_engine.entity_extraction import process_statement

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------
class StatementRequest(BaseModel):
    case_id: str
    statement_text: str


class EntityOut(BaseModel):
    text: str
    label: str
    start: int
    end: int


class GraphNodeOut(BaseModel):
    id: str
    type: str


class GraphEdgeOut(BaseModel):
    source: str
    target: str
    context: str


class RelationshipGraphOut(BaseModel):
    nodes: list[GraphNodeOut]
    edges: list[GraphEdgeOut]


class StatementResponse(BaseModel):
    case_id: str
    summary: list[str]
    entities: list[EntityOut]
    relationship_graph: RelationshipGraphOut


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/extract", response_model=StatementResponse)
def extract_statement(payload: StatementRequest):
    """
    Run entity extraction, summarization, and relationship-graph
    construction on a witness statement.

    Full path once wired into main.py: POST /api/v1/nlp/extract
    """
    if not payload.statement_text.strip():
        raise HTTPException(status_code=400, detail="statement_text cannot be empty")

    result = process_statement(payload.case_id, payload.statement_text)
    return result


@router.get("/health")
def health_check():
    """Full path once wired into main.py: GET /api/v1/nlp/health"""
    return {"status": "ok", "module": "nlp_engine"}
