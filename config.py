import os

PROXY_URL = os.getenv("PROXY_URL", "http://ikhyxlmu-rotate:mcfoaj670x36@p.webshare.io:80/")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://adamberlin112020:f6nEppPx0fOlHImd@cluster0.zbx2q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

BOOKER_URL = os.getenv("BOOKER_URL", "https://www.qtermin.de/qtermin-stadtheilbronn-abh?lang=de")
PROFILES = os.getenv("PROFILES", "profiles.csv")

# SELECTORS
RESIDENT_PERMIT_FAMILY = os.getenv("RESIDENT_PERMIT_FAMILY", "h1#sg63091txt")
COUNTER_PLUS = os.getenv("COUNTER_PLUS", "span.counterPlus")
CONTINUE_BUTTON = os.getenv("CONTINUE_BUTTON", "button#bp1")
SLOT1 = os.getenv("SLOT1", "li#slot1")

HTTP_BIN = os.getenv("HTTP_BIN", "https://httpbin.org/ip")
STMP_SERVER = os.getenv("STMP_SERVER", "smtp.gmail.com")
STMP_PORT = os.getenv("STMP_PORT", 587)

SENDER = os.getenv("SENDER", "adamberlin112020@gmail.com")
PASSWORD = os.getenv("PASSWORD", "wqoqcacupvplpzxg")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "zerfaouiabdallah@gmail.com")

CONTACTS_FILE = os.getenv("CONTACTS_FILE", "contacts.csv")
MESSAGE = os.getenv("MESSAGE", "message.html")
SUBJECT = os.getenv("SUBJECT", "Your appointment")
LOCATION_LINK = os.getenv("LOCATION_LINK", "https://maps.google.com/maps?hl=de&gl=de&um=1&ie=UTF-8&fb=1&sa=X&ftid=0x47982f412dab0e6f:0x30aa9965f34723b")
OFFICE_ADDRESS = os.getenv("OFFICE_ADDRESS", "Marktpl. 7, 74072 Heilbronn")
OFFICE_NAME = os.getenv("OFFICE_NAME", "Stadt Heilbronn")

MAX_DISTANCE = 170
TIMEOUT = 30
BASE_DIR = os.path.abspath("io")