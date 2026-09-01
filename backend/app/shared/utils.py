"""
shared/utils.py

Small, generic helper functions reused across CSIA modules. Nothing here
should depend on any single module (no imports from case_management,
image_analysis, etc.) — that's what keeps this "shared" instead of
belonging to one person.
"""

import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional


# ---------------------------------------------------------------------------
# IDs
# ---------------------------------------------------------------------------

def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID, optionally prefixed by type.

    generate_id("case")      -> "case_3f9a1c2b"
    generate_id("evidence")  -> "evidence_7d1e44aa"
    generate_id()            -> "9b6f2e11"
    """
    short_uuid = uuid.uuid4().hex[:8]
    return f"{prefix}_{short_uuid}" if prefix else short_uuid


# ---------------------------------------------------------------------------
# Timestamps
# ---------------------------------------------------------------------------

def now_utc() -> datetime:
    """Current UTC time, used whenever a module needs 'now'."""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """
    Format a datetime as ISO 8601, e.g. '2026-08-31T21:52:00Z'.
    This is the standard format all modules should use when sending
    timestamps to the frontend or to each other.
    """
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_timestamp(value: str) -> Optional[datetime]:
    """
    Parse a timestamp string into a datetime object.
    Returns None instead of raising if the format is unrecognized —
    useful because real evidence (per the project brief) often has
    missing or inconsistent timestamps.

    Handles common formats: ISO 8601, 'YYYY-MM-DD HH:MM', 'YYYY-MM-DD'.
    """
    if not value:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def sort_by_timestamp(items: list, key: str = "timestamp", reverse: bool = False) -> list:
    """
    Sort a list of dicts by a timestamp field, pushing items with a
    missing/unparseable timestamp to the end instead of crashing.
    Handy for timeline_suggestions and report_generator.
    """
    def sort_key(item: dict):
        ts = parse_timestamp(item.get(key, ""))
        return (ts is None, ts or datetime.min.replace(tzinfo=timezone.utc))

    return sorted(items, key=sort_key, reverse=reverse)


# ---------------------------------------------------------------------------
# File validation (used by evidence_upload, image_analysis)
# ---------------------------------------------------------------------------

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_TEXT_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}
MAX_FILE_SIZE_MB = 20


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def is_image_file(filename: str) -> bool:
    return get_file_extension(filename) in ALLOWED_IMAGE_EXTENSIONS


def is_text_file(filename: str) -> bool:
    return get_file_extension(filename) in ALLOWED_TEXT_EXTENSIONS


def is_file_size_valid(file_size_bytes: int, max_mb: int = MAX_FILE_SIZE_MB) -> bool:
    return file_size_bytes <= max_mb * 1024 * 1024


# ---------------------------------------------------------------------------
# Text cleanup (used by nlp_engine, ocr_reader)
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Basic whitespace/newline cleanup for OCR output or witness statements
    before they're passed to summarization/entity extraction.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate(text: str, max_length: int = 200) -> str:
    """Shorten text for previews (e.g. case list, search results)."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


# ---------------------------------------------------------------------------
# Standard API response shape
# ---------------------------------------------------------------------------

def success_response(data: Any = None, message: str = "OK") -> dict:
    """
    Standard success envelope so the frontend can rely on one shape
    from every module.

        return success_response(data=case_dict)
    """
    return {"success": True, "message": message, "data": data}


def error_response(message: str, code: Optional[str] = None) -> dict:
    """
    Standard error envelope for cases where you want to return an error
    without raising (most of the time, raise a CSIAException from
    shared/exceptions.py instead — this is here for edge cases).
    """
    return {"success": False, "error": code or "Error", "message": message}
