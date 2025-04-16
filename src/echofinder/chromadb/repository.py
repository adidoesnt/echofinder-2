from src.echofinder.openai.embedding import embed_text
from src.echofinder.chromadb.main import client

def upsert_embeddings(ids: list[str], documents: list[str], metadata: list[dict[str, str]], collection_name: str):
    print(f"Fetching collection: {collection_name}")
    collection = client.get_or_create_collection(collection_name)
    
    print(f"Embedding documents")
    embeddings = [embed_text(document) for document in documents]
        
    print(f"Upserting vectors into collection: {embeddings}")
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadata=metadata
    )
    
    print(f"Upserted {len(ids)} vectors into collection: {collection_name}")