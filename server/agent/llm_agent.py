# server/agent/llm_agent.py
# -------------------------
# תקשורת עם Ollama מקומית דרך REST

import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"  # עדיף 127.0.0.1 מאשר localhost
MODEL_NAME = "mistral:latest"                        # השתמש בתג שמופיע ב-/api/tags
DEFAULT_TIMEOUT = 90                                 # העלאת timeout (מודלים לפעמים איטיים)

def ask_ai(question: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    שולח שאלה למודל דרך Ollama ומחזיר את המחרוזת 'response'.
    במקרה של שגיאה מחזיר טקסט שגיאה ברור.
    """
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,   # שם המודל כפי שהוא מותקן אצלך
                "prompt": question,    # הטקסט/שאלה למודל
                "stream": False        # לקבל תשובה בבת אחת (לא סטרימינג)
            },
            timeout=timeout,
        )
        # אם השרת החזיר קוד שאינו 2xx – נזרוק חריגה עם פרטים
        resp.raise_for_status()

        # ניסיון לפענח JSON; אם לא תקין – ניפול ל־except
        data = resp.json()

        # Ollama מחזיר שדה 'response' כשstream=False
        return (data.get("response") or "").strip() or "לא התקבלה תשובה"
    
    except requests.Timeout:
        return "שגיאה: המודל לא השיב בזמן (Timeout). נסי שוב או הגדילי את ה-Timeout."
    except ValueError:
        # קורה אם הגוף לא JSON תקין
        return f"שגיאה: תשובה לא תקינה מהמודל: {resp.text[:200]}..."
    except requests.RequestException as e:
        # שגיאות רשת/HTTP אחרות
        return f"שגיאה בתקשורת עם Ollama: {e}"
