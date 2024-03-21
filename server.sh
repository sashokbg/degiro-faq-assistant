python3 -m llama_cpp.server \
  --model ./models/mistral-7b-instruct-v0.2.Q5_K_S.gguf \
  --n_ctx 4096 \
  --n_gpu_layers 20 \
  --hf_pretrained_model_name_or_path mistralai/Mistral-7B-Instruct-v0.1
