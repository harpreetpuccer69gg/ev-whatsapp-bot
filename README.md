# EV Assist - Flipkart Minutes 🛵

A responsive web app that helps Flipkart delivery riders find and book EV rentals in their city.
Supports Hindi, English, Bengali and Kannada.

🌐 **Live:** https://ev-rental-in-minutes.onrender.com
📊 **Leads Sheet:** https://docs.google.com/spreadsheets/d/1RwPcbZp8Wtv5HRdp7uXIMupEmp6V5HXtrAiElx7DEPI/edit
📄 **Docs:** https://docs.google.com/document/d/1b2901P0-3EQTdFiNRjN9KKJIrWRpQnbrmuTDmkvVS9M/edit?tab=t.0

---

## Features

- **Hero Carousel** — 4 posters with auto-slide (5s) and manual swipe (Android + iOS)
- **City Selector** — 13 cities across India
- **Budget Filter** — 4 weekly budget ranges
- **EV Results** — Search, filter by type (Hi-Speed / Low Speed / E-Cycle), sort by price
- **EV Detail Page** — Range, charging, deposit, refundable deposit, weekly rent
- **Booking Form** — Rider enters name + phone, vendor contacts in 24 hours
- **Multilingual** — English, Hindi, Bengali, Kannada
- **Auto Lead Capture** — Every booking logs to Google Sheets
- **Disclaimer** — Shown on YuvwaaSpeed and Bounce detail pages
- **Mobile Responsive** — Works on any Android or iPhone browser

---

## Vendors (40+ entries across 13 cities)

Bounce, YuvwaaSpeed, Yulu, Freedo, Bijliride, Bykemania, Volt Up, EMO, Linkmiles,
Nexzu, Motovolt, TezzFleet, Zeway, Yugo, Blive, Go Green, Zorro, EcoEV, Evify, Baaz

---

## Setup Instructions

### 1. Clone & Install
```bash
cd ev-whatsapp-bot
pip install -r requirements.txt
```

### 2. Google Sheets
- Go to https://console.cloud.google.com
- Create a project → Enable Google Sheets API
- Create Service Account → Download credentials.json
- Place credentials.json in project root
- Share the sheet with the service account email
- Copy Sheet ID from URL to `.env`

### 3. Environment Variables (.env)
```
GOOGLE_SHEET_ID=your_sheet_id
```

### 4. Run Locally
```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Deploy on Render.com
- Push code to GitHub
- Go to https://render.com → New Web Service
- Connect GitHub repo → branch: `main`
- Set environment variables from `.env`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Deploy — auto-redeploys on every push to main

---

## Project Structure

```
ev-whatsapp-bot/
├── app/
│   ├── main.py              # FastAPI server + routes
│   ├── sheets.py            # Google Sheets lead logging
│   └── static/
│       ├── index.html       # Main landing page
│       ├── bounce.html      # Bounce second page
│       └── images/          # EV and vendor images
├── data/
│   └── vendors.json         # EV vendor database (40+ entries)
├── .env                     # API keys
├── render.yaml              # Render deployment config
├── requirements.txt
└── README.md
```

---

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main landing page |
| `/bounce` | GET | Bounce second page |
| `/vendors` | GET | Returns vendors.json as JSON |
| `/submit-lead` | POST | Logs lead to Google Sheets |
| `/health` | GET | Health check |

---

## Google Sheet Columns

| Column | Description |
|--------|-------------|
| Timestamp | When lead was created |
| Rider Name | Name provided by rider |
| Rider Phone | Mobile number |
| City | City selected |
| Language | Language chosen |
| Budget Range | Weekly budget preference |
| Vendor | Selected vendor name |
| Make | Vehicle make/model |
| Type | Hi-Speed / Low Speed / E-Cycle |
| Rental/Week | Weekly rental amount |
| Security Deposit | Security deposit amount |
| Refundable Deposit | Refundable amount |
| SPOC Name | Vendor contact person |
| SPOC Phone | Vendor contact number |
| Status | New Lead |
