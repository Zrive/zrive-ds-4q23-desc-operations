import requests
import pandas as pd
import re
import sys
sys.path.append("..")
from credentials import keys

API_KEY = keys.Google_API_KEY
Search_Engine_ID = keys.Google_Search_Engine_ID

def build_payload(API_KEY:str, cx:str, query:str, start:int=1, num:int=10, **params):
    """
    Construye el payload necesario para realizar la solicitud a la API de Google Custom Search.
    Parameters:
    - api_key (str): La clave de API de Google Custom Search.
    - cx (str): El identificador de búsqueda personalizado.
    - query (str): La cadena de búsqueda.
    Returns:
    - dict: El payload para la solicitud.
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

def make_request(url:str, payload:dict):
    """
    Realiza la solicitud a la API y maneja posibles errores.
    Parameters:
    - url (str): La URL de la API.
    - payload (dict): El payload de la solicitud.
    Returns:
    - dict: La respuesta de la API en formato JSON.
    """
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()  # Verifica si hay errores en la respuesta HTTP
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Tiempo de espera agotado: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error desconocido: {err}")

def google_v1(query:str, result_total:int=10) -> str:
    url = "https://www.googleapis.com/customsearch/v1"
    items =[]
    reminder = result_total
    if reminder > 0:
        pages = (result_total // 10) + 1
    else:
        pages = result_total // 10 
    for i in range(pages):
        if pages == i + 1 and reminder > 0:
            payload = build_payload(API_KEY=API_KEY, cx=Search_Engine_ID, query=query, start=(i+1)*10, num=reminder)
        else:
            payload = build_payload(API_KEY=API_KEY, cx=Search_Engine_ID, query=query, start=(i+1)*10)
        response = make_request(url=url, payload=payload)
        items.extend(response['items'])
    df = pd.json_normalize(items)
    joined_snippets = '\n'.join(map(str, df['snippet']))  
    return joined_snippets

def build_payload2(api_key, cx, q):
    payload = {
        'key': api_key,
        'cx': cx,
        'q': q,
        'fileType': 'html'
    }
    return payload

def google_v2(query:str) -> str:
    api_url = "https://www.googleapis.com/customsearch/v1"
    payload = build_payload2(api_key=API_KEY, cx=Search_Engine_ID, q=query)
    response_json = make_request(api_url, payload)
    if response_json and 'items' in response_json:
        first_result = response_json['items'][0]
        if 'snippet' in first_result:
            snippet_text = first_result['snippet']
            return snippet_text
    else:
        return None