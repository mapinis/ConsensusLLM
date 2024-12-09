"""
ConsensusLLM
A tool for two models to debate until they come to a consensus
main.py
12/9/2024
"""

import configparser
import os

from typedefs import Config


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


def print_intro(model_1: str, model_2: str):
    """
    Print the introduction
    """
    os.system("cls" if os.name == "nt" else "clear")
    width = os.get_terminal_size().columns

    print("-" * width + "\n")
    print(f"{{:^{width}}}".format("ConsensusLLM"))
    print(f"{{:^{width}}}".format("Using LLMs to reach a consensus"))
    print("\n" + "-" * width + "\n")

    print(f"Today's models are {model_1} and {model_2}.")
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

    # Print intro
    print_intro(cfg["MODEL1"], cfg["MODEL2"])

    # get topic from user
    topic = get_topic()

    # start conversation


if __name__ == "__main__":
    main()
