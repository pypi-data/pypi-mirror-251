"""
Module to hold reporting-related functions.
"""
import pandas as pd


def parse_report_dict(report_dict: dict) -> pd.DataFrame:
    """Parse a report dictionary into a DataFrame."""

    fields_to_keep = ['correct_response', 'input_tokens', 'output_tokens', 'total_cost']
    reduced_report_dict = [{k: v for k, v in r.items() if k in fields_to_keep} for r in report_dict]

    df = pd.DataFrame(reduced_report_dict)

    return df


def generate_summary_report(df: pd.DataFrame) -> dict:
    """Generate a summary report from a DataFrame."""

    summary_dict = dict()

    # Get total cost
    summary_dict["total_cost"] = df["total_cost"].sum()

    # Get total number of tokens used
    summary_dict["total_tokens"] = df["input_tokens"].sum() + df["output_tokens"].sum()

    # Get total number of correct responses
    summary_dict["total_correct_responses"] = df["correct_response"].sum()

    # Get total number of responses
    summary_dict["total_responses"] = len(df)

    # Get total accuracy
    summary_dict["accuracy"] = summary_dict["total_correct_responses"] / summary_dict["total_responses"]

    return summary_dict


def get_summary_from_report_dict(report_dict: dict) -> dict:
    """Get a summary report from a report dictionary."""

    df = parse_report_dict(report_dict)
    summary_df = generate_summary_report(df)

    return summary_df