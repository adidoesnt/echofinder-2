from src.echofinder.openai.embedding import embed_text
from src.echofinder.chromadb.main import client
from src.echofinder.constants import CHROMA_N_RESULTS

def upsert_embeddings(ids: list[str], documents: list[str], metadata: list[dict[str, str]], collection_name: str):
    print(f"Fetching collection: {collection_name}")
    collection = client.get_or_create_collection(
        name=collection_name,
    )
    
    print(f"Embedding documents")
    embeddings = [embed_text(document) for document in documents]
        
    print(f"Upserting vectors into collection {collection_name}")
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadata,
    )
    
    print(f"Upserted {len(ids)} vectors into collection: {collection_name}")
    
def search_embeddings(query: str, collection_name: str, where: dict[str, str]):
    print(f"Searching for {query} in collection: {collection_name}")
    collection = client.get_or_create_collection(
        name=collection_name,
    )
    
    print(f"Embedding query")
    query_embedding = embed_text(query)
    
    print(f"Searching for {query} in collection: {collection_name}")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=CHROMA_N_RESULTS,
        where=where,
    )
    
    print(f"Found {len(results['documents'][0])} results")
    return {
        "documents": results['documents'][0],
        "ids": results['ids'][0],
        "metadatas": results['metadatas'][0],
    }
