import os
import pickle

from pydash import head, tail

from config import EMBEDDINGS_FILE
from langchain.document_loaders import ConfluenceLoader, UnstructuredHTMLLoader
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

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(vector_store, f)


# https://llamahub.ai/l/confluence
def get_from_confluence():
    confluence_loader = ConfluenceLoader(
        url=os.getenv("CONFLUENCE_URL"),
        api_key=os.getenv("CONFLUENCE_API_TOKEN"),
        username=os.getenv("CONFLUENCE_USER_NAME"),
        max_retry_seconds=1,
    )

    documents = confluence_loader.load(
        page_ids=["11111111"],
        include_attachments=False,
        include_archived_content=False,
        include_comments=False,
        max_pages=5,
    )

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(vector_store, f)


get_from_local_knowledge_base()
# get_from_confluence()
