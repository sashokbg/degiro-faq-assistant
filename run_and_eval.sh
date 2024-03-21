#pf connection create -f openai_connection.yaml

pf run delete -n first_run -y
pf run delete -n first_run_eval -y

pf run create --flow . --data batch_data.jsonl --stream --name first_run --column-mapping question='${data.question}'

pf run create --flow evaluation --data batch_data.jsonl --column-mapping groundtruth_link='${data.link}' --column-mapping question='${data.question}' answer='${run.outputs.answer}' --run first_run --stream --name first_run_eval

pf run show-metrics -n first_run_eval

# pf run visualize -n "first_run,first_run_eval"
