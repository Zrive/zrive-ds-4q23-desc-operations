import re


def parse_error(error: str) -> str:
    """
    In this function, errors are captured to match them with the error legend
    established in the main function, enabling the generation of statistics on errors.

    error: the error as text
    """
    status_code_pattern = re.compile(r"\b(\d{3})\b")
    match = status_code_pattern.search(error)

    if match:
        http_status_code = match.group(1)
        return http_status_code
    else:
        return "Error mal implementado"
