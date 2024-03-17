from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

query = model.encode("I cannot log in")
query_string = '[' + ','.join(map(str, query)) + ']'
print(f"Query vector: {query_string}")
