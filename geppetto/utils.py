import json
import logging
import os
import re
from typing import List


def load_json(file_name):
    """Load information from a JSON file."""
    try:
        with open(os.path.join("config", file_name), "r") as file:
            json_file = json.load(file)
            logging.info("%s:%s" % (file_name, json_file))
            return json_file
    except FileNotFoundError:
        logging.error("%s file not found." % file_name)
    except json.JSONDecodeError:
        logging.error("Error decoding %s file." % file_name)
    return {}


def is_image_data(data):
    return isinstance(data, bytes)


def lower_string_list(list_to_process: List[str]):
    return [element.lower() for element in list_to_process]


VERSION = os.getenv("GEPPETTO_VERSION")


def convert_openai_markdown_to_slack(text, model, version=VERSION):
    """
    Converts markdown text from the OpenAI format to Slack's "mrkdwn" format.

    This function handles:
    - Bold text conversion from double asterisks (**text**) to single asterisks (*text*).
    - Italics remain unchanged as they use underscores (_text_) in both formats.
    - Links are transformed from [text](url) to <url|text>.
    - Bullet points are converted from hyphens (-) to Slack-friendly bullet points (•).
    - Code blocks with triple backticks remain unchanged.
    - Strikethrough conversion from double tildes (~~text~~) to single tildes (~text~).

    Args:
        text (str): The markdown text to be converted.
        model (str): The LLM (model) used.
        version (str): The version of Geppetto.

    Returns:
        str: The markdown text formatted for Slack.
    """
    formatted_text = text.replace("* ", "- ")
    formatted_text = formatted_text.replace("**", "*")
    formatted_text = formatted_text.replace("__", "_")
    formatted_text = formatted_text.replace("- ", "• ")
    formatted_text = re.sub(r"\[(.*?)\]\((.*?)\)", r"<\2|\1>", formatted_text)
    formatted_text += (
        f"\n\n_(Geppetto v{version} Source: {model})_"
    )

    # Code blocks and italics remain unchanged but can be explicitly formatted
    # if necessary
    return formatted_text
