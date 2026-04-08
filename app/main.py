from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv
from app.bot_flow import process_message, get_session
from app.sarvam import transcribe_audio

load_dotenv()

app = FastAPI(title="EV WhatsApp Bot")

# Meta API config
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "evassist2024")
META_API_URL = f"https://graph.facebook.com/v22.0/{META_PHONE_NUMBER_ID}/messages"


async def send_whatsapp(phone: str, message: str):
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    async with httpx.AsyncClient() as client:
        await client.post(META_API_URL, json=payload, headers=headers)


# Webhook verification (Meta requires GET verification)
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return int(challenge)
    return JSONResponse({"status": "forbidden"}, status_code=403)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()

        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return JSONResponse({"status": "ignored"})

        msg = messages[0]
        phone = msg.get("from", "")
        msg_type = msg.get("type", "")
        text = ""

        if msg_type == "text":
            text = msg.get("text", {}).get("body", "").strip()
        elif msg_type == "audio":
            audio_url = msg.get("audio", {}).get("url", "")
            if audio_url:
                async with httpx.AsyncClient() as client:
                    audio_resp = await client.get(
                        audio_url,
                        headers={"Authorization": f"Bearer {META_ACCESS_TOKEN}"}
                    )
                    audio_bytes = audio_resp.content
                session = get_session(phone)
                lang = session.get("lang", "en")
                text = transcribe_audio(audio_bytes, lang)

        if not text or not phone:
            return JSONResponse({"status": "empty"})

        reply = process_message(phone, text)
        await send_whatsapp(phone, reply)
        return JSONResponse({"status": "ok"})

    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)


@app.post("/process")
async def process(request: Request):
    data = await request.json()
    phone = data.get("phone", "")
    message = data.get("message", "")
    if not phone or not message:
        return JSONResponse({"reply": ""})
    reply = process_message(phone, message)
    return JSONResponse({"reply": reply})


@app.get("/")
@app.head("/")
def health():
    return {"status": "EV WhatsApp Bot is running 🚴"}
