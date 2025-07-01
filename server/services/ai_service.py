from server.agent import llm_agent

def get_ai_answer(question: str) -> str:
    return llm_agent.ask_ai(question)
