# server/agent/llm_agent.py
# הקובץ הזה אחראי על תקשורת עם שרת
# Ollama
# מקומי
# באמצעות פרוטוקול
# REST
# 
# המטרה – לשלוח שאלה (טקסט) למודל שפה גדול
# LLM
# שמותקן אצלנו, ולקבל תשובה חכמה בחזרה.

import requests # ספרייה לביצוע בקשות
# HTTP

# כתובת מקומית של השרת –
# Ollama
# מאזינים כברירת מחדל על פורט 11434
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"   # עדיף להשתמש ב־
# 127.0.0.1
# מאשר
# localhost
# כדי למנוע בעיות תקשורת

# שם המודל שבו נשתמש – כאן מדובר במודל
# mistral
# בגירסה
# latest
MODEL_NAME = "mistral:latest"   

# זמן ההמתנה המרבי לבקשה –
# Timeout
# בשניות
DEFAULT_TIMEOUT = 90                                

def ask_ai(question: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    הפונקציה מקבלת שאלה (טקסט) ומשגרת אותה למודל דרך
    Ollama
    הפלט שמוחזר הוא המחרוזת מתוך השדה
    response
    שמגיע מהשרת.
    אם מתרחשת שגיאה – הפונקציה לא תקרוס אלא תחזיר הודעת שגיאה קריאה וברורה.
    """
    try:
        # שליחת בקשת
        # POST
        # לשרת
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,   # שם המודל כפי שהוא מותקן אצלך
                "prompt": question,    # השאלה/טקסט שאנחנו רוצים לשלוח למודל
                "stream": False        # לקבל תשובה בבת אחת (לא סטרימינג)
            },
            timeout=timeout,
        )

        # בדיקה האם התקבלה תשובה תקינה (קוד מצב
        # HTTP
        # תקין = בטווח 200–299).
        # אם לא – תיזרק חריגה עם פרטי התקלה.
        resp.raise_for_status()

        # ניסיון לפענח את גוף התשובה כ־
        # JSON
        # במידה והפענוח נכשל – נעבור לבלוק השגיאות.
        data = resp.json()

        # בשרת
        # Ollama
        # התשובה נשמרת תחת השדה
        # response
        # כאשר
        # stream=False
        return (data.get("response") or "").strip() or "No response received"
    
    except requests.Timeout:
        # במקרה שהמודל לא הספיק לענות במסגרת הזמן שהוגדר –
        # Timeout
        return "Error: Model did not respond in time (Timeout). Please try again or increase the timeout."
    
    except ValueError:
        # השגיאה הזאת מתרחשת אם התשובה שקיבלנו אינה בפורמט
        # JSON
        # תקין
        return f"Error: Invalid response from model: {resp.text[:200]}..."
    
    except requests.RequestException as e:
        # חריגות כלליות אחרות שקשורות לתקשורת
        # HTTP
        # או רשת
        return f"Error communicating with Ollama: {e}"
