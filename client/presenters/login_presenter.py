# client/presenters/login_presenter.py

from client.services import api_client
import requests


class LoginPresenter:
    """
    מחלקה שאחראית על החיבור בין ה־
    View  
    של מסך ההתחברות / הרשמה  
    לבין הלוגיקה של התקשורת מול השרת  

    ה־
    Presenter  
    הזה מקבל קלט מה־
    View  
    (שם משתמש + סיסמה),  
    שולח בקשות ל־
    API  
    דרך api_client,  
    ומעדכן את ה־
    View  
    בתוצאות (הצלחה או שגיאה).
    """

    def __init__(self, view, session_manager):
        # שמירה של ה־View (כדי להציג הודעות למשתמש)
        self.view = view
        # שמירה של מנהל הסשן (כדי לשמור את מצב ההתחברות של המשתמש)
        self.session = session_manager

    def login(self, username: str, password: str):
        """
        פונקציה שמבצעת התחברות (Login):
        1. שולחת שם משתמש + סיסמה ל־API
        2. בודקת האם התקבל Token
        3. אם כן – שומרת אותו בסשן וממשיכה למסך הראשי
        4. אם לא – מציגה שגיאה ב־View
        """
        try:
            # קריאה ל־API כדי להתחבר
            data = api_client.login(username, password)
            token = data.get("access_token")

            # אם לא התקבל טוקן → נכשל
            if not token:
                self.view.show_error("Login failed: Token not received.")
                return

            # שמירת טוקן ו־username בסשן
            if self.session:
                self.session.login(token, username)

            # עדכון ה־View שההתחברות הצליחה
            self.view.show_success(token)

        except requests.HTTPError as e:
            # טיפול בשגיאות HTTP (למשל 401 – סיסמה שגויה)
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Login failed.")

        except requests.RequestException as e:
            # טיפול בשגיאות רשת כלליות (אין אינטרנט, שרת נפל וכו')
            self.view.show_error(f"Server error: {e}")

    def register(self, username: str, password: str):
        """
        פונקציה שמבצעת הרשמה (Register):
        1. בודקת שכל השדות מולאו
        2. שולחת בקשת הרשמה ל־API
        3. אם הצליח – מנסה להתחבר אוטומטית
        """
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
            # קריאה ל־API כדי לבצע הרשמה
            data = api_client.register(username, password)

            # אחרי הרשמה מוצלחת – מתחברים אוטומטית
            self.login(username, password)

        except requests.HTTPError as e:
            # טיפול בשגיאות מהשרת (למשל "שם משתמש כבר תפוס")
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Registration failed.")

        except requests.RequestException as e:
            # טיפול בשגיאות רשת כלליות
            self.view.show_error(f"Server error: {e}")
