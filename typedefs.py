"""
typedefs.py
Module to hold types
12/9/2024
"""

from typing import TypedDict, Literal


class Config(TypedDict):
    """
    Class for the configuration info
    """

    OLLAMA_URL: str
    MODEL1: str
    MODEL2: str


class Message(TypedDict):
    """
    Message type to be type-safe
    """

    role: Literal["system", "user", "assistant", "tool"]
    content: str
