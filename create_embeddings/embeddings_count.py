import numpy as np
import psycopg2
from promptflow import tool
from psycopg2.extensions import register_adapter, AsIs
from sentence_transformers import SentenceTransformer


def adapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))


register_adapter(np.ndarray, adapt_numpy_array)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


@tool
def create_embeddings():
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM embeddings;")
    result = cur.fetchone()[0]

    print(f"Result is {result}")

    cur.close()
    conn.close()

    return result


