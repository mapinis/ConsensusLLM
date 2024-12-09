"""
ConsensusLLM
A tool for two models to debate until they come to a consensus
main.py
12/9/2024
"""

import configparser
import os
import random

from typedefs import Config

from conversation import run_conversation


def get_config(path: str = "./.cfg") -> Config:
    """
    Get the information from config file at the provided path
    Path defaults to "./.cfg"
    Config requires OLLAMA_ENDPOINT, MODEL1, and MODEL2
    Raises errors if config not found or any of these params are not present
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"The config file {path} does not exist.")

    parser = configparser.ConfigParser()
    parser.read(path)

    cfg: Config = {
        "OLLAMA_URL": parser["default"].get("OLLAMA_URL"),
        "MODEL1": parser["default"].get("MODEL1"),
        "MODEL2": parser["default"].get("MODEL2"),
    }

    if any(v is None for v in cfg.values()):
        raise ValueError("Configuration requires OLLAMA_URL, MODEL1, and MODEL2 keys.")

    return cfg


def print_intro(models: list[str]):
    """
    Print the introduction
    """
    os.system("cls" if os.name == "nt" else "clear")
    width = os.get_terminal_size().columns

    print("-" * width + "\n")
    print(f"{{:^{width}}}".format("ConsensusLLM"))
    print(f"{{:^{width}}}".format("Using LLMs to reach a consensus"))
    print("\n" + "-" * width + "\n")

    print(f"Today's models are {models[0]} and {models[1]}.")
    print("You are the moderator and control the topic.\n")


def get_topic() -> str:
    """
    Get the topic of the conversation from the user
    Raises error if topic is empty
    """

    topic = input("Today's topic or question: ")

    if not (topic := topic.strip()):
        raise ValueError("Topic cannot be empty.")

    print()  # empty line for it to look good

    return topic


def main():
    """
    Main logic
    """
    # import config
    cfg = get_config()
    models = [cfg["MODEL1"], cfg["MODEL2"]]

    # Print intro
    print_intro(models)

    # get topic from user
    topic = get_topic()

    # coin toss
    start = random.randint(0, 1)
    print(f"By coin toss, {models[start]} goes first.\n")

    # start conversation
    run_conversation(cfg, topic, start)


if __name__ == "__main__":
    main()
