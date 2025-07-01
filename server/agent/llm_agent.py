import requests

def ask_ai(question: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": question,
                "stream": False
            },
            timeout=30
        )
        data = response.json()
        return data.get("response", "לא התקבלה תשובה")
    except Exception as e:
        return f"שגיאה בתקשורת עם Ollama: {str(e)}"
