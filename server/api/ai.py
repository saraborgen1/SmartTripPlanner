from fastapi import APIRouter, Query
from ..services.ai_service import get_ai_answer

router = APIRouter()

@router.get("/ai")
def ai_endpoint(question: str = Query(..., description="שאלה לסוכן AI")):
    return {"answer": get_ai_answer(question)}
