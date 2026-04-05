# EV WhatsApp Bot 🚴

A WhatsApp bot that helps delivery riders find EV rentals in their city.
Supports Hindi, English, Bengali and Kannada.

---

## Conversation Flow

```
Rider: Hi
Bot: Welcome! Select language (1-Hindi, 2-English, 3-Bengali, 4-Kannada)
Rider: 2
Bot: Please share your name
Rider: Rahul
Bot: Please share your city
Rider: Bangalore
Bot: What is your weekly budget? (1/2/3/4)
Rider: 2
Bot: How much daily range do you need? (1/2/3)
Rider: 2
Bot: Here are top 3 EV options... (with deposit info)
Rider: 1
Bot: Confirmed! Vendor will contact you in 24 hours
→ Lead logged to Google Sheet
```

---

## Setup Instructions

### 1. Clone & Install
```bash
cd ev-whatsapp-bot
pip install -r requirements.txt
```

### 2. Green API (WhatsApp - Free 3 months)
- Sign up at https://green-api.com
- Create an instance and scan QR code with WhatsApp
- Copy Instance ID and API Token to `.env`
- Set webhook URL to: `https://your-domain.com/webhook`

### 3. Sarvam AI (Voice STT - Free 1000 calls/month)
- Sign up at https://sarvam.ai
- Get API key and add to `.env`

### 4. Google Sheets (Free)
- Go to https://console.cloud.google.com
- Create a project → Enable Google Sheets API
- Create Service Account → Download credentials.json
- Place credentials.json in project root
- Create a new Google Sheet
- Share the sheet with the service account email
- Copy Sheet ID from URL to `.env`

### 5. Fast2SMS (Future - Admin SMS)
- Sign up at https://fast2sms.com
- Get API key and add to `.env`

### 6. Run Locally
```bash
uvicorn app.main:app --reload --port 8000
```

### 7. Deploy Free on Render.com
- Push code to GitHub
- Go to https://render.com → New Web Service
- Connect GitHub repo
- Set environment variables from `.env`
- Deploy!

---

## Project Structure

```
ev-whatsapp-bot/
├── app/
│   ├── main.py          # FastAPI server + webhook
│   ├── bot_flow.py      # Conversation flow + multilingual
│   ├── ev_matcher.py    # EV matching engine
│   ├── sarvam.py        # Voice STT (Sarvam AI)
│   ├── sheets.py        # Google Sheets logging
│   └── notify.py        # SMS admin alert (future)
├── data/
│   └── vendors.json     # EV vendor database
├── .env                 # API keys
├── requirements.txt
└── README.md
```

---

## Google Sheet Columns

| Column | Description |
|--------|-------------|
| Timestamp | When lead was created |
| Rider Name | Name provided by rider |
| Rider Phone | WhatsApp number |
| City | City selected |
| Language | Language chosen |
| Budget Range | Weekly budget preference |
| Range Preference | Daily range preference |
| Vendor | Selected vendor name |
| Make | Vehicle make/model |
| Type | Hi-Speed / Low speed / E-Cycle |
| Rental/Week | Weekly rental amount |
| Security Deposit | Security deposit amount |
| Refundable Deposit | Refundable amount |
| SPOC Name | Vendor contact person |
| SPOC Phone | Vendor contact number |
| Status | New Lead |
