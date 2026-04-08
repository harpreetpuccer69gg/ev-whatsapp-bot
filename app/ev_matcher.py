import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/vendors.json")

BUDGET_RANGES = {
    "1": (0, 1000),
    "2": (1000, 1500),
    "3": (1500, 2000),
    "4": (2000, 99999),
}

RANGE_RANGES = {
    "1": (0, 60),
    "2": (60, 100),
    "3": (100, 99999),
}


def load_vendors():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_rental(rental_str):
    """Extract minimum rental value from string like '1610-1750' or '1500' or '₹59/day + ₹1.50/km'"""
    try:
        s = str(rental_str).replace("₹", "").replace(",", "").strip()
        # Extract first number found (handles '59/day + ...' and '179/- Day' etc.)
        import re
        numbers = re.findall(r'\d+', s)
        if not numbers:
            return None
        first = int(numbers[0])
        # If it looks like a daily rate (small number < 500), convert to weekly
        if "/day" in rental_str.lower() or "day" in rental_str.lower():
            return first * 7
        return first
    except:
        return None


def parse_range(range_str):
    """Extract minimum range value from string like '80-105' or '100'"""
    try:
        s = str(range_str).replace("km", "").strip()
        if "-" in s:
            return int(s.split("-")[0].strip())
        if "(" in s:
            return int(s.split("(")[0].strip())
        return int(float(s))
    except:
        return None


def match_vendors(city: str, budget_key: str, range_key: str, has_licence: bool = True):
    vendors = load_vendors()
    city_lower = city.strip().lower()

    city_vendors = [
        v for v in vendors
        if v.get("City", "").strip().lower() == city_lower
        and v.get("Status", "").strip().upper() in ["LIVE", "LIVE FROM NEXT WEEK", "MINUTES WIP"]
    ]

    if not city_vendors:
        return [], True

    # Filter by licence
    if not has_licence:
        city_vendors = [
            v for v in city_vendors
            if v.get("Type", "").strip().lower() in ["low speed", "e-cycle"]
        ]

    if not city_vendors:
        return [], True

    budget_min, budget_max = BUDGET_RANGES.get(budget_key, (0, 99999))
    range_min, range_max = RANGE_RANGES.get(range_key, (0, 99999))

    matched = []
    for v in city_vendors:
        rental = parse_rental(v.get("Approx Rental/Week"))
        km_range = parse_range(v.get("Range (Km)"))

        if rental is None or km_range is None:
            continue

        if budget_min <= rental <= budget_max and range_min <= km_range <= range_max:
            matched.append(v)

    fallback = False
    if not matched:
        matched = city_vendors
        fallback = True

    return matched, fallback


PHOTO_MAP = {
    "bgauss": "https://www.bgauss.com/wp-content/uploads/2023/01/C12i-MAX-Red.png",
    "yulu dex": "https://www.yulu.bike/wp-content/uploads/2022/06/Dex-Yellow.png",
    "ecargo": "https://www.nexzu.com/images/ecargo.png",
    "hum cycles": "https://www.motovolt.com/wp-content/uploads/2021/06/hum-cycle.png",
    "volt up": "https://voltup.in/wp-content/uploads/2022/08/voltup-bike.png",
    "vida": "https://www.heromotocorp.com/content/dam/hero-motocorp/vida/v1-pro.png",
    "bounce": "https://bounce.bike/wp-content/uploads/2022/06/infinity-e1.png",
    "kinetic": "https://www.kineticgreen.com/images/e-luna.png",
    "komaki": "https://komaki.in/wp-content/uploads/2022/06/xone.png",
    "maki": "https://goewent.com/images/maki.png",
}


def get_photo_url(make: str) -> str:
    if not make:
        return ""
    make_lower = make.lower()
    for key, url in PHOTO_MAP.items():
        if key in make_lower:
            return url
    return ""


def format_option(index: int, vendor: dict, lang: str = "en") -> str:
    name = vendor.get("Vendor", "N/A")
    make = vendor.get("Make", "N/A") or "N/A"
    rental = vendor.get("Approx Rental/Week", "N/A")
    km = vendor.get("Range (Km)", "N/A")
    deposit = vendor.get("Security Deposit", "N/A") or "N/A"
    refundable = vendor.get("Refundable Deposit", "Not available") or "Not available"
    charge_type = vendor.get("Charging/Swap", "N/A") or "N/A"
    photo = get_photo_url(make)
    photo_line = f"\n📸 {photo}" if photo else ""

    if lang == "hi":
        return (
            f"*{index}. {name} - {make}*\n"
            f"💰 किराया: ₹{rental}/सप्ताह\n"
            f"🔋 रेंज: {km} km\n"
            f"🔒 सिक्योरिटी डिपॉजिट: ₹{deposit}\n"
            f"↩️ रिफंडेबल: ₹{refundable}\n"
            f"⚡ चार्जिंग: {charge_type}{photo_line}"
        )
    elif lang == "bn":
        return (
            f"*{index}. {name} - {make}*\n"
            f"💰 ভাড়া: ₹{rental}/সপ্তাহ\n"
            f"🔋 রেঞ্জ: {km} km\n"
            f"🔒 সিকিউরিটি ডিপোজিট: ₹{deposit}\n"
            f"↩️ ফেরতযোগ্য: ₹{refundable}\n"
            f"⚡ চার্জিং: {charge_type}{photo_line}"
        )
    elif lang == "kn":
        return (
            f"*{index}. {name} - {make}*\n"
            f"💰 ಬಾಡಿಗೆ: ₹{rental}/ವಾರ\n"
            f"🔋 ರೇಂಜ್: {km} km\n"
            f"🔒 ಭದ್ರತಾ ಠೇವಣಿ: ₹{deposit}\n"
            f"↩️ ಮರುಪಾವತಿ: ₹{refundable}\n"
            f"⚡ ಚಾರ್ಜಿಂಗ್: {charge_type}{photo_line}"
        )
    else:
        return (
            f"*{index}. {name} - {make}*\n"
            f"💰 Rental: ₹{rental}/week\n"
            f"🔋 Range: {km} km\n"
            f"🔒 Security Deposit: ₹{deposit}\n"
            f"↩️ Refundable: ₹{refundable}\n"
            f"⚡ Charging: {charge_type}{photo_line}"
        )
