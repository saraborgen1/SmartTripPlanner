from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api import user, ai
import uvicorn

app = FastAPI(title="Smart Trip API")

# מאפשר גישה מה-Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # בזמן פיתוח – אפשר לשים כתובת מדויקת בפרודקשן
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# רישום הנתיבים
app.include_router(user.router, prefix="/user")
app.include_router(ai.router, prefix="/ai")

# בדיקה שהשרת רץ
@app.get("/")
def root():
    return {"message": "Smart Trip API is running ✅"}

# הפעלה מקומית (אופציונלי)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
