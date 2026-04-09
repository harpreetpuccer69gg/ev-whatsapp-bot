from app.ev_matcher import match_vendors, format_option

# In-memory session store {phone: session_data}
sessions = {}

MESSAGES = {
    "en": {
        "welcome": "👋 Welcome to *EV Assist*!\nI'll help you find the best EV rental.\n\nPlease select your language:\n1️⃣ Hindi\n2️⃣ English\n3️⃣ Bengali\n4️⃣ Kannada",
        "ask_licence": "🪪 Do you have a valid *driving licence*?\n\n1️⃣ Yes\n2️⃣ No",
        "no_licence_info": "✅ No problem! We'll show you *low speed EVs* that don't require a licence.",
        "ask_name": "Great! 😊 Please share your *name*.",
        "ask_city": "Thanks {name}! 🏙️ Please share your *city name*.",
        "ask_budget": "Got it! 💰 What is your *weekly budget*?\n\n1️⃣ Below ₹1000\n2️⃣ ₹1000 - ₹1500\n3️⃣ ₹1500 - ₹2000\n4️⃣ Above ₹2000",
        "ask_range": "Perfect! 🔋 How much *daily range* do you need?\n\n1️⃣ Below 60 km\n2️⃣ 60 km - 100 km\n3️⃣ Above 100 km",
        "results": "🎯 Here are your top EV options in *{city}*:\n\n{options}\n\nReply *1, 2 or 3* to confirm your choice.",
        "fallback": "⚠️ No exact match found. Here are *all available vendors* in {city}:\n\n{options}\n\nReply *1, 2 or 3* to confirm your choice.",
        "no_city": "😔 Sorry, we don't have vendors in *{city}* yet. Please try another city.",
        "confirm": "✅ Great choice, *{name}*!\n\n*{vendor}* will contact you within *24 hours* for your EV rental in *{city}*.\n\nThank you for using EV Assist! 🚴",
        "invalid": "❌ Invalid option. Please reply with a valid number.",
        "invalid_lang": "Please reply with 1, 2, 3 or 4 to select language.",
    },
    "hi": {
        "welcome": "👋 *EV Assist* में आपका स्वागत है!\nमैं आपको सबसे अच्छा EV किराया खोजने में मदद करूंगा।\n\nभाषा चुनें:\n1️⃣ हिंदी\n2️⃣ English\n3️⃣ Bengali\n4️⃣ Kannada",
        "ask_licence": "🪪 क्या आपके पास वैध *ड्राइविंग लाइसेंस* है?\n\n1️⃣ हाँ\n2️⃣ नहीं",
        "no_licence_info": "✅ कोई बात नहीं! हम आपको *लो स्पीड EV* दिखाएंगे जिनके लिए लाइसेंस की जरूरत नहीं।",
        "ask_name": "बढ़िया! 😊 कृपया अपना *नाम* बताएं।",
        "ask_city": "धन्यवाद {name}! 🏙️ कृपया अपना *शहर* बताएं।",
        "ask_budget": "ठीक है! 💰 आपका *साप्ताहिक बजट* क्या है?\n\n1️⃣ ₹1000 से कम\n2️⃣ ₹1000 - ₹1500\n3️⃣ ₹1500 - ₹2000\n4️⃣ ₹2000 से अधिक",
        "ask_range": "बढ़िया! 🔋 आपको कितनी *दैनिक रेंज* चाहिए?\n\n1️⃣ 60 km से कम\n2️⃣ 60 km - 100 km\n3️⃣ 100 km से अधिक",
        "results": "🎯 *{city}* में आपके लिए शीर्ष EV विकल्प:\n\n{options}\n\nअपनी पसंद के लिए *1, 2 या 3* जवाब दें।",
        "fallback": "⚠️ सटीक मिलान नहीं मिला। {city} में *सभी उपलब्ध विक्रेता*:\n\n{options}\n\nअपनी पसंद के लिए *1, 2 या 3* जवाब दें।",
        "no_city": "😔 माफ़ करें, *{city}* में अभी कोई विक्रेता नहीं है।",
        "confirm": "✅ बढ़िया चुनाव, *{name}*!\n\n*{vendor}* आपसे *24 घंटे* के भीतर *{city}* में EV किराए के लिए संपर्क करेगा।\n\nEV Assist का उपयोग करने के लिए धन्यवाद! 🚴",
        "invalid": "❌ गलत विकल्प। कृपया सही नंबर से जवाब दें।",
        "invalid_lang": "कृपया भाषा चुनने के लिए 1, 2, 3 या 4 से जवाब दें।",
    },
    "bn": {
        "welcome": "👋 *EV Assist*-এ আপনাকে স্বাগতম!\nআমি আপনাকে সেরা EV ভাড়া খুঁজে পেতে সাহায্য করব।\n\nভাষা নির্বাচন করুন:\n1️⃣ Hindi\n2️⃣ English\n3️⃣ Bengali\n4️⃣ Kannada",
        "ask_licence": "🪪 আপনার কি বৈধ *ড্রাইভিং লাইসেন্স* আছে?\n\n1️⃣ হ্যাঁ\n2️⃣ না",
        "no_licence_info": "✅ কোনো সমস্যা নেই! আমরা আপনাকে *লো স্পিড EV* দেখাব যেগুলোর জন্য লাইসেন্স দরকার নেই।",
        "ask_name": "দারুণ! 😊 আপনার *নাম* জানান।",
        "ask_city": "ধন্যবাদ {name}! 🏙️ আপনার *শহরের নাম* জানান।",
        "ask_budget": "ঠিক আছে! 💰 আপনার *সাপ্তাহিক বাজেট* কত?\n\n1️⃣ ₹1000-এর নিচে\n2️⃣ ₹1000 - ₹1500\n3️⃣ ₹1500 - ₹2000\n4️⃣ ₹2000-এর উপরে",
        "ask_range": "চমৎকার! 🔋 আপনার কতটুকু *দৈনিক রেঞ্জ* দরকার?\n\n1️⃣ 60 km-এর নিচে\n2️⃣ 60 km - 100 km\n3️⃣ 100 km-এর উপরে",
        "results": "🎯 *{city}*-তে আপনার জন্য সেরা EV বিকল্প:\n\n{options}\n\nআপনার পছন্দ নিশ্চিত করতে *1, 2 বা 3* উত্তর দিন।",
        "fallback": "⚠️ সঠিক মিল পাওয়া যায়নি। {city}-তে *সব উপলব্ধ বিক্রেতা*:\n\n{options}\n\nআপনার পছন্দ নিশ্চিত করতে *1, 2 বা 3* উত্তর দিন।",
        "no_city": "😔 দুঃখিত, *{city}*-তে এখনো কোনো বিক্রেতা নেই।",
        "confirm": "✅ দারুণ পছন্দ, *{name}*!\n\n*{vendor}* *24 ঘণ্টার* মধ্যে *{city}*-তে আপনার EV ভাড়ার জন্য যোগাযোগ করবে।\n\nEV Assist ব্যবহার করার জন্য ধন্যবাদ! 🚴",
        "invalid": "❌ ভুল বিকল্প। সঠিক নম্বর দিয়ে উত্তর দিন।",
        "invalid_lang": "ভাষা নির্বাচন করতে 1, 2, 3 বা 4 দিয়ে উত্তর দিন।",
    },
    "kn": {
        "welcome": "👋 *EV Assist*ಗೆ ಸ್ವಾಗತ!\nನಾನು ನಿಮಗೆ ಅತ್ಯುತ್ತಮ EV ಬಾಡಿಗೆ ಹುಡುಕಲು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.\n\nಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ:\n1️⃣ Hindi\n2️⃣ English\n3️⃣ Bengali\n4️⃣ Kannada",
        "ask_licence": "🪪 ನಿಮ್ಮ ಬಳಿ ಮಾನ್ಯ *ಡ್ರೈವಿಂಗ್ ಲೈಸೆನ್ಸ್* ಇದೆಯೇ?\n\n1️⃣ ಹೌದು\n2️⃣ ಇಲ್ಲ",
        "no_licence_info": "✅ ಪರವಾಗಿಲ್ಲ! ನಾವು ನಿಮಗೆ *ಲೋ ಸ್ಪೀಡ್ EV* ತೋರಿಸುತ್ತೇವೆ ಅದಕ್ಕೆ ಲೈಸೆನ್ಸ್ ಬೇಕಿಲ್ಲ.",
        "ask_name": "ಅದ್ಭುತ! 😊 ನಿಮ್ಮ *ಹೆಸರು* ತಿಳಿಸಿ.",
        "ask_city": "ಧನ್ಯವಾದ {name}! 🏙️ ನಿಮ್ಮ *ನಗರದ ಹೆಸರು* ತಿಳಿಸಿ.",
        "ask_budget": "ಸರಿ! 💰 ನಿಮ್ಮ *ವಾರದ ಬಜೆಟ್* ಎಷ್ಟು?\n\n1️⃣ ₹1000 ಕೆಳಗೆ\n2️⃣ ₹1000 - ₹1500\n3️⃣ ₹1500 - ₹2000\n4️⃣ ₹2000 ಮೇಲೆ",
        "ask_range": "ಅದ್ಭುತ! 🔋 ನಿಮಗೆ ಎಷ್ಟು *ದೈನಂದಿನ ರೇಂಜ್* ಬೇಕು?\n\n1️⃣ 60 km ಕೆಳಗೆ\n2️⃣ 60 km - 100 km\n3️⃣ 100 km ಮೇಲೆ",
        "results": "🎯 *{city}*ನಲ್ಲಿ ನಿಮಗಾಗಿ ಅತ್ಯುತ್ತಮ EV ಆಯ್ಕೆಗಳು:\n\n{options}\n\nನಿಮ್ಮ ಆಯ್ಕೆ ದೃಢೀಕರಿಸಲು *1, 2 ಅಥವಾ 3* ಉತ್ತರಿಸಿ.",
        "fallback": "⚠️ ನಿಖರ ಹೊಂದಾಣಿಕೆ ಸಿಗಲಿಲ್ಲ. {city}ನಲ್ಲಿ *ಎಲ್ಲಾ ಲಭ್ಯ ವಿಕ್ರೇತರು*:\n\n{options}\n\nನಿಮ್ಮ ಆಯ್ಕೆ ದೃಢೀಕರಿಸಲು *1, 2 ಅಥವಾ 3* ಉತ್ತರಿಸಿ.",
        "no_city": "😔 ಕ್ಷಮಿಸಿ, *{city}*ನಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ವಿಕ್ರೇತರಿಲ್ಲ.",
        "confirm": "✅ ಅದ್ಭುತ ಆಯ್ಕೆ, *{name}*!\n\n*{vendor}* *24 ಗಂಟೆಗಳಲ್ಲಿ* *{city}*ನಲ್ಲಿ ನಿಮ್ಮ EV ಬಾಡಿಗೆಗಾಗಿ ಸಂಪರ್ಕಿಸುತ್ತಾರೆ.\n\nEV Assist ಬಳಸಿದ್ದಕ್ಕೆ ಧನ್ಯವಾದ! 🚴",
        "invalid": "❌ ತಪ್ಪು ಆಯ್ಕೆ. ದಯವಿಟ್ಟು ಸರಿಯಾದ ಸಂಖ್ಯೆಯಲ್ಲಿ ಉತ್ತರಿಸಿ.",
        "invalid_lang": "ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಲು 1, 2, 3 ಅಥವಾ 4 ಉತ್ತರಿಸಿ.",
    },
}

