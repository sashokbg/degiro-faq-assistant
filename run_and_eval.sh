#pf connection create -f openai_connection.yaml
export PF_BATCH_METHOD="spawn"

data_file='batch_data_big.jsonl'

name=$1
shift 1
variants="$@"

pf run delete -n "${name}" -y
pf run delete -n "${name}_eval_groundedness" -y
pf run delete -n "${name}_eval_relevance" -y

command="pf run create --flow . --data $data_file --stream --name $name --column-mapping question='\${data.question}'"

for variant in $variants
do
  command="$command --variant='\${$variant}'"
done

echo "Running command: $command"

eval "$command"

pf run create --flow ./evaluate_groundedness \
  --data "$data_file" \
  --column-mapping groundtruth_link='${data.link}' \
  --column-mapping question='${data.question}' \
  answer='${run.outputs.answer}' \
  --run $name \
  --stream \
  --name "${name}_eval_groundedness"

pf run create --flow evaluate_relevance \
  --data "$data_file" \
  --column-mapping ground_truth_content='${data.ground_truth_content}' \
  --column-mapping question='${data.question}' \
  answer='${run.outputs.answer}' \
  --run $name \
  --stream \
  --name "${name}_eval_relevance"

pf run show-details -n "${name}_eval_groundedness"
pf run show-details -n "${name}_eval_relevance"

echo "Groundedness score"
pf run show-metrics -n "${name}_eval_groundedness"
echo "Relevancy score"
pf run show-metrics -n "${name}_eval_relevance"

pf run visualize -n "${name},${name}_eval_groundedness,${name}_eval_relevance"
