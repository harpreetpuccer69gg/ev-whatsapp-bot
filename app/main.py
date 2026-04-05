from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv
from app.bot_flow import process_message, get_session
from app.sarvam import transcribe_audio

load_dotenv()

app = FastAPI(title="EV WhatsApp Bot")

GREEN_API_INSTANCE = os.getenv("GREEN_API_INSTANCE", "")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN", "")
GREEN_API_URL = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}"


async def send_whatsapp(phone: str, message: str):
    url = f"{GREEN_API_URL}/sendMessage/{GREEN_API_TOKEN}"
    payload = {"chatId": f"{phone}@c.us", "message": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        msg_type = data.get("typeWebhook")

        if msg_type not in ["incomingMessageReceived"]:
            return JSONResponse({"status": "ignored"})

        sender_data = data.get("senderData", {})
        phone = sender_data.get("sender", "").replace("@c.us", "")
        msg_data = data.get("messageData", {})
        type_message = msg_data.get("typeMessage")

        text = ""

        # Handle text message
        if type_message == "textMessage":
            text = msg_data.get("textMessageData", {}).get("textMessage", "").strip()

        # Handle voice message
        elif type_message == "audioMessage":
            audio_url = msg_data.get("fileMessageData", {}).get("downloadUrl", "")
            if audio_url:
                async with httpx.AsyncClient() as client:
                    audio_resp = await client.get(audio_url)
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


@app.get("/")
def health():
    return {"status": "EV WhatsApp Bot is running 🚴"}
