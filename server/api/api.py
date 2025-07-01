# api/ai.py
from fastapi import APIRouter, Query
from ..agent.llm_agent import ask_ai

router = APIRouter()

@router.get("/ask_ai")
def ask_ai_endpoint(question: str = Query(..., description="שאלה על יעד הטיול")):
    answer = ask_ai(question)
    return {"answer": answer}
