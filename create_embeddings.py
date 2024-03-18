import numpy as np
import psycopg2
from langchain_core.documents import Document
from promptflow import tool
from psycopg2.extensions import register_adapter, AsIs
from sentence_transformers import SentenceTransformer
import json


def adapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))


register_adapter(np.ndarray, adapt_numpy_array)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


@tool
def create_embeddings(chunks: list[Document]):
    embeddings = model.encode(list(map(lambda chunk: chunk.page_content, chunks)))

    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

    cur = conn.cursor()

    for document, embedding in zip(chunks, embeddings):
        embedding_text = '[' + ','.join(map(str, embedding)) + ']'

        cur.execute('INSERT INTO embeddings (title, link, chunk, embedding) VALUES (%s, %s, %s, %s)',
                    (document.metadata['title'],
                     document.metadata['link'],
                     document.page_content,
                     embedding_text))

    conn.commit()
    cur.close()
    conn.close()

    return []
