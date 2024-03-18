import numpy as np
import psycopg2
from promptflow import tool
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer


def adapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))


register_adapter(np.ndarray, adapt_numpy_array)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')


@tool
def vector_search(question) -> list[str]:
    query = model.encode(question)
    query_string = '[' + ','.join(map(str, query)) + ']'

    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")

    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT title, link, chunk, 1-(embedding <=> %s) as cosine_similarity 
        FROM embeddings 
        ORDER BY cosine_similarity 
        DESC LIMIT 3;"""

    cur.execute(sql, (query_string,))
    result = cur.fetchmany(2)

    cur.close()
    conn.close()

    return result
