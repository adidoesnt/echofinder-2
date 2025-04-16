import os
import json
from dotenv import load_dotenv

load_dotenv()

# Environment
ENV = os.getenv("ENV", "dev")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Config
config = None
with open("src/echofinder/config.json", "r") as f:
    config = json.load(f)

