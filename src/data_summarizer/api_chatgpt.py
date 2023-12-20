from openai import OpenAI
from pathlib import Path
from src.data_extraction.utils import keys
import logging
import re

logger = logging.getLogger(__name__)

logger.level = logging.INFO

OPENAI_KEYS_PATH = "keys/open_ai.txt"


def chatgpt_call(text: str, company_name: str) -> str:
    """
    This function performs OpenAI ChatGPT 3.5 summarization and warns if the
    link and the company name provided don't match. Parameters:

    text: The text we want to summarize.
    company_name: The company name.
    """
    api_key = keys.load_api_key(OPENAI_KEYS_PATH)
    client = OpenAI(api_key=api_key)

    message_content = (
        f"""me haces un resumen de este html de la empresa {company_name},
                    en un maximo de 3 lineas que resuma a que se dedica dicha empresa por favor.
                      Respira profundamente y trabajo en este problema paso a paso:"""
        + text
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role": "user", "content": message_content}],
        stream=False,
    )

    choices = response.choices
    if choices:
        first_choice = choices[0]
        message = first_choice.message
        content = message.content
        if manage_name_company_errors(content):
            return "COMPANY_NAME and URL not exact"
        return content
    else:
        return None


def manage_name_company_errors(text: str) -> bool:
    """
    Checks if text contians 'html' string

    text: The text we want to check.
    """
    if str(text).lower().find("html") != -1:
        return True

    return False
