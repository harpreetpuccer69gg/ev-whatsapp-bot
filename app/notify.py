import requests
import os

FAST2SMS_KEY = os.getenv("FAST2SMS_API_KEY", "")
SENDER_ID = os.getenv("FAST2SMS_SENDER_ID", "EVRIDE")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "")


def send_admin_sms(session: dict, rider_phone: str):
    """Send lead notification SMS to admin (future use)"""
    if not FAST2SMS_KEY or not ADMIN_PHONE:
        return

    chosen = session.get("chosen", {})
    message = (
        f"New EV Lead!\n"
        f"Rider: {session.get('name')} | {rider_phone}\n"
        f"City: {session.get('city')}\n"
        f"Vendor: {chosen.get('Vendor')}\n"
        f"Make: {chosen.get('Make')}\n"
        f"Rental: {chosen.get('Approx Rental/Week')}/week"
    )

    requests.post(
        "https://www.fast2sms.com/dev/bulkV2",
        headers={"authorization": FAST2SMS_KEY},
        data={
            "sender_id": SENDER_ID,
            "message": message,
            "language": "english",
            "route": "v3",
            "numbers": ADMIN_PHONE,
        }
    )
