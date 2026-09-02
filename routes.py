from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from .report_builder import build_pdf_report


router = APIRouter(
    prefix="/cases",
    tags=["Report Generator"]
)


@router.get("/{case_id}/report")
def generate_report(case_id: str):

    report_path = build_pdf_report(case_id)

    if report_path is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"{case_id}_report.pdf"
    )