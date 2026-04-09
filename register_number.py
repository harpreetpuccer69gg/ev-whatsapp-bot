import requests

PHONE_NUMBER_ID = "1100933029766806"
ACCESS_TOKEN = "EAAVRGTGdkesBRIFgJ2afmmf3XMJ3UnG89XZACIELMIu8dUoRHnhyws83VQ9pVJZCioaXZCcsZBfqViUAtq1SjaCpMIEse61pd8wyqrOMZAvv1HnkgL9UrSgni8ZCKDxxZBjC7WV2CUtJwjrsm6GBaexDsPKZAV6q7nVqo1idgVZB2BrixDWZBvDL0fWCLD5fuzHAZDZD"

# Register number
url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/register"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
payload = {
    "messaging_product": "whatsapp",
    "pin": "123456"
}

r = requests.post(url, headers=headers, json=payload)
print("Register response:", r.json())
