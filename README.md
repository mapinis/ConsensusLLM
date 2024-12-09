# ConsensusLLM

Playing with LLMs having a conversation and reaching a consensus. Built in Python using Ollama.

## Setup

Prerequisites: Ollama, Python 3

### Python

Install the dependencies from `requirements.txt`:

```
pip install -r requirements.txt
```

### Ollama

This repository includes Ollama Modelfiles for the cases of liberal and conservative participants. But, any models can be used, as long as they have the correct system prompts. See the included Modelfiles for examples.

These models need to be loaded into Ollama for them to work, specifically with the exact names defined in `.cfg`.

For example:

```
ollama create LIBERAL -f ./models/liberal.modelfile
ollama create CONSERVATIVE -f ./models/conservative.modelfile
```

A script is included in the repository as `create_models.sh` to execute these commands for these specific models.

See Ollama documentation on Modelfiles if you want to explore creating your own models for this tool! Just remember to modify `.cfg`.

## Execution

First, make sure that Ollama is running:

```
ollama server
```

Verify that the "OLLAMA_HOST" variable matches that in `.cfg`. Then, just run the main Python script:

```
python3 main.py
```

Have fun!
