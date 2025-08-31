#server/main.py

# הקובץ הזה הוא קובץ הכניסה הראשי של שרת ה־
# FastAPI
# במערכת 
# "Smart Trip".
# הוא מייבא את כל ה־
# routers
# (מודולים של
# API)
# שאחראים על חלקים שונים במערכת,
# מאגד אותם לאפליקציה אחת,
# ומפעיל נקודת קצה ראשית כדי לוודא שהשרת פועל.
from fastapi import FastAPI
from server.api.user_routes import router as user_router        # ניהול משתמשים וטיולים
from server.api.opentrip import router as trip_router           # אתרי תיירות ומסלולים
from server.api.ai import router as ai_router                   # חיבור לסוכן AI
from server.api.weather import router as weather_router         # תחזית מזג אוויר
from server.api.opentrip import router as opentrip_router       # alias נוסף ל־opentrip 



# יצירת מופע ראשי של
# FastAPI
# עם כותרת מותאמת
app = FastAPI(title="Smart Trip API")

# חיבור ה־
# router
# של 
# opentrip
# לאפליקציה
app.include_router(opentrip_router)

# חיבור כל שאר ה־
# routers
# לאפליקציה הראשית:
# user_router – משתמשים וטיולים
# trip_router – אתרים ומסלולים
# ai_router – שאלות ותשובות מול AI
# weather_router – נתוני מזג אוויר
app.include_router(user_router)
app.include_router(trip_router)
app.include_router(ai_router)
app.include_router(weather_router)

# נקודת קצה בסיסית בנתיב
# /
# כדי שלא יוחזר 404 כאשר ניגשים לכתובת הראשית של השרת.
# כאן מוחזרת הודעת סטטוס פשוטה עם טקסט.
@app.get("/")
def root():
    return {"message": "Smart Trip API is running 🚀"}
