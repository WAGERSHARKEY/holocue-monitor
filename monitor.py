import time
import requests

# --- CONFIG ---
THINGSBOARD_URL = "http://147.182.255.178:9090"  # Your ThingsBoard URL
THINGSBOARD_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzaGFya2V5bW9yZ2FuM0BnbWFpbC5jb20iLCJ1c2VySWQiOiI3YmJkNjAwMC02YjhiLTExZjAtYTkxZC00NTMzNDgyOGFkNGEiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6IjI2MzZlNTQ2LTUwMmItNGMzYS1hMjUxLTdmZDQ3MDllNmIxYiIsImV4cCI6MTc1NTAwNDcxNywiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3NTQ5OTU3MTcsImZpcnN0TmFtZSI6Ik1vcmdhbiIsImxhc3ROYW1lIjoiV2FnYWNoYWtpIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjViZDVmNGEwLTZiOGItMTFmMC1hOTFkLTQ1MzM0ODI4YWQ0YSIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.5O_uocx0B9cZA555rrlTaGubCJNmqKXuB48pUqiovmdkshqQphkin5uk3VbPG-JXz_XKn48bxLUaF3dyE96gSQ"  # Paste token from /api/auth/login
DEVICE_ID = "70f52b90-71cf-11f0-a91d-45334828ad4a"  # Device ID
CHECK_INTERVAL = 60  # seconds between checks

TELEGRAM_BOT_TOKEN = "8047829388:AAF4BH9TmgJRT9zhyJuyUV3g404tTwKFJak"
TELEGRAM_CHAT_ID = "6624444269"

# --- FUNCTIONS ---
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, json=payload)

def get_last_activity():
    url = f"{THINGSBOARD_URL}/api/device/{DEVICE_ID}"
    headers = {"X-Authorization": f"Bearer {THINGSBOARD_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return data.get("lastActivityTime")
    else:
        print("Failed to fetch device info:", r.text)
        return None

# --- MAIN LOOP ---
last_alert = 0
while True:
    last_activity = get_last_activity()
    if last_activity:
        seconds_since_active = (time.time() * 1000 - last_activity) / 1000
        if seconds_since_active > 300 and (time.time() - last_alert > 300):
            send_telegram_message(f"⚠ Device inactive for {int(seconds_since_active / 60)} minutes!")
            last_alert = time.time()
    time.sleep(CHECK_INTERVAL)
