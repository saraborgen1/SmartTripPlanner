from server.agent import llm_agent

#מגדיר פונקציה שמקבלת מחרוזת שאלה ומחזירה מחרוזת - זוהי פונקציית תיווך בין ה
#API
#לבין מודל הסוכן שלנו
def get_ai_answer(question: str) -> str:
    return llm_agent.ask_ai(question)
