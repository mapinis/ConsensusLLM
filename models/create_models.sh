#!/bin/bash

# create the models in ollama
ollama create LIBERAL -f ./liberal.modelfile
ollama create CONSERVATIVE -f ./conservative.modelfile