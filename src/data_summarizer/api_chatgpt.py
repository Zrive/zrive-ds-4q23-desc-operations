from openai import OpenAI
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b70535e (fixed key exposure)
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

logger.level = logging.INFO
<<<<<<< HEAD

KEYS_PATH = "keys/open_ai.txt"


def chatgpt_call(text: str, company_name: str) -> str:
    api_key = _load_api_key()
=======


def chatgpt_call(text: str, company_name: str) -> str:
    api_key = "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"
>>>>>>> 685ba7e (Executable: Web_Scraper + Api_ChatGpt)
=======


def chatgpt_call(text: str, company_name: str) -> str:
    api_key = _load_api_key()
>>>>>>> b70535e (fixed key exposure)
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


<<<<<<< HEAD
<<<<<<< HEAD
def _load_api_key() -> str:
    try:
        with open(KEYS_PATH, "r") as file:
=======
def _load_api_key() -> str:
    file_path = Path(__file__).parent.parent.parent.resolve() / "keys.txt"
    try:
        with open(file_path, "r") as file:
            # Lee la primera línea del archivo, que debe contener la clave
>>>>>>> b70535e (fixed key exposure)
            file_line = file.readline().strip()
            pattern = r'"([^"]*)"'
            api_key = re.search(pattern, file_line).group(1)
            return api_key
    except FileNotFoundError:
        logger.warning(
<<<<<<< HEAD
            f"El archivo {KEYS_PATH} no se encontró. No se han conseguido las Keys de OPENAI"
=======
            f"El archivo {file_path} no se encontró. No se han conseguido las Keys de OPENAI"
>>>>>>> b70535e (fixed key exposure)
        )
        return None


<<<<<<< HEAD
=======
>>>>>>> 685ba7e (Executable: Web_Scraper + Api_ChatGpt)
=======
>>>>>>> b70535e (fixed key exposure)
def manage_name_company_errors(text: str) -> bool:
    if str(text).lower().find("html") != -1:
        return True

    return False
