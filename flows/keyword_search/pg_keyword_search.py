from promptflow.core import tool

import psycopg2
from psycopg2.extras import RealDictCursor


@tool
def keyword_search(question, k_top) -> list[dict]:
    conn = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=postgres")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT ts_rank_cd(to_tsvector((cmetadata -> 'title') || '' || document),
                          plainto_tsquery('english', %(question)s), 32 /* rank/(rank+1) */) as rank,
               *
        FROM langchain_pg_embedding
        WHERE to_tsvector((cmetadata -> 'title') || '' || document) @@
              plainto_tsquery('english', %(question)s)
        ORDER BY rank DESC
        LIMIT 3
        ;"""

    cur.execute(sql, {'question': question})
    docs = cur.fetchmany(3)

    cur.close()
    conn.close()

    print(f"Found {len(docs)} docs")

    result = []

    for doc in docs:
        result.append({
            "score": doc['rank'],
            "content": doc['document'],
            "title": doc['cmetadata']['title'],
            "link": doc['cmetadata']['link']
        })

    print(f"Found {result}")
    return result


if __name__ == "__main__":
    keyword_search("Can I buy a part of a share ?", 5)
