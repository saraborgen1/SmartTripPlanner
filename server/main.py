# # # # from fastapi import FastAPI
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from server.api import ai, user_routes
# # # # import uvicorn

# # # # app = FastAPI(title="Smart Trip API")

# # # # # מאפשר גישה מה-Frontend
# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["*"],  # בזמן פיתוח – אפשר לשים כתובת מדויקת בפרודקשן
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )

# # # # # רישום הנתיבים
# # # # app.include_router(user_routes.router, prefix="/user")
# # # # app.include_router(ai.router, prefix="/ai")

# # # # # בדיקה שהשרת רץ
# # # # @app.get("/")
# # # # def root():
# # # #     return {"message": "Smart Trip API is running ✅"}

# # # # # הפעלה מקומית (אופציונלי)
# # # # if __name__ == "__main__":
# # # #     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# # # # smoke_test.py
# # # import os, json, random, string, time
# # # from datetime import date, timedelta
# # # from fastapi import FastAPI
# # # import requests
# # # app = FastAPI(title="Smart Trip API")
# # # @app.get("/")
# # # def root():
# # #     return {"message": "Smart Trip API is running 🚀"}

# # # BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
# # # TIMEOUT = 40  # שניות לבקשה, חלק מהשירותים איטיים

# # # def _ok(status):
# # #     return 200 <= status < 300

# # # def _rand_username(prefix="testuser_"):
# # #     salt = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
# # #     return f"{prefix}{salt}"

# # # def _print_section(title):
# # #     print("\n" + "="*80)
# # #     print(title)
# # #     print("="*80)

# # # def check_server_alive():
# # #     # ניסיון לפינג כללי: ננסה דף תיעוד של FastAPI (אם מופעל)
# # #     urls = [f"{BASE_URL}/docs", f"{BASE_URL}/openapi.json"]
# # #     for u in urls:
# # #         try:
# # #             r = requests.get(u, timeout=10)
# # #             if r.status_code in (200, 401):  # יש מקרים שיש auth
# # #                 return True, f"Reachable: {u}"
# # #         except Exception as e:
# # #             continue
# # #     return False, "Server not reachable on /docs or /openapi.json. Is uvicorn running?"

# # # def test_weather(city="Jerusalem"):
# # #     url = f"{BASE_URL}/weather_data"
# # #     try:
# # #         r = requests.get(url, params={"city": city}, timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/weather_data HTTP {r.status_code}: {r.text[:200]}"
# # #         data = r.json()
# # #         # בדיקת מבנה בסיסית
# # #         if "destination" in data and "forecast" in data and isinstance(data["forecast"], list):
# # #             return True, f"/weather_data OK for city={city} (days={len(data['forecast'])})"
# # #         return False, f"/weather_data unexpected JSON schema: {json.dumps(data)[:300]}"
# # #     except Exception as e:
# # #         return False, f"/weather_data exception: {e}"

# # # def test_ai(question="Hello from smoke test"):
# # #     url = f"{BASE_URL}/ai"
# # #     try:
# # #         r = requests.get(url, params={"question": question}, timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/ai HTTP {r.status_code}: {r.text[:200]}"
# # #         data = r.json()
# # #         # מצופה משהו כמו {"answer": "..."} או טקסט — נבדוק שיש תוכן
# # #         has_text = isinstance(data, dict) and any(isinstance(v, str) and v.strip() for v in data.values())
# # #         if has_text:
# # #             return True, "/ai OK"
# # #         # אם זה לא dict – נבדוק שיש טקסט גוף
# # #         if isinstance(data, str) and data.strip():
# # #             return True, "/ai OK (string response)"
# # #         return False, f"/ai unexpected response: {str(data)[:300]}"
# # #     except Exception as e:
# # #         # לעתים Ollama לא רץ – נציין כבדיקה “אופציונלית”
# # #         return None, f"/ai optional check failed (LLM likely not running): {e}"

