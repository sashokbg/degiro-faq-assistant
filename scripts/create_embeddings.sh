pf run delete -n create_embeddings -y
pf run create --flow flows/create_embeddings --stream --name create_embeddings --data batch_data_empty.jsonl
