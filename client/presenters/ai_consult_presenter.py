# client/presenters/ai_consult_presenter.py

import requests
from client.services import api_client


class AIChatPresenter:
    """
    מחלקה שאחראית על החיבור בין ה־
    View  
    (הממשק הגרפי)

    לבין השירות  
    api_client  

    ששולח שאלה אל ה־
    AI  
    ומחזיר תשובה.
    """

    def __init__(self, view):
        # שמירה של ה־
        # View  
        # כדי שנוכל לגשת לשדות ולכפתורים שבו
        self.view = view

        # חיבור הכפתור "Send" מה־
        # View  
        # אל הפונקציה  
        # on_send
        self.view.send_btn.clicked.connect(self.on_send)

        # גם אם המשתמש ילחץ על מקש  
        # Enter  
        # בתוך שדה הקלט — זה ישלח
        self.view.input.returnPressed.connect(self.on_send)

    def on_send(self):
        """
        פונקציה שנקראת כאשר המשתמש לוחץ על כפתור "שלח"
        או מקיש על מקש  
        Enter.
        """

        # לוקח את הטקסט משדה הקלט  
        # input  
        # ומוריד רווחים מיותרים
        question = self.view.input.text().strip()

        # אם אין טקסט (שורה ריקה) — לא נשלח כלום
        if not question:
            return

        # מוסיף את ההודעה של המשתמש להיסטוריה של הצ'אט ב־
        # View
        self.view.append_user(question)

        # מנקה את שדה הקלט ב־
        # View
        self.view.clear_input()

        # מבטל זמנית את האפשרות ללחוץ כפתורים או לכתוב שוב ב־
        # View  
        # עד שתקבל תשובה
        self.view.set_enabled(False)

        try:
            # שולח את השאלה לשרת דרך  
            # api_client.ask_ai  
            # ומקבל תשובה
            answer = api_client.ask_ai(question)

            # אם לא התקבלה תשובה — מציג הודעה ריקה
            if not answer:
                answer = "(No answer)"

            # מוסיף את התשובה של ה־
            # AI  
            # להיסטוריית השיחה
            self.view.append_assistant(answer)

        except requests.HTTPError as e:
            # אם השרת החזיר שגיאת  
            # HTTP  
            # ננסה לקרוא את הפירוט
            try:
                detail = e.response.json().get("detail", e.response.text)
            except Exception:
                detail = e.response.text or str(e)

            # מציג את השגיאה בצ'אט (מהצד של ה־
            # AI)
            self.view.append_assistant(f"Error: {detail}")

        except requests.RequestException as e:
            # אם יש שגיאת רשת (אין אינטרנט וכו')
            self.view.append_assistant(f"Network error: {e}")

        finally:
            # מפעיל מחדש את ה־
            # View  
            # (מאפשר למשתמש לשלוח שוב הודעות)
            self.view.set_enabled(True)