LANG_MAP = {"1": "hi", "2": "en", "3": "bn", "4": "kn"}


def get_msg(lang, key, **kwargs):
    msg = MESSAGES.get(lang, MESSAGES["en"]).get(key, "")
    return msg.format(**kwargs) if kwargs else msg


def get_session(phone):
    if phone not in sessions:
        sessions[phone] = {"step": "language"}
    return sessions[phone]


def clear_session(phone):
    sessions.pop(phone, None)


def process_message(phone: str, message: str) -> str:
    msg = message.strip()
    session = get_session(phone)
    step = session.get("step")
    lang = session.get("lang", "en")

    # Step 1: Language selection
    if step == "language":
        if msg in LANG_MAP:
            session["lang"] = LANG_MAP[msg]
            session["step"] = "licence"
            return get_msg(LANG_MAP[msg], "ask_licence")
        # First message - show welcome
        if msg.lower() in ["hi", "hello", "hey", "start", "helo"]:
            return get_msg("en", "welcome")
        return get_msg("en", "invalid_lang")

    # Step 2: Licence check
    if step == "licence":
        if msg not in ["1", "2"]:
            return get_msg(lang, "invalid")
        session["licence"] = msg == "1"
        session["step"] = "name"
        if msg == "2":
            return get_msg(lang, "no_licence_info") + "\n\n" + get_msg(lang, "ask_name")
        return get_msg(lang, "ask_name")

    # Step 3: Name
    if step == "name":
        session["name"] = msg.title()
        session["step"] = "city"
        return get_msg(lang, "ask_city", name=session["name"])

    # Step 3: City
    if step == "city":
        session["city"] = msg.title()
        session["step"] = "budget"
        return get_msg(lang, "ask_budget")

    # Step 4: Budget
    if step == "budget":
        if msg not in ["1", "2", "3", "4"]:
            return get_msg(lang, "invalid")
        session["budget"] = msg
        session["step"] = "confirm"

        city = session["city"]
        has_licence = session.get("licence", True)
        vendors, fallback = match_vendors(city, session["budget"], "all", has_licence)

        if not vendors:
            clear_session(phone)
            return get_msg(lang, "no_city", city=city)

        session["vendors"] = vendors
        options_text = "\n\n".join([format_option(i + 1, v, lang) for i, v in enumerate(vendors)])

        if fallback:
            return get_msg(lang, "fallback", city=city, options=options_text)
        return get_msg(lang, "results", city=city, options=options_text)

    # Step 6: Confirmation
    if step == "confirm":
        vendors = session.get("vendors", [])
        if msg not in [str(i + 1) for i in range(len(vendors))]:
            return get_msg(lang, "invalid")

        chosen = vendors[int(msg) - 1]
        session["chosen"] = chosen
        session["step"] = "done"

        # Log to Google Sheet
        try:
            from app.sheets import log_lead
            log_lead(session, phone)
        except Exception:
            pass

        # Notify admin (WhatsApp group - future)
        try:
            from app.notify import send_admin_sms
            send_admin_sms(session, phone)
        except Exception:
            pass

        name = session.get("name", "Rider")
        city = session.get("city", "")
        vendor = chosen.get("Vendor", "")
        clear_session(phone)
        return get_msg(lang, "confirm", name=name, vendor=vendor, city=city)

    # Restart if done
    clear_session(phone)
    return get_msg("en", "welcome")