# # # def test_register_and_login():
# # #     username = _rand_username()
# # #     password = "P@ssw0rd!"
# # #     # register
# # #     try:
# # #         r = requests.post(f"{BASE_URL}/register",
# # #                           json={"username": username, "password": password},
# # #                           timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/register HTTP {r.status_code}: {r.text[:200]}", None
# # #     except Exception as e:
# # #         return False, f"/register exception: {e}", None

# # #     # login
# # #     try:
# # #         r = requests.post(f"{BASE_URL}/login",
# # #                           json={"username": username, "password": password},
# # #                           timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/login HTTP {r.status_code}: {r.text[:200]}", None
# # #         # ייתכן שיש token בתשובה או סתם OK
# # #         return True, "/register + /login OK", {"username": username, "password": password}
# # #     except Exception as e:
# # #         return False, f"/login exception: {e}", None

# # # def test_create_and_get_trip(user):
# # #     # נבנה טיול מינימלי תקין לפי התיאור שלך
# # #     start = date.today() + timedelta(days=3)
# # #     end = start + timedelta(days=4)
# # #     trip = {
# # #         "username": user["username"],
# # #         "destination": "Jerusalem",
# # #         "start_date": start.strftime("%Y-%m-%d"),
# # #         "end_date": end.strftime("%Y-%m-%d"),
# # #         "sites": ["Old City", "Israel Museum"],
# # #         "transport": ["walk", "car"],
# # #         "notes": "Smoke test trip"
# # #     }
# # #     # create_trip
# # #     try:
# # #         r = requests.post(f"{BASE_URL}/create_trip", json=trip, timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/create_trip HTTP {r.status_code}: {r.text[:200]}"
# # #     except Exception as e:
# # #         return False, f"/create_trip exception: {e}"

# # #     # my_trips/{username}
# # #     try:
# # #         r = requests.get(f"{BASE_URL}/my_trips/{user['username']}", timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return False, f"/my_trips HTTP {r.status_code}: {r.text[:200]}"
# # #         data = r.json()
# # #         if isinstance(data, list) and any(t.get("destination") == "Jerusalem" for t in data if isinstance(t, dict)):
# # #             return True, "/create_trip + /my_trips OK"
# # #         return False, f"/my_trips returned unexpected data: {str(data)[:300]}"
# # #     except Exception as e:
# # #         return False, f"/my_trips exception: {e}"

# # # def test_get_sites(city="Jerusalem", address="הרצל 10, תל אביב", profile="driving-car"):
# # #     # בדיקה זו תלויה ב־OpenRouteService/OpenTripMap. אם חסר מפתח – ייתכן ותיכשל.
# # #     try:
# # #         r = requests.get(f"{BASE_URL}/get_sites",
# # #                          params={"city": city, "address": address, "profile": profile},
# # #                          timeout=TIMEOUT)
# # #         if not _ok(r.status_code):
# # #             return None, f"/get_sites HTTP {r.status_code}: {r.text[:200]} (optional)"
# # #         data = r.json()
# # #         if isinstance(data, list) and (len(data) == 0 or isinstance(data[0], dict)):
# # #             return True, f"/get_sites OK (items={len(data)})"
# # #         return None, f"/get_sites unexpected schema (optional): {str(data)[:300]}"
# # #     except Exception as e:
# # #         return None, f"/get_sites optional check failed: {e}"

# # # def main():
# # #     _print_section("SmartTripPlanner - Smoke Test")

# # #     ok, msg = check_server_alive()
# # #     print(f"Server alive? {ok} | {msg}")
# # #     if not ok:
# # #         return

# # #     # 1) weather
# # #     ok, msg = test_weather()
# # #     print(msg)

# # #     # 2) ai (אופציונלי, תלוי Ollama)
# # #     ai_ok, ai_msg = test_ai()
# # #     if ai_ok is True:
# # #         print(ai_msg)
# # #     elif ai_ok is None:
# # #         print(f"AI check skipped: {ai_msg}")
# # #     else:
# # #         print(f"AI FAILED: {ai_msg}")

# # #     # 3) register + login
# # #     ok, msg, user = test_register_and_login()
# # #     print(msg)
# # #     if not ok or not user:
# # #         print("Stopping after register/login failure.")
# # #         return

