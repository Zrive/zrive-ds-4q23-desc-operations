import re


def parse_error(error: str) -> str:
    status_code_pattern = re.compile(r"\b(\d{3})\b")
    match = status_code_pattern.search(error)

    if match:
        http_status_code = match.group(1)
        return http_status_code
    else:
        return "Error mal implementado"
