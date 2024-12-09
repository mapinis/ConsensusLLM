"""
conversation.py
Handles the conversations between the LLMs
12/9/2024
"""

import json
from typing import Callable

import requests
from typedefs import Config, Message


def ask_model(
    ollama_url: str,
    model: str,
    conversation: list[Message],
    handle_token: Callable[[str], None],
):
    """
    Ask Ollama for a chat completion for the given model and with the provided conversation.
    Response is streamed to handle_token function is used to handle token by token
    """

    endpoint = ollama_url + "api/chat/"
    with requests.post(
        endpoint,
        json={
            "model": model,
            "messages": conversation,
        },
        stream=True,
    ) as response:

        if response.status_code != 200:
            raise ConnectionError(
                f"Unable to reach Ollama: {response.status_code}. Is Ollama running with the models installed?"
            )

        # run through the response stream
        for line in response.iter_lines(decode_unicode=True, chunk_size=8):
            if line:

                try:
                    data = json.loads(line)  # parse

                    if data["done"]:  # check if the stream is done
                        break

                    # else append
                    handle_token(
                        data["message"]["content"]
                    )  # held in "response" for whatever reason

                except Exception as e:
                    print(f"Error parsing response: {line}.")
                    raise e


def run_conversation(config: Config, topic: str, start: int) -> tuple[list[Message]]:
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
        # for _ in range(3):

        print(f"{models[current_model]}:")
        latest_message = ""

        def handle_token(token: str):
            nonlocal latest_message
            latest_message += token
            print(token, end="")

        ask_model(
            config["OLLAMA_URL"],
            models[current_model],
            conversations[current_model],
            handle_token,
        )

        print("\n")

        # check for consensus
        if latest_message[-9:] == "CONSENSUS" or latest_message[-10:] == "CONSENSUS.":
            consensus[current_model] = True

        # model is done, append the messages
        conversations[current_model].append(
            {"role": "assistant", "content": latest_message}
        )

        other_model = (current_model + 1) % 2
        conversations[other_model].append(
            {"role": "user", "content": f"{models[current_model]}: {latest_message}"}
        )

        # set next model
        current_model = other_model
        # print(current_model, other_model, conversations)

    # while loop over, consensus reached
    return conversations