# # #     # 4) create_trip + my_trips
# # #     ok, msg = test_create_and_get_trip(user)
# # #     print(msg)

# # #     # 5) get_sites (אופציונלי — תלוי מפתחות חיצוניים וזמינות השירותים)
# # #     gs_ok, gs_msg = test_get_sites()
# # #     if gs_ok is True:
# # #         print(gs_msg)
# # #     else:
# # #         print(f"get_sites skipped/partial: {gs_msg}")

# # #     _print_section("Done")

# # # if __name__ == "__main__":
# # #     main()

# # # -*- coding: utf-8 -*-
# # """
# # Smoke test for SmartTripPlanner FastAPI server.

# # Runs a quick end-to-end check of key endpoints:
# #   - /docs or /openapi.json (server alive)
# #   - /register, /login
# #   - /create_trip, /my_trips/{username}
# #   - /ai?question=...
# #   - /weather_data?city=...
# #   - /get_sites?city=...&address=...&profile=...

# # Usage:
# #   python smoke_test.py
# #   (optional) set BASE_URL env var, default: http://127.0.0.1:8000
# # """

# # import os
# # import sys
# # import time
# # import json
# # import random
# # import string
# # from datetime import date, timedelta
# # import requests
# # from fastapi import FastAPI

# # app = FastAPI(title="Smart Trip API")
# # @app.get("/")
# # def root():
# #     return {"message": "Smart Trip API is running 🚀"}

# # BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
# # TIMEOUT = int(os.getenv("SMOKE_TIMEOUT", "30"))

# # def _ok(status: int) -> bool:
# #     return 200 <= status < 300

# # def _rand_username(prefix="smoke_") -> str:
# #     salt = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
# #     return f"{prefix}{salt}"

# # def section(title: str):
# #     print("\n" + "="*80)
# #     print(title)
# #     print("="*80)

# # def try_get(url: str, **kwargs):
# #     try:
# #         r = requests.get(url, timeout=TIMEOUT, **kwargs)
# #         return r, None
# #     except Exception as e:
# #         return None, e

# # def try_post(url: str, **kwargs):
# #     try:
# #         r = requests.post(url, timeout=TIMEOUT, **kwargs)
# #         return r, None
# #     except Exception as e:
# #         return None, e

# # def check_server_alive():
# #     section("Server alive (/docs or /openapi.json)")
# #     for path in ("/docs", "/openapi.json"):
# #         r, err = try_get(BASE_URL + path)
# #         if r and _ok(r.status_code):
# #             print(f"[PASS] GET {path} -> {r.status_code}")
# #             return True
# #         else:
# #             msg = f"{err}" if err else f"HTTP {r.status_code if r else 'N/A'}"
# #             print(f"[WARN] GET {path} failed: {msg}")
# #     return False

# # def test_register_login():
# #     section("Auth: /register and /login")
# #     username = _rand_username()
# #     password = "P@ssw0rd!"
# #     r, err = try_post(f"{BASE_URL}/register", json={"username": username, "password": password})
# #     if not (r and _ok(r.status_code)):
# #         print(f"[FAIL] POST /register -> {r.status_code if r else 'N/A'}; err={err or r.text}")
# #         return False, username, password
# #     print(f"[PASS] POST /register {username}")

# #     r, err = try_post(f"{BASE_URL}/login", json={"username": username, "password": password})
# #     if not (r and _ok(r.status_code)):
# #         print(f"[FAIL] POST /login -> {r.status_code if r else 'N/A'}; err={err or r.text}")
# #         return False, username, password
# #     print(f"[PASS] POST /login {username}")
# #     return True, username, password

# # def test_create_and_list_trips(username: str):
# #     section("Trips: /create_trip and /my_trips/{username}")
# #     start = date.today() + timedelta(days=7)
# #     end = start + timedelta(days=3)
# #     payload = {
# #         "username": username,
# #         "destination": "Jerusalem",
# #         "start_date": start.strftime("%Y-%m-%d"),
# #         "end_date": end.strftime("%Y-%m-%d"),
# #         "selected_sites": ["Old City", "Mahane Yehuda Market"],
# #         "transport": ["רכב"],
# #         "notes": "Smoke test trip"
# #     }
# #     r, err = try_post(f"{BASE_URL}/create_trip", json=payload)
# #     if not (r and _ok(r.status_code)):
# #         print(f"[FAIL] POST /create_trip -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
# #         return False

