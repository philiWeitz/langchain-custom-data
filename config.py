import os

from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_FILE = os.path.join("embeddings", "faiss_openai_embeddings.pkl")
