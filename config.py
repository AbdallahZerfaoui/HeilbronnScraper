import os

PROXY_URL = os.getenv("PROXY_URL", "http://ikhyxlmu-rotate:mcfoaj670x36@p.webshare.io:80/")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://adamberlin112020:f6nEppPx0fOlHImd@cluster0.zbx2q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

HTTP_BIN = os.getenv("HTTP_BIN", "https://httpbin.org/ip")
STMP_SERVER = os.getenv("STMP_SERVER", "smtp.gmail.com")
STMP_PORT = os.getenv("STMP_PORT", 587)

SENDER = os.getenv("SENDER", "adamberlin112020@gmail.com")
PASSWORD = os.getenv("PASSWORD", "wqoqcacupvplpzxg")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "zerfaouiabdallah@gmail.com")

CONTACTS_FILE = os.getenv("CONTACTS_FILE", "contacts.txt")
MESSAGE = os.getenv("MESSAGE", "message.txt")
SUBJECT = os.getenv("SUBJECT", "Your appointment")

MAX_DISTANCE = 160
TIMEOUT = 30
BASE_DIR = os.path.abspath("io")