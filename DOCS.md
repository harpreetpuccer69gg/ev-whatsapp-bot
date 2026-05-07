# EV Assist - Flipkart Minutes | Project Documentation

---

## 🔗 Important Links

| Resource | Link |
|----------|------|
| 🌐 Live Landing Page | https://ev-rental-in-minutes.onrender.com |
| 📊 Google Sheet (Leads) | https://docs.google.com/spreadsheets/d/1RwPcbZp8Wtv5HRdp7uXIMupEmp6V5HXtrAiElx7DEPI/edit?gid=0#gid=0 |
| 📄 Project Documentation | https://docs.google.com/document/d/1b2901P0-3EQTdFiNRjN9KKJIrWRpQnbrmuTDmkvVS9M/edit?tab=t.0 |

---

## 🏗️ What We Have Built

### Landing Page (Page 1 - Main)
- A fully responsive **EV rental discovery web app** for Flipkart Minutes delivery riders
- **Hero carousel** with 4 posters:
  - Poster 1 — General EV rental intro with delivery rider image
  - Poster 2 — YuvwaaSpeed special offer (₹59/day) with bike image
  - Poster 3 — Flipkart Minutes EV poster with scannable QR code
  - Poster 4 — Yulu DeX poster, clicking opens Yulu detail page
- **City selector** — 13 cities supported (Bangalore, Mumbai, Delhi NCR, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, Guwahati, Patna, Coimbatore)
- **Weekly budget filter** — 4 budget ranges (Below ₹1000 / ₹1000–1500 / ₹1500–2000 / ₹2000+)
- **EV results** with search, filter by type (Hi-Speed / Low Speed / E-Cycle), sort by price
- **EV detail page** — full slide-in page showing range, charging, deposit, refundable deposit, weekly rent
- **Booking confirmation sheet** — rider enters name + phone to submit lead
- **Multilingual support** — English, Hindi, Bengali, Kannada
- **Intro popup** — language + city selection on first visit
- **Success popup** — confirmation after lead submission

### Vendors Added
- **40+ vendor entries** across 13 cities including:
  - Bounce (Bangalore, Hyderabad, Delhi NCR) — ₹1750/week, Swap, 75km, ₹500 refundable deposit
  - YuvwaaSpeed, Yulu, Baaz, Bykemania, Volt Up, Freedo, Bijliride, EMO, Linkmiles, Nexzu, Motovolt, TezzFleet, Zeway, Yugo, Blive, Go Green, Zorro, EcoEV, Speedz, e-went, Evify

### Lead Capture → Google Sheet
- Every time a rider submits a booking request, the following is logged automatically:
  - Timestamp, Rider Name, Phone, City, Language, Budget, Vendor, Make, Type, Weekly Rent, Security Deposit, Refundable Deposit, SPOC Name, SPOC Phone, Status

### Page 2 — Bounce Page (`/bounce`)
- Separate route serving the second page
- Accessible via Bounce EV card "Book Now" or Poster 3 click

---

## 🚴 How It Benefits Delivery Riders

| Benefit | Details |
|---------|---------|
| ✅ One place for all EVs | Riders don't need to search multiple vendors — all options in one page |
| ✅ Budget-based filtering | Riders can filter EVs by their weekly budget so no time wasted |
| ✅ Transparent pricing | Weekly rent, security deposit, refundable deposit all shown upfront |
| ✅ City-specific results | Only shows EVs available in the rider's city |
| ✅ Multilingual | Supports Hindi, Bengali, Kannada — riders can use in their own language |
| ✅ Fast booking | Rider just enters name + phone — vendor contacts within 24 hours |
| ✅ Mobile friendly | Fully responsive, works perfectly on any Android/iPhone |
| ✅ No app download needed | Works directly in browser — zero friction |
| ✅ Special offers visible | Featured deals like YuvwaaSpeed ₹59/day shown on hero banner |

---

## 🚀 Deployment

| Detail | Info |
|--------|------|
| Platform | [Render.com](https://render.com) — Free tier |
| Service Type | Web Service (Python) |
| Framework | FastAPI + Uvicorn |
| Branch | `main` on GitHub |
| Auto Deploy | ✅ Yes — every push to `main` triggers redeploy automatically |
| Port | `$PORT` (assigned by Render, default 10000) |
| Repo | https://github.com/harpreetpuccer69gg/ev-rental.in.minutes |

### How Deployment Works
1. Code is pushed to GitHub (`main` branch)
2. Render detects the new commit automatically
3. Runs `pip install -r requirements.txt`
4. Starts server with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Live in ~1–2 minutes at https://ev-rental-in-minutes.onrender.com

---

## ✅ Conclusion

The **EV Assist - Flipkart Minutes** platform is a complete, production-deployed web solution that connects Flipkart delivery riders with EV rental vendors across 13 Indian cities. 

Riders can visit the landing page, select their city and budget, browse available EVs with full pricing transparency, and submit a booking request in under 60 seconds — all from their mobile browser without downloading any app.

Every lead is automatically captured in Google Sheets, giving the operations team real-time visibility into rider demand, city-wise interest, and vendor performance.

The platform is live, scalable, and ready to onboard more vendors and cities as Flipkart Minutes expands.

---

*Last Updated: May 2025*
