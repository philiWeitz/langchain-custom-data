import os
import pickle

from pydash import head, tail

from config import EMBEDDINGS_FILE
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


def get_from_local_knowledge_base():
    files_directory = os.path.join(os.path.dirname(__file__), "knowledge_base")
    files = os.listdir(files_directory)

    loaders = [
        UnstructuredHTMLLoader(os.path.join(files_directory, file))
        for file in files
    ]
    documents = [loader.load() for loader in loaders]

    document = head(documents)
    for doc in tail(documents):
        document += doc

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(document)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(vector_store, f)


get_from_local_knowledge_base()
