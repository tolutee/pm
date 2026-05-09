from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from auth import require_auth
from openai_service import simple_math_calculation

router = APIRouter()


@router.get("/__health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@router.get("/api/test")
async def test_api() -> Dict[str, str]:
    return {"message": "API is working!", "status": "success"}


@router.get("/api/test-openai")
async def test_openai(expression: str = "2+2") -> Dict[str, Any]:
    try:
        result = simple_math_calculation(expression)
        return {"expression": expression, "result": result, "status": "success"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API key not configured: {str(e)}",
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}",
        )


@router.get("/api/me")
async def get_me(user: Dict[str, Any] = Depends(require_auth)) -> Dict[str, str]:
    return {"username": user["username"]}
