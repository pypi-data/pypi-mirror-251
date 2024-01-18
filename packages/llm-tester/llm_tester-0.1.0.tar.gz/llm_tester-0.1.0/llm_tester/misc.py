"""
Miscellaneous functions for the LLM Tester.
"""
import os
import pprint
import click
from typing import List, Dict
from .testing import TestUnit
from langchain.prompts import PromptTemplate
from langchain.output_parsers.boolean import BooleanOutputParser
from langchain_core.output_parsers import StrOutputParser

PROMPT = """
You are a validator. Your task is to determine whether an answer is correct or not.
You will be given two messages: a response from an LLM and the expected response.
You must determine whether the response is correct or not based only on the expected response.
Do not base your assessment on any other information.
The response will not be necessarily be exactly the same as the expected response, 
but if its meaning is the same, then it is correct.
You must answer with a single word: True if the response is correct, False if it is not.

For context, here is the question: `{prompt}`

Response: `{response}`
Expected Response: `{expected_response}`

Based on the Expected Response, is the Response correct?
"""

prompt = PromptTemplate(
    template=PROMPT,
    input_variables=["prompt", "response", "expected_response"]
)
output_parser = StrOutputParser() | BooleanOutputParser(true_val="True", false_val="False")  # piping parsers together. Just like in the shell!



def tests_loader(tests_path: str) -> List[TestUnit]:
    """Load all test units from a given directory."""

    for filename in os.listdir(tests_path):
        if filename.endswith(".py"):
            with open(os.path.join(tests_path, filename), "r") as f:
                exec(f.read(), {} , locals())
    
    tests_list = [v for k, v in locals().items() if isinstance(v, TestUnit)]
    return tests_list


def print_error_message(log_dict: Dict):
    """print error message"""

    # print first lines
    click.secho("========\nTEST FAILED\n\n", fg="red")

    # print dictionary
    pp = pprint.PrettyPrinter(indent=4)
    for line in pp.pformat(log_dict).splitlines():
        click.secho(line, fg="red")

    # print separator
    click.secho("\n========", fg="red")
