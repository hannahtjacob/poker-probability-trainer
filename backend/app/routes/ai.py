from fastapi import APIRouter, HTTPException

from poker import ai_explainer


router = APIRouter()


@router.post("/explain")
def explain(analysis: dict):
    try:
        return ai_explainer.explain_analysis_with_ai(analysis)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI explanation is currently unavailable: {error}",
        ) from error
