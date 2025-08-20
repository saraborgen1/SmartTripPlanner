import requests
from client.services import api_client

class AIChatPresenter:
    """
    Presenter לצ'אט:
    - קורא את הטקסט מה-View
    - שולח לשרת דרך api_client.ask_ai
    - מחזיר תשובה ומעדכן היסטוריה
    """
    def __init__(self, view):
        self.view = view
        # חיבור כפתור השליחה לפונקציה
        self.view.send_btn.clicked.connect(self.on_send)
        # גם Enter ישלח
        self.view.input.returnPressed.connect(self.on_send)

    def on_send(self):
        question = self.view.input.text().strip()
        if not question:
            return

        # הוספת הודעת המשתמש להיסטוריה
        self.view.append_user(question)
        self.view.clear_input()
        self.view.set_enabled(False)

        try:
            answer = api_client.ask_ai(question)
            if not answer:
                answer = "(No answer)"
            self.view.append_assistant(answer)
        except requests.HTTPError as e:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except Exception:
                detail = e.response.text or str(e)
            self.view.append_assistant(f"Error: {detail}")
        except requests.RequestException as e:
            self.view.append_assistant(f"Network error: {e}")
        finally:
            self.view.set_enabled(True)
