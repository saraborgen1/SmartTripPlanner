# client/presenters/login_presenter.py

from client.services import api_client
import requests

"""
מחלקה שמטפלת בלוגיקה של מסך ההתחברות וההרשמה.היא משמשת כמתווכת בין 
View –
(הממשק הגרפי של המשתמש)
לבין –
api_client 
(הלוגיקה ששולחת בקשות לשרת).
"""
class LoginPresenter:

    def __init__(self, view, session_manager):
          # שמירה של ה־
        # View
        # כדי שנוכל להציג הודעות (שגיאה/הצלחה) למשתמש
        self.view = view
        # שמירה של מנהל הסשן –
        # SessionManager –
        # כדי לעדכן את מצב ההתחברות (מחובר/מנותק)
        self.session = session_manager


    """
        פונקציה שמבצעת התחברות –
        Login –
        1. שולחת שם משתמש וסיסמה לשרת דרך ה־
           API
        2. מקבלת תשובה עם
           Token
        3. אם התקבל
           Token –
           שומרת אותו בסשן
        4. אם נכשל – מציגה שגיאה ב־
           View
    """
    def login(self, username: str, password: str):
      
        try:
            data = api_client.login(username, password)
            token = data.get("access_token")

            # אם לא קיבלנו טוקן → ההתחברות נכשלה
            if not token:
                self.view.show_error("Login failed: Token not received.")
                return

            # שמירת הטוקן ושם המשתמש במנהל הסשן
            if self.session:
                self.session.login(token, username)

            self.view.show_success(token)

        except requests.HTTPError as e:
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Login failed.")

        except requests.RequestException as e:
            # טיפול בשגיאות רשת כלליות (אין אינטרנט, שרת נפל וכו')
            self.view.show_error(f"Server error: {e}")


    """
        פונקציה שמבצעת הרשמה –
        Register –
        1. בודקת שכל השדות מולאו
        2. שולחת בקשת הרשמה לשרת דרך ה־
           API
        3. אם הצליחה – מנסה לבצע התחברות אוטומטית
    """
    def register(self, username: str, password: str):
  
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
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
