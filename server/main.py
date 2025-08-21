# -*- coding: utf-8 -*-
from fastapi import FastAPI
from server.api.user_routes import router as user_router
from server.api.opentrip import router as trip_router
from server.api.ai import router as ai_router
from server.api.weather import router as weather_router
from server.api.opentrip import router as opentrip_router


app = FastAPI(title="Smart Trip API")
app.include_router(opentrip_router)


# חיבור ה־routers
app.include_router(user_router)
app.include_router(trip_router)
app.include_router(ai_router)
app.include_router(weather_router)
# app.include_router(sites_router)

# root פשוט כדי שלא יחזיר 404
@app.get("/")
def root():
    return {"message": "Smart Trip API is running 🚀"}
