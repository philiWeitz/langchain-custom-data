import os
import pickle

from config import EMBEDDINGS_FILE
from langchain.document_loaders import TextLoader, UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

files_directory = os.path.join(os.path.dirname(__file__), "knowledge_base")
files = os.listdir(files_directory)

loaders = [UnstructuredHTMLLoader(os.path.join(files_directory, file)) for file in files]
documents = [loader.load() for loader in loaders]

document = documents[0]
for doc in documents[1:]:
    document += doc

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(texts, embeddings)

with open(EMBEDDINGS_FILE, "wb") as f:
    pickle.dump(vector_store, f)
