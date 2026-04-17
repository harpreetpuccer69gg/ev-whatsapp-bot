import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from app.sheets import log_lead

# Test session data
test_session = {
    "name": "Test Rider",
    "city": "Bangalore",
    "lang": "en",
    "budget": "2",
    "range": "2",
    "chosen": {
        "Vendor": "Linkmiles",
        "Make": "Bgauss C12i Max",
        "Type": "Hi-Speed",
        "Approx Rental/Week": "1610-1750",
        "Security Deposit": "3000",
        "Refundable Deposit": "1500",
        "SPOC": "Navya",
        "Phone": "8105073464"
    }
}

try:
    log_lead(test_session, "919999999999")
    print("SUCCESS - Google Sheets working! Check your sheet for test row.")
except Exception as e:
    print("FAILED - Error: " + str(e))
