"""
shared/exceptions.py

Custom exceptions used across all CSIA modules (case_management,
image_analysis, nlp_engine, evidence_upload, report_generator,
timeline_suggestions).

Instead of every module raising generic Python exceptions or returning
inconsistent error JSON, everyone raises one of these. main.py registers
the handlers below once, and every module gets clean, consistent error
responses for free.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# ---------------------------------------------------------------------------
# Base exception
# ---------------------------------------------------------------------------

class CSIAException(Exception):
    """
    Base class for all custom CSIA errors.

    status_code: HTTP status to return
    message: human-readable explanation shown to the frontend
    """

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# ---------------------------------------------------------------------------
# Case management (Yojit)
# ---------------------------------------------------------------------------

class CaseNotFoundError(CSIAException):
    def __init__(self, case_id: str):
        super().__init__(f"Case '{case_id}' was not found.", status_code=404)


class DuplicateCaseError(CSIAException):
    def __init__(self, case_id: str):
        super().__init__(f"Case '{case_id}' already exists.", status_code=409)


# ---------------------------------------------------------------------------
# Evidence upload (Tanya)
# ---------------------------------------------------------------------------

class EvidenceUploadError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Evidence upload failed: {reason}", status_code=400)


class InvalidFormatError(CSIAException):
    def __init__(self, expected: str, received: str):
        super().__init__(
            f"Invalid file format. Expected {expected}, received {received}.",
            status_code=415,
        )


class EvidenceNotFoundError(CSIAException):
    def __init__(self, evidence_id: str):
        super().__init__(f"Evidence '{evidence_id}' was not found.", status_code=404)


# ---------------------------------------------------------------------------
# Image analysis (Anwesha) — YOLO + OCR
# ---------------------------------------------------------------------------

class ImageProcessingError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Image processing failed: {reason}", status_code=422)


class OCRExtractionError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"OCR text extraction failed: {reason}", status_code=422)


# ---------------------------------------------------------------------------
# NLP engine (Anmol) — summarization + relationship graph
# ---------------------------------------------------------------------------

class NLPProcessingError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"NLP processing failed: {reason}", status_code=422)


class EntityExtractionError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Entity extraction failed: {reason}", status_code=422)


# ---------------------------------------------------------------------------
# Timeline + next-step suggestions (Sanskruti)
# ---------------------------------------------------------------------------

class TimelineBuildError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Timeline could not be built: {reason}", status_code=422)


class InsufficientDataError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Not enough data to proceed: {reason}", status_code=422)


# ---------------------------------------------------------------------------
# Report generator (Tanya)
# ---------------------------------------------------------------------------

class ReportGenerationError(CSIAException):
    def __init__(self, reason: str):
        super().__init__(f"Report generation failed: {reason}", status_code=500)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class AuthenticationError(CSIAException):
    def __init__(self, message: str = "Invalid credentials."):
        super().__init__(message, status_code=401)


class AuthorizationError(CSIAException):
    def __init__(self, message: str = "You do not have permission to do this."):
        super().__init__(message, status_code=403)


# ---------------------------------------------------------------------------
# Handler registration
# ---------------------------------------------------------------------------

def register_exception_handlers(app: FastAPI) -> None:
    """
    Call this once in main.py:

        from shared.exceptions import register_exception_handlers
        app = FastAPI()
        register_exception_handlers(app)

    Every CSIAException raised anywhere in the app (any module, any route)
    will automatically be turned into a clean JSON response instead of a
    raw 500 stack trace.
    """

    @app.exception_handler(CSIAException)
    async def csia_exception_handler(request: Request, exc: CSIAException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.__class__.__name__,
                "message": exc.message,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Catch-all safety net so nothing ever leaks a raw traceback to the
        # frontend. Keep this LAST — FastAPI checks handlers most-specific
        # first, so CSIAException above still takes priority.
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "InternalServerError",
                "message": "Something went wrong. Please try again.",
            },
        )