# #     print(f"[PASS] POST /create_trip (id not returned, stored server-side)")

# #     r, err = try_get(f"{BASE_URL}/my_trips/{username}")
# #     if not (r and _ok(r.status_code)):
# #         print(f"[FAIL] GET /my_trips/{username} -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
# #         return False
# #     try:
# #         trips = r.json()
# #         print(f"[PASS] GET /my_trips/{username} -> {len(trips)} trip(s)")
# #     except Exception as e:
# #         print(f"[WARN] Could not parse trips JSON: {e}")
# #     return True

# # def test_ai():
# #     section("AI proxy: GET /ai?question=...")
# #     r, err = try_get(f"{BASE_URL}/ai", params={"question": "מה מזג האוויר בירושלים היום?"})
# #     if not (r and _ok(r.status_code)):
# #         print(f"[WARN] GET /ai failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
# #         return False
# #     try:
# #         data = r.json()
# #         print(f"[PASS] /ai responded. keys={list(data.keys())}")
# #     except Exception as e:
# #         print(f"[WARN] /ai JSON parse error: {e}")
# #         return False
# #     return True

# # def test_weather():
# #     section("Weather: GET /weather_data?city=Jerusalem")
# #     r, err = try_get(f"{BASE_URL}/weather_data", params={"city": "Jerusalem"})
# #     if not (r and _ok(r.status_code)):
# #         print(f"[WARN] /weather_data failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
# #         return False
# #     try:
# #         data = r.json()
# #         keys = list(data.keys())
# #         print(f"[PASS] /weather_data responded. keys={keys}")
# #     except Exception as e:
# #         print(f"[WARN] /weather_data JSON parse error: {e}")
# #         return False
# #     return True

# # def test_get_sites():
# #     section("Sites & routes: GET /get_sites")
# #     params = {
# #         "city": "Jerusalem",
# #         "address": "King George St 10, Jerusalem",
# #         "profile": "driving-car",
# #     }
# #     r, err = try_get(f"{BASE_URL}/get_sites", params=params)
# #     if not (r and _ok(r.status_code)):
# #         print(f"[WARN] /get_sites failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
# #         return False
# #     try:
# #         data = r.json()
# #         print(f"[PASS] /get_sites responded. type={type(data).__name__}, len={len(data) if isinstance(data, list) else 'N/A'}")
# #     except Exception as e:
# #         print(f"[WARN] /get_sites JSON parse error: {e}")
# #         return False
# #     return True

# # def main():
# #     results = {}
# #     results["alive"] = check_server_alive()
# #     ok_auth, username, _ = test_register_login()
# #     results["auth"] = ok_auth

# #     if ok_auth:
# #         results["trips"] = test_create_and_list_trips(username)
# #     else:
# #         results["trips"] = False

# #     results["ai"] = test_ai()
# #     results["weather"] = test_weather()
# #     results["sites"] = test_get_sites()

# #     section("Summary")
# #     total = sum(1 for v in results.values() if v)
# #     print(json.dumps(results, ensure_ascii=False, indent=2))
# #     print(f"\nPASSED {total}/{len(results)} checks")

# #     must = ["alive", "auth", "trips"]
# #     exit_code = 0 if all(results.get(k) for k in must) else 1
# #     sys.exit(exit_code)

# # if __name__ == "__main__":
# #     main()




# # -*- coding: utf-8 -*-
# from fastapi import FastAPI
# from server.api.user_routes import router as user_router
# from server.api.opentrip import router as trip_router
# from server.api.ai import router as ai_router
# from server.api.weather import router as weather_router
# # from server.api.sites import router as sites_router

# app = FastAPI()
# app.include_router(user_router)
# app.include_router(trip_router)
# app.include_router(ai_router)
# app.include_router(weather_router)
# # app.include_router(sites_router)

