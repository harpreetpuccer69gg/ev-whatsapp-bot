import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE", "credentials.json")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")

HEADERS = [
    "Timestamp", "Rider Name", "Rider Phone", "City", "Language",
    "Budget Range", "Range Preference", "Vendor", "Make", "Type",
    "Rental/Week", "Security Deposit", "Refundable Deposit",
    "SPOC Name", "SPOC Phone", "Status"
]

BUDGET_LABELS = {
    "1": "Below ₹1000",
    "2": "₹1000 - ₹1500",
    "3": "₹1500 - ₹2000",
    "4": "Above ₹2000"
}

RANGE_LABELS = {
    "1": "Below 60km",
    "2": "60km - 100km",
    "3": "Above 100km"
}

LANG_LABELS = {
    "en": "English", "hi": "Hindi", "bn": "Bengali", "kn": "Kannada"
}


def get_sheet():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1

    # Add headers if sheet is empty
    if sheet.row_count == 0 or sheet.cell(1, 1).value != "Timestamp":
        sheet.insert_row(HEADERS, 1)

    return sheet


def log_lead(session: dict, phone: str):
    chosen = session.get("chosen", {})
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session.get("name", ""),
        phone,
        session.get("city", ""),
        LANG_LABELS.get(session.get("lang", "en"), "English"),
        BUDGET_LABELS.get(session.get("budget", ""), ""),
        RANGE_LABELS.get(session.get("range", ""), ""),
        chosen.get("Vendor", ""),
        chosen.get("Make", ""),
        chosen.get("Type", ""),
        chosen.get("Approx Rental/Week", ""),
        chosen.get("Security Deposit", ""),
        chosen.get("Refundable Deposit", ""),
        chosen.get("SPOC", ""),
        chosen.get("Phone", ""),
        "New Lead"
    ]
    get_sheet().append_row(row)
