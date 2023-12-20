import logging
import re

logger = logging.getLogger(__name__)

logger.level = logging.INFO


def load_api_key(path: str) -> str:
    try:
        with open(path, "r") as file:
            file_line = file.readline().strip()
            pattern = r'"([^"]*)"'
            api_key = re.search(pattern, file_line).group(1)
            return api_key
    except FileNotFoundError:
        logger.warning(
            f"El archivo {path} no se encontró. No se han conseguido las Keys de OPENAI"
        )
        return None
