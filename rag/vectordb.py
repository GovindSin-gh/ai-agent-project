import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client
client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(name="agent_knowledge")


def embed_text(text):
    """
    Convert text into embedding vector
    """
    return embedding_model.encode(text).tolist()


def add_document(doc_id, text):
    """
    Add knowledge document to vector DB
    """

    embedding = embed_text(text)

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )


def search(query, top_k=3):
    """
    Search relevant documents
    """

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


# Example initial knowledge
def load_initial_knowledge():

    docs = {
        "gmail_signup": """
        To create a Gmail account:
        1. Open https://accounts.google.com/signup
        2. Enter first name and last name
        3. Choose a username
        4. Enter password
        5. Click next
        6. Enter phone number if required
        """,

        "login_google": """
        To login to Google:
        1. Go to https://accounts.google.com
        2. Enter email
        3. Enter password
        4. Click next
        """
    }

    for doc_id, text in docs.items():
        add_document(doc_id, text)


if __name__ == "__main__":
    load_initial_knowledge()
    print("Vector DB initialized with knowledge")
