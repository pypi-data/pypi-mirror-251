"""
CLI tool for testing the LLM.
The tool must:
- Load the .env file
- Go through the files in the llm_tests directory and retrieve all TestUnit objects
- Run each TestUnit with the Validator
- Print & log the results
"""
import click
import logging
import json
from dotenv import load_dotenv
from datetime import datetime
from .misc import tests_loader
from .validate import Validator
from .reporting import get_summary_from_report_dict


@click.command()
@click.option("--tests-path", default="./llm_tests/", help="Path to the directory containing the tests.")
@click.option("--env", default=".env", help="Path to the .env file.")
@click.option("--validator-model", default="gpt-3.5-turbo", help="Model to use to validate responses.")
@click.option('--verbosity',
              type=click.Choice(['WARN', 'DEBUG'], case_sensitive=False),
              default='WARN',
              help='Verbosity level. WARN by default. Must be one of: WARN, DEBUG.'
            )
def run_tests(
    tests_path: str = "./llm_tests/",
    env: str = ".env",
    validator_model: str = "gpt-3.5-turbo",
    verbosity: str = "WARN",
    ) -> None:
    """Run all tests in the given directory."""
    now = datetime.now()  # get time once per run

    # Set logging level
    if verbosity == "WARN":
        logging.basicConfig(level=logging.WARN)
    elif verbosity == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)

    # Load .env
    env_loaded = load_dotenv(env)
    if not env_loaded:
        logging.warn(f"Could not load .env from {env}.")

    # Load tests
    tests = tests_loader(tests_path)
    logging.info(f"Loaded {len(tests)} tests from {tests_path}")

    # Run tests
    report_accumulator = list()

    for test in tests:
        validator = Validator(test, validator_model)
        report_dict = validator.validate_conversation()
        # generate summary report
        summary = get_summary_from_report_dict(report_dict)
        click.echo(f"Conversation metrics: {summary}\n\n")

        # log full output to file
        with open(f"{tests_path}/output_{now.strftime('%y-%m-%d_%H:%M')}.log", "a") as f:
            f.write("\n")
            f.write(json.dumps(report_dict, indent=4))
            f.write(f"\nConversation metrics:\n{summary}\n")
            
        # save conversation-level report to variable
        for d in report_dict:
            report_accumulator.append(d)

    # generate total summary report
    total_summary = get_summary_from_report_dict(report_accumulator)
    click.echo(f"\n\nTotal metrics: {total_summary}")
    # log full output to file
    with open(f"{tests_path}/output_{now.strftime('%y-%m-%d_%H:%M')}.log", "a") as f:
        f.write(f"\n\nTotal metrics:\n{total_summary}\n")
        f.write("\n--------------------------------\n")
