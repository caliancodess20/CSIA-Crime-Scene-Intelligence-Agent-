# backend/app/timeline_suggestions/routes.py

from fastapi import (
    APIRouter,
    HTTPException,
)

from .timeline_builder import (
    build_timeline,
)

from app.integration.orchestrator import (
    process_case,
)


router = APIRouter(
    prefix="/timeline",
    tags=["Timeline & Suggestions"],
)


@router.get(
    "/case/{case_id}",
)
async def get_case_timeline(
    case_id: str,
):
    """
    Generate the complete timeline and next-step
    suggestions for a Case Management case.
    """

    if not case_id:
        raise HTTPException(
            status_code=400,
            detail="case_id is required.",
        )

    try:

        result = await process_case(
            case_id
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process case: "
                + str(exc)
            ),
        )
