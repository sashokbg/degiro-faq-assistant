import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from promptflow.core import tool

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.HttpClient(settings=Settings(allow_reset=True), host='localhost', port=8000)


@tool
def create_embeddings(docs: list[Document]):
    Chroma.from_documents(client=client, documents=docs, embedding=embeddings, collection_name="degiro_embeddings")

    return []
