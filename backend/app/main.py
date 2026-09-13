"""
Entry point for the Case Management + Search module.

Run with:
    uvicorn app.main:app --reload --port 8000

Once other modules' routers exist (evidence upload, image analysis, NLP,
timeline, reports), they get included in main.py the same way.
"""

from fastapi import FastAPI

from .case_management.database import Base, engine
from .case_management.routes import router as case_management_router
from .timeline_suggestions.routes import router as timeline_router
from .shared.exceptions import register_exception_handlers


app = FastAPI(
    title="CSIA API",
    description="Crime Scene Intelligence Assistant — Case Management & Search",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(case_management_router)
app.include_router(timeline_router)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}