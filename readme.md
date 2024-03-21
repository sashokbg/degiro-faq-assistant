https://python.langchain.com/docs/modules/data_connection/document_transformers/markdown_header_metadata

https://api.python.langchain.com/en/latest/documents/langchain_core.documents.base.Document.html#langchain_core.documents.base.Document

https://www.sbert.net/

https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

https://python.langchain.com/docs/integrations/vectorstores/pgvector

https://tembo.io/blog/pgvector-and-embedding-solutions-with-postgres

https://www.psycopg.org/docs/usage.html

https://llama-cpp-python.readthedocs.io/en/latest/server/

## using pf

Test a single node
```shell
pf flow test --flow . --node create_embeddings
```

Test entire flow with input
```shell
pf flow test --flow . --inputs question='Can I open an account from Bulgaria ?'
```

Create a new batch run
```shell
pf run create --flow . --data batch_data.jsonl --stream --name third_run --column-mapping question='${data.question}'
```

pf connection create -f openai_connection.yaml

# Pip freeze 

'''
pip freeze > requirements.txt
'''
