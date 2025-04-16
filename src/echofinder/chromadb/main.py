import chromadb

from src.echofinder.constants import CHROMA_CLIENT_HOST, CHROMA_CLIENT_PORT, CHROMA_CLIENT_AUTH_CREDENTIALS, CHROMA_CLIENT_AUTH_PROVIDER

client = chromadb.HttpClient(
    host=CHROMA_CLIENT_HOST,
    port=CHROMA_CLIENT_PORT,
    settings=chromadb.Settings(
        chroma_client_auth_provider=CHROMA_CLIENT_AUTH_PROVIDER,
        chroma_client_auth_credentials=CHROMA_CLIENT_AUTH_CREDENTIALS,
    ),
)

def init_chroma_client():
    print("Initialising Chroma client...")
    client.heartbeat()
    
    print("Chroma client initialised")
    