from utils import web_requests, text_parsers
from credentials import keys

API_KEY = keys.GOOGLE_API_KEY
SEARCH_ENGINE_ID = keys.GOOGLE_SEARCH_ENGINE_ID
API_URL = "https://www.googleapis.com/customsearch/v1"


def build_payload(API_KEY: str, cx: str, query: str, start: int = 1, **params):
    """
    Builds the necessary payload to make a request to the Google Custom Search API.
    Parameters:
    - api_key (str): The API key for Google Custom Search.
    - cx (str): The custom search identifier.
    - query (str): The search string.
    Returns:
    - dict: The payload for the request.
    """
    payload = {"key": API_KEY, "q": query, "cx": cx, "fileType": "html"}
    payload.update(params)
    return payload


def google(query: str) -> str:
    """
    This function will perform a Google search and concatenate the 10 first snippets
    which are short definitions for a web page.
    """
    try:
        payload = build_payload(API_KEY=API_KEY, cx=SEARCH_ENGINE_ID, query=query)
        response_json = web_requests.request_with_cooloff(
            url=API_URL, headers={}, params=payload
        )
        response_to_parse = str(response_json)
        return text_parsers.parser_request_response(original_text=response_to_parse)
    except Exception as e:
        print(f"Error en google para {query}: {e}")
        return None
