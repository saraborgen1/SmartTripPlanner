#server/database/db_config.py

# הקובץ הזה אחראי על יצירת חיבור למסד הנתונים מסוג
# SQL Server
# שנמצא בענן.
# החיבור מתבצע באמצעות ספריית
# pyodbc
# שמספקת ממשק לעבוד מול מסדי נתונים דרך
# ODBC Driver.
import pyodbc

# פונקציה שמחזירה אובייקט חיבור למסד הנתונים בענן
def get_connection():
    # פרטי החיבור למסד הנתונים
    #כתובת השרת
    #Host
    #שבו נמצא מסד הנתונים
    server = 'SmartTripDB.mssql.somee.com'       
    database = 'SmartTripDB'                     # שם מסד הנתונים
    username = 'borgen_SQLLogin_1'                       # שם המשתמש במסד הנתונים
    password = 'rm5m5752q7'                      # סיסמת המשתמש

    # יצירת מחרוזת החיבור 
    # (Connection String)
    # המחרוזת כוללת את כל הפרטים הנדרשים: דרייבר, שרת, מסד, משתמש וסיסמה
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"  # מציין את הדרייבר הדרוש לחיבור
        f"SERVER={server};"                           # כתובת השרת
        f"DATABASE={database};"                       # שם מסד הנתונים
        f"UID={username};"                            # שם המשתמש
        f"PWD={password};"                            # סיסמה
        f"TrustServerCertificate=yes;"                # מאפשר אמון בתעודת השרת גם אם אינה חתומה
    )

    # מחזירים אובייקט חיבור 
    # (Connection)
    # שניתן להשתמש בו כדי להריץ שאילתות
    # SQL
    # באמצעות פונקציות כמו 
    # cursor()
    return pyodbc.connect(conn_str)
