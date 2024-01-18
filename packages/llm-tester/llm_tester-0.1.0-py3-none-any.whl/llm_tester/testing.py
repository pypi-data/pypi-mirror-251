"""
Testing classes and functions for the LLM Tester
"""
from typing import Any
from .conversation import Conversation


class TestUnit():
    """Each test unit consists of a a conversation flow and an LLM instance."""

    def __init__(
            self,
            llm: Any,
            conversation: Conversation,
        ) -> None:
        self.llm = llm
        self.conversation = conversation

    


