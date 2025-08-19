# -*- coding: utf-8 -*-
"""
Smoke test for SmartTripPlanner FastAPI server.

Runs a quick end-to-end check of key endpoints:
  - /docs or /openapi.json (server alive)
  - /register, /login
  - /create_trip, /my_trips/{username}
  - /ai?question=...
  - /weather_data?city=...
  - /get_sites?city=...&address=...&profile=...

Usage:
  python smoke_test.py
  (optional) set BASE_URL env var, default: http://127.0.0.1:8000
"""

import os
import sys
import time
import json
import random
import string
from datetime import date, timedelta
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = int(os.getenv("SMOKE_TIMEOUT", "30"))

def _ok(status: int) -> bool:
    return 200 <= status < 300

def _rand_username(prefix="smoke_") -> str:
    salt = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}{salt}"

def section(title: str):
    print("\n" + "="*80)
    print(title)
    print("="*80)

def try_get(url: str, **kwargs):
    try:
        r = requests.get(url, timeout=TIMEOUT, **kwargs)
        return r, None
    except Exception as e:
        return None, e

def try_post(url: str, **kwargs):
    try:
        r = requests.post(url, timeout=TIMEOUT, **kwargs)
        return r, None
    except Exception as e:
        return None, e

def check_server_alive():
    section("Server alive (/docs or /openapi.json)")
    for path in ("/docs", "/openapi.json"):
        r, err = try_get(BASE_URL + path)
        if r and _ok(r.status_code):
            print(f"[PASS] GET {path} -> {r.status_code}")
            return True
        else:
            msg = f"{err}" if err else f"HTTP {r.status_code if r else 'N/A'}"
            print(f"[WARN] GET {path} failed: {msg}")
    return False

def test_register_login():
    section("Auth: /register and /login")
    username = _rand_username()
    password = "P@ssw0rd!"
    r, err = try_post(f"{BASE_URL}/register", json={"username": username, "password": password})
    if not (r and _ok(r.status_code)):
        print(f"[FAIL] POST /register -> {r.status_code if r else 'N/A'}; err={err or r.text}")
        return False, username, password
    print(f"[PASS] POST /register {username}")

    r, err = try_post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if not (r and _ok(r.status_code)):
        print(f"[FAIL] POST /login -> {r.status_code if r else 'N/A'}; err={err or r.text}")
        return False, username, password
    print(f"[PASS] POST /login {username}")
    return True, username, password

def test_create_and_list_trips(username: str):
    section("Trips: /create_trip and /my_trips/{username}")
    start = date.today() + timedelta(days=7)
    end = start + timedelta(days=3)
    payload = {
        "username": username,
        "destination": "Jerusalem",
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "selected_sites": ["Old City", "Mahane Yehuda Market"],
        "transport": ["רכב"],
        "notes": "Smoke test trip"
    }
    r, err = try_post(f"{BASE_URL}/create_trip", json=payload)
    if not (r and _ok(r.status_code)):
        print(f"[FAIL] POST /create_trip -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
        return False

    print(f"[PASS] POST /create_trip (id not returned, stored server-side)")

    r, err = try_get(f"{BASE_URL}/my_trips/{username}")
    if not (r and _ok(r.status_code)):
        print(f"[FAIL] GET /my_trips/{username} -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
        return False
    try:
        trips = r.json()
        print(f"[PASS] GET /my_trips/{username} -> {len(trips)} trip(s)")
    except Exception as e:
        print(f"[WARN] Could not parse trips JSON: {e}")
    return True

def test_ai():
    section("AI proxy: GET /ai?question=...")
    r, err = try_get(f"{BASE_URL}/ai", params={"question": "מה מזג האוויר בירושלים היום?"})
    if not (r and _ok(r.status_code)):
        print(f"[WARN] GET /ai failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
        return False
    try:
        data = r.json()
        print(f"[PASS] /ai responded. keys={list(data.keys())}")
    except Exception as e:
        print(f"[WARN] /ai JSON parse error: {e}")
        return False
    return True

def test_weather():
    section("Weather: GET /weather_data?city=Jerusalem")
    r, err = try_get(f"{BASE_URL}/weather_data", params={"city": "Jerusalem"})
    if not (r and _ok(r.status_code)):
        print(f"[WARN] /weather_data failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
        return False
    try:
        data = r.json()
        keys = list(data.keys())
        print(f"[PASS] /weather_data responded. keys={keys}")
    except Exception as e:
        print(f"[WARN] /weather_data JSON parse error: {e}")
        return False
    return True

def test_get_sites():
    section("Sites & routes: GET /get_sites")
    params = {
        "city": "Jerusalem",
        "address": "King George St 10, Jerusalem",
        "profile": "driving-car",
    }
    r, err = try_get(f"{BASE_URL}/get_sites", params=params)
    if not (r and _ok(r.status_code)):
        print(f"[WARN] /get_sites failed -> {r.status_code if r else 'N/A'}; err={err or (r.text if r else '')}")
        return False
    try:
        data = r.json()
        print(f"[PASS] /get_sites responded. type={type(data).__name__}, len={len(data) if isinstance(data, list) else 'N/A'}")
    except Exception as e:
        print(f"[WARN] /get_sites JSON parse error: {e}")
        return False
    return True

def main():
    results = {}
    results["alive"] = check_server_alive()
    ok_auth, username, _ = test_register_login()
    results["auth"] = ok_auth

    if ok_auth:
        results["trips"] = test_create_and_list_trips(username)
    else:
        results["trips"] = False

    results["ai"] = test_ai()
    results["weather"] = test_weather()
    results["sites"] = test_get_sites()

    section("Summary")
    total = sum(1 for v in results.values() if v)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nPASSED {total}/{len(results)} checks")

    must = ["alive", "auth", "trips"]
    exit_code = 0 if all(results.get(k) for k in must) else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
