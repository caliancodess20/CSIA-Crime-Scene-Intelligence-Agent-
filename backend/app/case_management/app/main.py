"""
Entry point for the Case Management + Search module.

Run with:
    uvicorn app.main:app --reload --port 8000

Once other modules' routers exist (evidence upload, image analysis, NLP,
timeline, reports), they get included here the same way case_management
is, so the whole backend is served from one FastAPI app.
"""

from fastapi import FastAPI

from .case_management.database import Base, engine
from .case_management.routes import router as case_management_router

# Creates tables if they don't exist yet. In a real deployment this would
# be replaced by Alembic migrations so schema changes are tracked.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CSIA API",
    description="Crime Scene Intelligence Assistant — Case Management & Search",
    version="0.1.0",
)

app.include_router(case_management_router)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
