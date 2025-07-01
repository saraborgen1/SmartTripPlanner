# server/main.py
from fastapi import FastAPI
from .api import api as ai
from .api import opentrip
from .api import weather


app = FastAPI()

app.include_router(opentrip.router)
app.include_router(weather.router)


# רישום הנתיב של הסוכן
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {"msg": "SmartTripPlanner backend is running!"}







