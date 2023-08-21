import os
import pickle
import shutil
from uuid import uuid4

from pydash import is_empty, reject

from config import EMBEDDINGS_FILE
from langchain.document_loaders import BSHTMLLoader, ConfluenceLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from scraper import Scraper

URLS = [
    "https://www.finder.fi/Kaavoitus+ja+maank%C3%A4yt%C3%B6nsuunnittelu/CHAOS+Architect+Oy/Helsinki/yhteystiedot/3122669",
    "https://vainu.io/company/chaos-architects-oy-taloustiedot-ja-liikevaihto/7000255/yritystiedot",
    "https://chaosarchitects.com",
    "https://chaosarchitects.com/dashboards",
    "https://chaosarchitects.com/customer-cases",
    "https://chaosarchitects.com/vision/",
    "https://chaosarchitects.com/team/",
    "https://chaosarchitects.com/blog/",
]


def get_from_local_knowledge_base():
    files_directory = os.path.join(os.path.dirname(__file__), "knowledge_base")
    get_embeddings_from_html_in_folder(files_directory)


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

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(vector_store, f)


def get_by_url():
    scraped_files_directory = os.path.join(
        os.path.dirname(__file__), "scraped_html"
    )

    if os.path.exists(scraped_files_directory):
        shutil.rmtree(scraped_files_directory)

    os.makedirs(scraped_files_directory)

    scraper = Scraper()

    for url in URLS:
        html_content = scraper.get_html_content(url)
        last_url_part = reject(url.split("/"), is_empty)[-1].replace(".", "-")
        file_name = f"{last_url_part}-{uuid4()}.html"

        with open(
            os.path.join(scraped_files_directory, file_name), "w"
        ) as file:
            file.write(html_content)

    get_embeddings_from_html_in_folder(scraped_files_directory)


def get_embeddings_from_html_in_folder(folder_path):
    files = os.listdir(folder_path)

    loaders = [BSHTMLLoader(os.path.join(folder_path, file)) for file in files]
    documents = [loader.load()[0] for loader in loaders]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(vector_store, f)


get_from_local_knowledge_base()
# get_from_confluence()
# get_by_url()