# # ========================
# # בדיקות smoke מתחילות כאן
# # ========================
# import os, sys, json, requests, random, string
# from datetime import date, timedelta

# BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
# TIMEOUT = int(os.getenv("SMOKE_TIMEOUT", "30"))

# def _ok(status: int) -> bool:
#     return 200 <= status < 300

# def _rand_username(prefix="smoke_") -> str:
#     return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
#     end = start + timedelta(days=10)
#     payload = {
#         "username": username,
#         "destination": "Jerusalem",
#         "start_date": start.strftime("%Y-%m-%d"),
#         "end_date": end.strftime("%Y-%m-%d"),
#         "selected_sites": ["Old City", "Mahane Yehuda"],
#         "transport": ["רכב"],
#         "notes": "בדיקה"
#     }
#     r, err = try_post(f"{BASE_URL}/create_trip", json=payload)
#     if not (r and _ok(r.status_code)):
#         print(f"[FAIL] POST /create_trip -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
#         return False
#     print(f"[PASS] POST /create_trip")

#     r, err = try_get(f"{BASE_URL}/my_trips/{username}")
#     if not (r and _ok(r.status_code)):
#         print(f"[FAIL] GET /my_trips/{username} -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
#         return False
#     try:
#         trips = r.json()
#         print(f"[PASS] GET /my_trips/{username} -> {len(trips)} trips")
#     except Exception as e:
#         print(f"[WARN] trips JSON error: {e}")
#     return True

# def test_ai():
#     section("AI: /ai?question=...")
#     r, err = try_get(f"{BASE_URL}/ai", params={"question": "מה מזג האוויר בירושלים?"})
#     if not (r and _ok(r.status_code)):
#         print(f"[WARN] /ai failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
#         return False
#     try:
#         print(f"[PASS] /ai responded: {list(r.json().keys())}")
#     except:
#         print(f"[WARN] /ai JSON error")
#         return False
#     return True

# def test_weather():
#     section("Weather: /weather_data?city=Jerusalem")
#     r, err = try_get(f"{BASE_URL}/weather_data", params={"city": "Jerusalem"})
#     if not (r and _ok(r.status_code)):
#         print(f"[WARN] /weather_data failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
#         return False
#     try:
#         print(f"[PASS] /weather_data responded: {list(r.json().keys())}")
#     except:
#         print(f"[WARN] /weather_data JSON error")
#         return False
#     return True

# def test_get_sites():
#     section("Sites: /get_sites")
#     params = {
#         "city": "Jerusalem",
#         "address": "King George St 10",
#         "profile": "driving-car"
#     }
#     r, err = try_get(f"{BASE_URL}/get_sites", params=params)
#     if not (r and _ok(r.status_code)):
#         print(f"[WARN] /get_sites failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
#         return False
#     try:
#         print(f"[PASS] /get_sites responded: {len(r.json())} items")
#     except:
#         print(f"[WARN] /get_sites JSON error")
#         return False
#     return True

# def run_smoke_test():
#     results = {}
#     results["alive"] = check_server_alive()
#     ok_auth, username, _ = test_register_login()
#     results["auth"] = ok_auth
#     results["trips"] = test_create_and_list_trips(username) if ok_auth else False
#     results["ai"] = test_ai()
#     results["weather"] = test_weather()
#     results["sites"] = test_get_sites()

#     section("Summary")
#     total = sum(1 for v in results.values() if v)
#     print(json.dumps(results, ensure_ascii=False, indent=2))
#     print(f"\n✅ PASSED {total}/{len(results)} checks")

# # ===== רק אם מריצים ישירות =====
# if __name__ == "__main__":
#     run_smoke_test()

# -*- coding: utf-8 -*-
from fastapi import FastAPI
from server.api.user_routes import router as user_router
from server.api.opentrip import router as trip_router
from server.api.ai import router as ai_router
from server.api.weather import router as weather_router
# from server.api.sites import router as sites_router

app = FastAPI(title="Smart Trip API")

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
