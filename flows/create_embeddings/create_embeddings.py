import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from promptflow.core import tool

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5433")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


@tool
def create_embeddings(docs: list[Document]):
    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name="embeddings",
        connection_string=CONNECTION_STRING,
    )

    return []
