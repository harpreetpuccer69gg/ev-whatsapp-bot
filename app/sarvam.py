import requests
import os

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
STT_URL = "https://api.sarvam.ai/speech-to-text"

LANG_CODE_MAP = {
    "hi": "hi-IN",
    "en": "en-IN",
    "bn": "bn-IN",
    "kn": "kn-IN"
}


def transcribe_audio(audio_bytes: bytes, lang: str = "en") -> str:
    """Convert voice message bytes to text using Sarvam AI"""
    if not SARVAM_API_KEY:
        return ""

    lang_code = LANG_CODE_MAP.get(lang, "en-IN")

    response = requests.post(
        STT_URL,
        headers={"api-subscription-key": SARVAM_API_KEY},
        files={"file": ("audio.ogg", audio_bytes, "audio/ogg")},
        data={"language_code": lang_code, "model": "saarika:v1"}
    )

    if response.status_code == 200:
        return response.json().get("transcript", "").strip()
    return ""
