# client/utils/session.py

class SessionManager:
    """
    מחלקה שמנהלת את מצב ההתחברות של המשתמש.
    SessionManager
    שומרת מידע כמו
    user_token
    ו־
    username
    כדי לדעת האם המשתמש מחובר ומה השם שלו.
    """

    def __init__(self):
        # מחרוזת שמייצגת את "אסימון" ההתחברות מהשרת
        # user_token
        self.user_token = None

        # שם המשתמש הנוכחי (לשימוש ב־
        # UI
        # למשל כדי להציג ברכה אישית)
        # username
        self.username = None  

    def is_logged_in(self):
        """
        מחזירה אמת אם המשתמש מחובר כרגע.
        כלומר אם יש ערך ב־
        user_token
        """
        return self.user_token is not None

    def login(self, token, username=None):
        """
        פעולה שמבצעת התחברות.
        מקבלת אסימון
        token
        ושם משתמש
        username
        ושומרת אותם במשתנים של האובייקט.
        """
        self.user_token = token
        self.username = username

    def logout(self):
        """
        פעולה שמבצעת התנתקות.
        מאפסת את הערכים של
        user_token
        ו־
        username
        """
        self.user_token = None
        self.username = None
