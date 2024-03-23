import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import MarkdownHeaderTextSplitter

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5433")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_embeddings():
    file = open("faq.md", "r")
    markdown_text = file.read()
    file.close()

    headers_to_split_on = [
        ("#", "title"),
        ("##", "link")
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    docs = markdown_splitter.split_text(markdown_text)

    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name="embeddings2",
        connection_string=CONNECTION_STRING,
    )


def main():
    # create_embeddings()

    store = PGVector(
        collection_name="embeddings2",
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )

    result = store.similarity_search_with_score("DEGIRO is a wholesale, online stockbroker ?", k=2)
    print(f"Registered to db")
    for doc, score in result:
        print("-" * 80)
        print("Score: ", score)
        print(doc.page_content)
        print("-" * 80)


if __name__ == "__main__":
    main()
