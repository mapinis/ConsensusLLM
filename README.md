# ConsensusLLM

Playing with LLMs having a conversation and reaching a consensus. Built in Python using Ollama.

## Setup

This repository includes Ollama Modelfiles for the cases of liberal and conservative participants. But, any models can be used, as long as they have the correct system prompts. See the included Modelfiles for examples.

These models need to be loaded into Ollama for them to work, specifically with the exact names defined in `.cfg`.

For example:

```
ollama create LIBERAL -f ./liberal.modelfile
ollama create CONSERVATIVE -f ./conservative.modelfile
```
