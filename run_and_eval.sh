#pf connection create -f openai_connection.yaml

variant=''
data_file='batch_data_big.jsonl'

if [ -n $1 ]; then
  variant=$1
fi

pf run delete -n first_run -y
pf run delete -n first_run_eval -y

if [ -z $variant ]; then
  echo "Running default variant"
  pf run create --flow . --data "$data_file" --stream --name first_run --column-mapping question='${data.question}'
else
  echo "Running $variant"
  pf run create --flow . --data "$data_file" --stream --name first_run --variant="\${chat.$variant}" --column-mapping question='${data.question}'
fi

pf run create --flow evaluation \
  --data "$data_file" \
  --column-mapping groundtruth_link='${data.link}' \
  --column-mapping question='${data.question}' \
  answer='${run.outputs.answer}' \
  --run first_run \
  --stream \
  --name first_run_eval

pf run show-details -n first_run_eval

echo "Final result"
pf run show-metrics -n first_run_eval

# pf run visualize -n "first_run,first_run_eval"
