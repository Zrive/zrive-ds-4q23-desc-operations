from openai import OpenAI
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

logger.level = logging.INFO

KEYS_PATH = "keys/open_ai.txt"


def chatgpt_call(text: str, company_name: str) -> str:
    api_key = _load_api_key()
    client = OpenAI(api_key=api_key)

    message_content = (
        f"""me haces un resumen de este html de la empresa {company_name}, 
                    en un maximo de 3 lineas que resuma a que se dedica dicha empresa por favor.
                      Respira profundamente y trabajo en este problema paso a paso:"""
        + text
    )
    # Enviar solicitud de completación de chat
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


def _load_api_key() -> str:
    try:
        with open(KEYS_PATH, "r") as file:
            file_line = file.readline().strip()
            pattern = r'"([^"]*)"'
            api_key = re.search(pattern, file_line).group(1)
            return api_key
    except FileNotFoundError:
        logger.warning(
            f"El archivo {KEYS_PATH} no se encontró. No se han conseguido las Keys de OPENAI"
        )
        return None


def manage_name_company_errors(text: str) -> bool:
    if str(text).lower().find("html") != -1:
        return True

    return False
