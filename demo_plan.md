# Demo Plan

## Present Degiro FAQ Assistant

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
pf flow test --flow flows/no_embeddings --inputs \
  "question=Can I open an account for my child ?"
```

## Run flow with keyword search

```shell
pf flow test --flow flows/keyword_search --inputs \
  'question=Can I open an account for my child ?'
```

```shell
pf flow test --flow flows/keyword_search --inputs \
  'question=I want to open an account for my child !'
```

```shell
pf flow test --flow flows/keyword_search --inputs \
  'question=It is possible to open an account for my kid. How do I do it ?'
```

## Run with embeddings

```shell
pf flow test --flow flows/default --inputs \
  'question=Can I open an account for my child ?'
```

```shell
pf flow test --flow flows/default --inputs \
  'question=I want to open an account for my child !'
```

```shell
pf flow test --flow flows/default --inputs \
  'question=It is possible to open an account for my kid. How do I do it ?'
```

## Add Citation

```shell
pf flow test --flow flows/default --inputs \
  'question=I want to open an account for my child !' \
  --variant='${chat.few_shots}'
```

## Chroma Version

```shell
pf flow test --flow ./flows/chroma --inputs \
  'question=I want to open an account for my child !' \
  --variant='${chat.default}'
```

```shell
pf flow test --flow ./flows/chroma --inputs \
  'question=I want to open an account for my child !' \
  --variant='${chat.few_shots}'
```

## Evaluation Flows

No keyword, no vector
```shell
./scripts/run_and_eval.sh "default_no_vec_no_word" "./flows/no_embeddings"
```

Keyword, no vector
```shell
./scripts/run_and_eval.sh "default_no_vec_word" "./flows/keyword_search"
```

Default flow with vector search AND word search
```shell
./scripts/run_and_eval.sh "default_vec_word" "./flows/default" chat.default
```

Default flow with vector search AND word search + few_shots
```shell
./scripts/run_and_eval.sh "few_shots_vec_word" "./flows/default" chat.few_shots
```

Chroma Version
```shell
./scripts/run_and_eval.sh "default_chroma" "./flows/chroma" chat.few_shots
```


- Metrics

  https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/concept-model-monitoring-generative-ai-evaluation-metrics?view=azureml-api-2

- Batch Data

- Visualize

```shell
./visualize.sh
```
