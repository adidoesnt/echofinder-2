from telebot.types import Message

from src.echofinder.constants import CHROMA_COLLECTION_NAME
from src.echofinder.chromadb.repository import upsert_embeddings
from src.echofinder.bot.types import MessageInfo

def save_messages(messages: list[Message]):
    print(f"Saving {len(messages)} messages")
    
    try:
        ids = [str(message.id) for message in messages]
        documents = [message.text for message in messages]
        metadata = [MessageInfo(
            message_id=message.id,
            chat_id=message.chat.id,
            firstname=message.from_user.first_name,
            lastname=message.from_user.last_name if message.from_user.last_name else "",
            username=message.from_user.username if message.from_user.username else "",
            sender_id=message.from_user.id,
            sent_at=message.date
        ).model_dump(mode='json') for message in messages]
    
        upsert_embeddings(ids, documents, metadata, CHROMA_COLLECTION_NAME)
        
        print(f"Saved {len(messages)} messages")
    except Exception as e:
        print(f"Error saving messages: {e}")
