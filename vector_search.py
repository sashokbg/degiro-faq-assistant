import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from promptflow import tool

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5433")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs=model_kwargs)


@tool
def vector_search(question) -> list[dict]:
    print(f"Searching vectors for Q: {question}")

    store = PGVector(
        collection_name="embeddings",
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )

    docs = store.similarity_search_with_score(question, k=2)

    print(f"Found {len(docs)} docs")

    result = []

    for doc, score in docs:
        result.append({
            "score": round(1 - score, 2),
            "content": doc.page_content,
            "title": doc.metadata['title'],
            "link": doc.metadata['link']
        })

    return result
