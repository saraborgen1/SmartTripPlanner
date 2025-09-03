# client/utils/session.py

# הקובץ הזה מגדיר מחלקה לניהול מצב ההתחברות של המשתמש בצד ה־
# Client.
# SessionManager
# שומר מידע כמו
# user_token
# (אסימון ההתחברות מהשרת)
# ו־
# username
# (שם המשתמש הנוכחי),
# כדי לאפשר לשאר חלקי האפליקציה לדעת אם המשתמש מחובר ומה שמו.

class SessionManager:


    def __init__(self):
        # מחרוזת שמייצגת את "אסימון" ההתחברות מהשרת
        # user_token
        self.user_token = None

        # שם המשתמש הנוכחי
        # username
        # למשל להצגה ב־
        # UI
        # (כדי להציג הודעת ברוך הבא מותאמת אישית)
        self.username = None  

    def is_logged_in(self):
        """
        פונקציה שבודקת האם המשתמש מחובר כרגע.
        היא מחזירה אמת 
        (True)
        אם יש ערך ב־
        user_token,
        ושקר 
        (False)
        אם אין.
        """
        return self.user_token is not None

    def login(self, token, username=None):
        """
        פונקציה שמבצעת התחברות.
        מקבלת אסימון –
        token –
        ושם משתמש –
        username –
        ושומרת אותם בתוך משתני האובייקט.
        """
        self.user_token = token
        self.username = username

    def logout(self):
        """
        פונקציה שמבצעת התנתקות.
        מאפסת את הערכים של:
        user_token
        ו־
        username
        כך שהמערכת תחזור למצב של "לא מחובר".
        """
        self.user_token = None
        self.username = None
