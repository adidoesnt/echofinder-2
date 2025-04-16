from src.echofinder.openai.main import client
from src.echofinder.constants import EMBEDDING_MODEL

def embed_text(text: str):
    print(f"Embedding text: {text}")
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    print(f"Received embedding response")
    
    print(f"Parsed embedding")
    return response.data[0].embedding
