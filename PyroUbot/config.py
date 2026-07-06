import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "8150856435").split()))

API_ID = int(os.getenv("API_ID", "31495965"))

API_HASH = os.getenv("API_HASH", "fbb76d2fc08ee0bd33f86dde82fc1f3a")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8610838719:AAE2p6QcJMW2WoQJo3PvMep2CHG4qCcw39o")

OWNER_ID = int(os.getenv("OWNER_ID", "8150856435"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1003730428070").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://nexxacrossz_db_user:<db_password>@cluster0.xo8sh2k.mongodb.net/?appName=Cluster0")

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1003730428070"))
