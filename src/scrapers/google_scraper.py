import sys
sys.path.append("..")
from utils.web_requests import request_with_cooloff
from utils.text_parsers import parser_request_response 
from credentials import keys


API_KEY = keys.Google_API_KEY
Search_Engine_ID = keys.Google_Search_Engine_ID

def build_payload(API_KEY:str, cx:str, query:str, start:int=1, num:int=10, **params):
    """
    Builds the necessary payload to make a request to the Google Custom Search API.
    Parameters:
    - api_key (str): The API key for Google Custom Search.
    - cx (str): The custom search identifier.
    - query (str): The search string.
    Returns:
    - dict: The payload for the request.
    """
    payload = {
        'key': API_KEY,
        'q':query,
        'cx': cx,
        'num': num,
        'fileType': 'html'
    }
    payload.update(params)
    return payload

def google(query:str) -> str:
    '''
    This function will perform a Google search and concatenate the 10 first snippets
    which are short definitions for a web page.
    '''
    try:
        api_url = "https://www.googleapis.com/customsearch/v1"
        payload = build_payload(api_key=API_KEY, cx=Search_Engine_ID, q=query)
        response_json = request_with_cooloff(url=api_url, params=payload)
        response_to_parse = str(response_json)
        return parser_request_response(texto_originario=response_to_parse)
    except Exception as e:
        print(f"Error en google_v2 para {query}: {e}")
        return None