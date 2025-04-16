import os
import json
from dotenv import load_dotenv

load_dotenv()

# Environment
ENV = os.getenv("ENV", "dev")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")
TELEGRAM_BOT_SERVER_PORT = os.getenv("PORT", 8001)

# Chroma
CHROMA_CLIENT_AUTH_CREDENTIALS = os.getenv("CHROMA_CLIENT_AUTH_CREDENTIALS")
CHROMA_CLIENT_AUTH_PROVIDER = os.getenv("CHROMA_CLIENT_AUTH_PROVIDER")
CHROMA_CLIENT_HOST = os.getenv("CHROMA_CLIENT_HOST", "localhost")
CHROMA_CLIENT_PORT = os.getenv("CHROMA_CLIENT_PORT", 8000)
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "messages")
CHROMA_N_RESULTS = os.getenv("CHROMA_N_RESULTS", 5)

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
SUMMARISATION_MODEL = os.getenv("SUMMARISATION_MODEL", "gpt-4o-mini")

# Config
config = None
with open("src/echofinder/config.json", "r") as f:
    config = json.load(f)

