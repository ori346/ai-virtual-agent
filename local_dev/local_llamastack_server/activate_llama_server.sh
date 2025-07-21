#!/bin/bash

MODEL_COUNT=$(ollama ps | tail -n +2 | wc -l)

# Check if any model is running
if [ "$MODEL_COUNT" -eq 0 ]; then
  echo "No models running. Starting llama3.2:3b-instruct-fp16..."
    # Load the model - and exit chat mode immediately
  echo "/bye" | ollama run llama3.2:3b-instruct-fp16 --keepalive 60m

  echo "Model is now loaded. Starting server..."
else
  echo "Model already running:"
  ollama ps
fi

podman run -it --rm --platform linux/amd64 \
    --name llama-server \
    --network host \
    -v ~/.llama:/~/.llama:z \
    -v ./run.yaml:/run.yaml:z \
    llamastack/distribution-ollama \
    --yaml-config /run.yaml \
    --port 8321
