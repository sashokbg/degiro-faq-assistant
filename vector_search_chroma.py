import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from promptflow.core import tool

model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs=model_kwargs)

client = chromadb.HttpClient(settings=Settings(allow_reset=True), host='localhost', port=8000)


@tool
def vector_search(question, k_top) -> list[dict]:
    print(f"Searching vectors for Q: {question}")
    db = Chroma(client=client, embedding_function=embeddings, collection_name="degiro_embeddings")
    docs = db.similarity_search_with_score(question, k=k_top)

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


if __name__ == "__main__":
    vector_search("Can I buy a part of a share ?", 5)
