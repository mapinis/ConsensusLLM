"""
conversation.py
Handles the conversations between the LLMs
12/9/2024
"""

from typing import Callable
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
        "content": f"""MODERATOR: The topic of the conversation is: {topic}. \
                {models[start]} has won the coin toss, and may begin. \
                I hope the conversation is respectful and leads to a consensus.""",
    }

    # the conversations of both the models. Different because they have
    # different understandings of "assistant" and "user" roles.
    conversations = ([opening_message], [opening_message])

    # consensus values (both start at false)
    consensus = [False, False]

    # begin the loop
    current_model = start
    while not (consensus[0] and consensus[1]):

        print(f"{models[current_model]}:")
        latest_message = ""

        def handle_token(token: str):
            latest_message += token
            print(token, end="")

        ask_model(
            config["OLLAMA_URL"],
            models[current_model],
            conversations[current_model],
            handle_token,
        )

        # check for consensus
        if latest_message == "CONSENSUS":
            consensus[current_model] = True

        # model is done, append the messages
        conversations[current_model].append(
            {"role": "assistant", "content": latest_message}
        )

        other_model = (start + 1) // 2
        conversations[other_model].append(
            {"role": "user", "content": f"{models[current_model]}: {latest_message}"}
        )

        # set next model
        current_model = other_model

    # while loop over, consensus reached
    return conversations
