from src.echofinder.bot.main import init_bot
from src.echofinder.chromadb.main import init_chroma_client

if __name__ == "__main__":
    init_chroma_client()
    init_bot()
