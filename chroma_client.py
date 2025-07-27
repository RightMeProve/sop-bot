# chroma_db/db/chroma_client.py

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Set path for persistent DB
CHROMA_DB_PATH = "./chroma_db"

# Define embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_sop_collection():
    """
    Initializes and returns the ChromaDB SOP collection with sentence-transformer embeddings.
    Uses cosine similarity for semantic search.
    """
    # Initialize persistent ChromaDB client
    client = PersistentClient(path=CHROMA_DB_PATH)

    # Set up embedding function
    embedding_function = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

    # Get or create SOP collection
    collection = client.get_or_create_collection(
        name="sop_collection",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


# Optional: debug info when running this file directly
if __name__ == "__main__":
    collection = get_sop_collection()
    print("✅ Existing collections:", [col.name for col in collection._client.list_collections()])
    print("📂 Collection name:", collection.name)
    print("📊 Total SOP documents in collection:", collection.count())
