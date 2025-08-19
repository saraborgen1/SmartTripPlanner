from fastapi import HTTPException
from server.models.user import User
from server.database import db_config

# פונקציה לרישום משתמש חדש למסד הנתונים
def register_user(user: User):
    conn = db_config.get_connection()       # יצירת חיבור למסד הנתונים
    cursor = conn.cursor()                  # יצירת סמן (cursor) לביצוע שאילתות

    # בדיקה אם המשתמש כבר קיים בטבלה
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():                   # אם נמצאה תוצאה – המשתמש כבר קיים
        raise HTTPException(status_code=400, detail="Username already exists")

    # הוספת המשתמש החדש לטבלה
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
         (user.username, user.password)
    )
    conn.commit()                           # שמירה של השינויים במסד הנתונים
    return {"message": "User registered successfully"}

# פונקציה להתחברות משתמש קיים
def login_user(user: User):
    conn = db_config.get_connection()       # יצירת חיבור למסד הנתונים
    cursor = conn.cursor()

    # בדיקת קיום משתמש עם שם וסיסמה תואמים
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (user.username, user.password)
    )
    if cursor.fetchone():                   # אם נמצא משתמש – החיבור הצליח
        return {"access_token": f"token_for_{user.username}"}

    # אחרת – שם משתמש או סיסמה שגויים
    raise HTTPException(status_code=401, detail="Invalid username or password")
