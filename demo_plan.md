# Demo Plan

## Present Degiro

## Present FAQ Assistant

https://www.degiro.com/uk/helpdesk/

## Create Embeddings

```shell
pf run create --flow create_embeddings --name create_embeddings --data batch_data_empty.jsonl
```

```shell
pf run visualize -n create_embeddings
```

## Run flow with no embeddings

```shell
pf flow test --flow no_embeddings_flow --inputs \
  "question=Can I open an account for my child ?"
```

## Run flow with keyword search

```shell
pf flow test --flow word_search_flow --inputs \
  'question=Can I open an account for my child ?'
```

```shell
pf flow test --flow word_search_flow --inputs \
  'question=I want to open an account for my child !'
```

```shell
pf flow test --flow word_search_flow --inputs \
  'question=It is possible to open an account for my kid. How do I do it ?'
```

## Run with embeddings

```shell
pf flow test --flow . --inputs \
  'question=Can I open an account for my child ?'
```

```shell
pf flow test --flow . --inputs \
  'question=I want to open an account for my child !'
```

```shell
pf flow test --flow . --inputs \
  'question=It is possible to open an account for my kid. How do I do it ?'
```

## Add Citation

```shell
pf flow test --flow . --inputs \
  'question=I want to open an account for my child !' \
  --variant='${chat.few_shots}'
```

## Evaluation Flows

- Metrics

  https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/concept-model-monitoring-generative-ai-evaluation-metrics?view=azureml-api-2

- Batch Data
- Visualize

```shell
./visualize.sh
```
