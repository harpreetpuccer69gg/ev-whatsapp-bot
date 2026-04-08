import requests

SESSION = "evbot"
TOKEN = "$2b$10$I.l0AmPEi_U2V9dl7kscVeIyDha.roT4kNUClVKxjQ5SZDhxQBpFO"
BASE_URL = "http://localhost:21465"
HEADERS = {"Authorization": f"Bearer {SESSION}:{TOKEN}", "Content-Type": "application/json"}

# Start session
r = requests.post(f"{BASE_URL}/api/{SESSION}/start-session", headers=HEADERS, json={"webhook": "", "waitQrCode": False})
print("Start session:", r.json())
