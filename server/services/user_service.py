# server/services/user_service.py

# הקובץ הזה מגדיר את שכבת השירות 
# (Service Layer)
# שאחראית על פעולות ניהול משתמשים במערכת:
# רישום משתמש חדש והתחברות משתמש קיים.
#
# השכבה הזו נמצאת בין שכבת ה־
# API
# לבין מסד הנתונים,
# ומבצעת את הלוגיקה בפועל.
from fastapi import HTTPException
from server.models.user import User
from server.database import db_config

# פונקציה לרישום משתמש חדש למסד הנתונים
def register_user(user: User):
    # יצירת חיבור למסד הנתונים
    conn = db_config.get_connection() 

    # יצירת סמן
    # cursor
    # לביצוע שאילתות
    cursor = conn.cursor()       

    # בדיקה אם המשתמש כבר קיים בטבלה
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():                  
         # אם נמצאה תוצאה – המשתמש כבר קיים
        # נזרקת חריגת
        # HTTPException
        # עם קוד סטטוס 400
        raise HTTPException(status_code=400, detail="Username already exists")

    # הוספת המשתמש החדש לטבלה
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
         (user.username, user.password)
    )
    # שמירת השינויים במסד הנתונים
    conn.commit()        
    # החזרת הודעת הצלחה              
    return {"message": "User registered successfully"}


# פונקציה להתחברות משתמש קיים
def login_user(user: User):
    # יצירת חיבור למסד הנתונים
    conn = db_config.get_connection() 
    # יצירת סמן
     # cursor
     # לביצוע שאילתות     
    cursor = conn.cursor()

    # בדיקת קיום משתמש עם שם וסיסמה תואמים
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (user.username, user.password)
    )
    if cursor.fetchone():
        # אם נמצא משתמש – ההתחברות הצליחה
        # מחזירים טוקן גישה פשוט 
        # (access_token)                   
        return {"access_token": f"token_for_{user.username}"}
    # אחרת – שם המשתמש או הסיסמה שגויים
    # נזרקת חריגת
    # HTTPException
    # עם קוד סטטוס 401
    raise HTTPException(status_code=401, detail="Invalid username or password")
