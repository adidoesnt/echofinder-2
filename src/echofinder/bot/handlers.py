from telebot.types import Message

from src.echofinder.constants import CHROMA_COLLECTION_NAME
from src.echofinder.chromadb.repository import upsert_embeddings, search_embeddings, get_embeddings
from src.echofinder.bot.types import MessageInfo
from src.echofinder.openai.summarisation import get_prompt_response

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
        
def search_messages(query: str, chat_id: int):
    print(f"Searching for {query} in collection: {CHROMA_COLLECTION_NAME}")
    
    results = search_embeddings(query, CHROMA_COLLECTION_NAME, {"chat_id": chat_id})
    print(f"Found {len(results['documents'])} results")
    
    return results

def get_last_n_messages(chat_id: int, n: int) -> dict[str, list[str]]:
    results = get_embeddings(CHROMA_COLLECTION_NAME, {"chat_id": chat_id})
    
    combined = list(zip(results['documents'], results['metadatas']))
    combined.sort(key=lambda x: x[1]['sent_at'])
    combined = combined[-n:]
    
    print(f"Fetched last {n} messages from chat {chat_id}: {combined}")
    
    return combined

def get_summarisation_prompt(messages: list[dict[str, str]]):
    print(f"Getting summarisation prompt for {len(messages)} messages")
    
    prompt_template = """
You are a helpful assistant that summarises text messages in personal and group chats.
Summarise the following text messages:\n
{messages}\n
You may refer to users by their first name, unless two users share the same first name.
"""
        
    prompt = prompt_template.format(messages="\n".join([f"{message[1]['firstname']} {message[1]['lastname'] if message[1]['lastname'] else ''}: {message[0]}" for message in messages]))
    print(f"Prompt: {prompt}")
    
    return prompt

def summarise_messages(n: str, chat_id: int):
    print(f"Summarising {n} messages")
    
    if not n.isdigit():
        response = "Number of messages to summarise must be a number"
        return response
    
    n = int(n)
    
    if n < 1 or n > 200:
        response = "Number of messages to summarise must be between 1 and 200"
        return response
    
    print(f"Getting last {n} messages from chat {chat_id}")
    last_n_messages = get_last_n_messages(chat_id, n)
    
    if n > len(last_n_messages):
        print("[WARNING] n is greater than the number of messages, using all messages")
    
    prompt = get_summarisation_prompt(last_n_messages)
    
    response = get_prompt_response(prompt)
    print(f"Response: {response}")
    
    return response
