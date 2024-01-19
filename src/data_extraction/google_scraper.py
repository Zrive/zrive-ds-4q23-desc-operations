from src.data_extraction.utils import web_requests, text_parsers, keys

GOOGLE_API_KEY_PATH = "keys/google.txt"
SEARCH_ENGINE_ID_PATH = "keys/search_engine_id.txt"
API_URL = "https://www.googleapis.com/customsearch/v1"


def build_payload(API_KEY: str, cx: str, query: str, **params) -> dict[str:any]:
    """
    Builds the necessary payload to make a request to the Google Custom Search API.

    api_key : The API key for Google Custom Search.
    cx: The custom search identifier.
    query: The search string.
    """
    payload = {"key": API_KEY, "q": query, "cx": cx, "fileType": "html"}
    payload.update(params)
    return payload


def google(query: str) -> str:
    """
    This function performs a Google search and concatenates the 10 first snippets,
    which are short definitions for web pages.

    query: The search string.
    """
    try:
        api_usage = True
        api_key = keys.load_api_key(GOOGLE_API_KEY_PATH)
        search_engine_id = keys.load_api_key(SEARCH_ENGINE_ID_PATH)
        payload = build_payload(API_KEY=api_key, cx=search_engine_id, query=query)
        response = web_requests.request_with_cooloff(
            url=API_URL, api_usage=api_usage, params=payload
        )
        response_to_parse = str(response)
        return text_parsers.parser_request_response(original_text=response_to_parse)
    except Exception as e:
        print(f"Error en google para {query}: {e}")
        return f"ERROR!: {response.status_code}"
