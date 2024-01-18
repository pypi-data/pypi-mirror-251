"""
Script to hold the Conversation and Message classes
"""
from typing import List, Dict, Any, Optional


class Message():
    """Each message is an inputs / output pair, plus metadata on where to find the query.
    Parameters
    ----------
    inputs: All inputs needed for the LLM to generate the output. Must be a dict.
        If you are not sure, the default is {"input": "your question"}

    output: Expected response from the LLM for the given inputs. Must be a string.

    query_key: Key corresponding to the input query or question posed to the LLM. Default: "input".
    """

    def __init__(self, inputs: Dict[str, Any], output: str, query_key: str = "input") -> None:
        self._inputs = inputs
        self._output = output
        self._query_key = query_key

    @property
    def inputs(self):
        return self._inputs
    
    @property
    def output(self):
        return self._output
    
    @property
    def query_key(self):
        return self._query_key
    
    @query_key.setter
    def query_key(self, new_value):
        self._query_key = new_value
    
    def get_query(self) -> str:
        return self._inputs.get(self._query_key, "Question not available. Proceed with answer validation.")

    # TODO: accept both string and dict as inputs. If string, then query_key is not needed. (single input)


class Conversation():
    """List of messages to validate.
    This is emulates a conversation flow"""
    def __init__(self, messages: List[Message], query_key: Optional[str] = None) -> None:
        self.messages = messages
        self._query_key = query_key
        if query_key:
            self._update_messages_query_key()

    @property
    def query_key(self):
        return self._query_key
    
    def _update_messages_query_key(self):
        for message in self.messages:
            message.query_key = self._query_key


