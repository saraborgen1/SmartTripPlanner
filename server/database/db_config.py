# מייבא את הספרייה pyodbc שמאפשרת להתחבר למסד נתונים מסוג SQL Server
import pyodbc

# פונקציה שמחזירה אובייקט חיבור למסד הנתונים בענן
def get_connection():
    # פרטי החיבור למסד הנתונים
    server = 'SmartTripDB.mssql.somee.com'       # כתובת השרת (host) שבו נמצא מסד הנתונים
    database = 'SmartTripDB'                     # שם מסד הנתונים
    # username = 'tripuser1'                       # שם המשתמש במסד הנתונים
    # password = 'Trip@1234!'                      # סיסמת המשתמש
    username = 'borgen_SQLLogin_1'                       # שם המשתמש במסד הנתונים
    password = 'rm5m5752q7'                      # סיסמת המשתמש

   
    # יצירת מחרוזת החיבור (connection string) עם כל הפרטים הנחוצים
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"  # מציין את הדרייבר הדרוש לחיבור
        f"SERVER={server};"                           # כתובת השרת
        f"DATABASE={database};"                       # שם מסד הנתונים
        f"UID={username};"                            # שם המשתמש
        f"PWD={password};"                            # סיסמה
        f"TrustServerCertificate=yes;"
    )

    # מחזיר אובייקט חיבור שמאפשר להריץ שאילתות מול מסד הנתונים
    return pyodbc.connect(conn_str)
