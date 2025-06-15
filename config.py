# config.py

import os

API_ID = int(os.getenv("API_ID", 123456))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URL = os.getenv("MONGO_URL", "your_mongo_url")

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-100xxxxxxxxxx"))
OWNER_ID = int(os.getenv("OWNER_ID", 123456789))
