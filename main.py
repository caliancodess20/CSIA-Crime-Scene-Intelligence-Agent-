from fastapi import FastAPI

from backend.app.evidence_upload.routes import router as evidence_router
from backend.app.report_generator.routes import router as report_router


app = FastAPI(title="CSIA Backend")


@app.get("/")
def home():
    return {"message": "CSIA Backend is running!"}


app.include_router(evidence_router)
app.include_router(report_router)