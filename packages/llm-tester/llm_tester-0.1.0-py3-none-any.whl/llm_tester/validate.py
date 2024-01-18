"""
Validation function
"""
from typing import Any

from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import get_openai_callback
from .conversation import Message
from .testing import TestUnit
from .misc import prompt, output_parser, print_error_message
import click
import logging


class Validator():
    """Validator class for validating a conversation flow
    Each validator is associated with a single LLM instance and a single conversation.
    """

    def __init__(
            self,
            test_unit: TestUnit,
            validator_model: str = "gpt-3.5-turbo"
        ) -> None:
        self._llm_to_validate = test_unit.llm
        self._conversation = test_unit.conversation
        self._model = validator_model
        self._validator_chain = self._build_chain()
        self._token_tracker = list()  # TODO: Store in a list? Or an ordered dict? For now, list of dicts...

    def validate_message(self, message: Message):
        """
        Validate a single message
        This should:
            - Check that the LLM response is correct
            - Keep track of the tokens used

        Parameters
        ----------
        message : Message
            Message to validate. Each message is an inputs / output pair, plus metadata on where to find the query.
        """
        # Get the actual response from the LLM & track token use
        with get_openai_callback() as cb:
            try:
                aux_chain = self._llm_to_validate | StrOutputParser()  # Force the output to be a string
                response = aux_chain.invoke(message.inputs)
            except Exception:
                logging.warn("The LLM's output cannot be forced to a string through OutputParser.\
                             Trying with str() function... If this fails, tweak the LLM's output parser.")
                response = str(self._llm_to_validate.invoke(message.inputs))
        
        # Check that the response is correct
        expected_response = message.output
        response_is_correct = self._validator_chain.invoke(
            {
                "prompt": message.get_query(),
                "expected_response": expected_response,
                "response": response,
            }
        )

        # Log token use
        self._token_tracker.append({
            "correct_response": response_is_correct,
            "prompt": message.inputs,
            "expected_response": expected_response,
            "response": response,
            "input_tokens": cb.prompt_tokens,
            "output_tokens": cb.completion_tokens,
            "total_cost": cb.total_cost,
        })

        return response_is_correct
    
    def _build_chain(self):
        """Build the LLM chain to validate the conversation"""
        global prompt, output_parser  # imported from misc.py

        validator_llm = ChatOpenAI(
            model=self._model
        )
        validator_chain = prompt | validator_llm | output_parser
        return validator_chain
    
    def validate_conversation(self):
        """Validate the entire conversation"""
        for message in self._conversation.messages:
            if self.validate_message(message):
                click.secho("-----\nTEST OK\n-----", fg="green")
            else:
                print_error_message(self._token_tracker[-1])

        return self._token_tracker

    @property
    def model(self):
        return self._model
