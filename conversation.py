"""
conversation.py
Handles the conversations between the LLMs
12/9/2024
"""

import json
from typing import Callable

import requests
from colorama import Fore

from typedefs import Config, Message


def ask_model(
    ollama_url: str,
    model: str,
    conversation: list[Message],
    handle_token: Callable[[str], None],
    handle_consensus: Callable[[str], None],
):
    """
    Ask Ollama for a chat completion for the given model and with the provided conversation.
    Response is streamed, handle_token function is used to handle token by token
    Provides a tool for the model to call for consensus with their understanding of what the consensus is
    This is then used to call handle_consensus
    """

    endpoint = ollama_url + "api/chat/"
    with requests.post(
        endpoint,
        json={
            "model": model,
            "messages": conversation,
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "propose_consensus",
                        "description": "Propose consensus with your understanding of the consensus after significant conversation working towards agreement.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "summary": {
                                    "type": "string",
                                    "description": "Short summary of your understanding of the consensus after long conversation.",
                                }
                            },
                            "required": ["summary"],
                        },
                    },
                }
            ],
        },
        stream=True,
    ) as response:

        if response.status_code != 200:
            raise ConnectionError(
                f"Unable to reach Ollama: {response.status_code}. Is Ollama running with the models installed?"
            )

        # run through the response stream
        for line in response.iter_lines(decode_unicode=True):
            if line:

                try:
                    data = json.loads(line)  # parse
                    print(data)
                    # check for consensus call
                    if "tool_calls" in data["message"]:
                        func = data["message"]["tool_calls"][0]["function"]
                        if func["name"] == "propose_consensus":
                            handle_consensus(func["arguments"]["summary"])

                    # append token if present
                    if data["message"]["content"]:
                        handle_token(data["message"]["content"])

                    if data["done"]:  # check if the stream is done
                        break

                except Exception as e:
                    print(f"Error parsing response: {line}.")
                    raise e


def run_conversation(
    config: Config, colors: list[str], topic: str, start: int
) -> tuple[list[Message]]:
    """
    Run the conversation between the two models
    Returns a tuple of messages between the models
    Requires the overall config, the topic, and the int (0 or 1) for the start model
    """

    # holds the models
    models = (config["MODEL1"], config["MODEL2"])

    opening_message: Message = {
        "role": "user",
        "content": f"MODERATOR: The topic of the conversation is: {topic}. {models[start]} has won the coin toss, and may begin. I hope the conversation is respectful and leads to a consensus.",
    }

    # the conversations of both the models. Different because they have
    # different understandings of "assistant" and "user" roles.
    conversations = ([opening_message], [opening_message])

    # consensus values (both start at false)
    consensus = [False, False]

    # begin the loop
    current_model = start
    while not consensus[0] or not consensus[1]:

        print(f"{models[current_model]}:")
        latest_message = ""
        other_model = (current_model + 1) % 2

        # set color
        print(colors[current_model])

        def handle_token(token: str):
            nonlocal latest_message
            latest_message += token
            print(token, end="", flush=True)

        def handle_consensus(summary: str):
            nonlocal consensus
            nonlocal conversations
            nonlocal other_model

            print(
                "\n",
                colors[current_model] + models[current_model] + Fore.RESET,
                "has proposed consensus with summary:",
                Fore.GREEN + summary + Fore.RESET,
            )

            consensus[current_model] = True
            conversations[other_model].append(
                {
                    "role": "user",
                    "content": f'MODERATOR: {models[current_model]} has proposed consensus with summary "{summary}". If you agree, use "propose_consensus" tool.',
                }
            )

        ask_model(
            config["OLLAMA_URL"],
            models[current_model],
            conversations[current_model],
            handle_token,
            handle_consensus,
        )

        print("\n" + Fore.RESET)  # newline and color reset

        # model is done, append the messages
        conversations[current_model].append(
            {"role": "assistant", "content": latest_message}
        )

        conversations[other_model].append(
            {"role": "user", "content": f"{models[current_model]}: {latest_message}"}
        )

        # set next model
        current_model = other_model

    # while loop over, consensus reached
    # TODO: summary of consensus screens, maybe return the summaries instead?
    return conversations
