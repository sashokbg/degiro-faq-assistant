CREATE EXTENSION vector;

CREATE TABLE embeddings (id bigserial PRIMARY KEY, title text, link text, chunk text, embedding vector(384));
