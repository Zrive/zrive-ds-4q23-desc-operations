import requests
import sys
sys.path.append("..")
from credentials import keys
from bs4 import BeautifulSoup

subscription_key = keys.Bing_API_KEY
search_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def bing_v1(query:str, num_pages:int=5) -> str:
    """
    Realiza la solicitud a la API, sin contemplar muchos errores.
    Concatena los snippets de las 5 (default) primeras urls
    Parameters:
    - query (str): La palabra de busqueda.
    - num_pages (int): El numero de urls de las que se quieren extraer snippets.

    Returns:
    - str: el texto snippet de las num_pages urls
    """
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    pages = search_results['webPages']
    results = pages['value']
    snipets = []
    for result in results[:num_pages]:
        snipets.append(result['snippet'])
    return '\n'.join(snipets)

def bing_v2(query:str, num_pages:int=3) -> str:
    """
    Realiza la solicitud a la API, sin contemplar muchos errores.
    Concatena los bodies de los htmls de las 3 (default) primeras urls
    Parameters:
    - query (str): La palabra de busqueda.
    - num_pages (int): El numero de urls de las que se quieren extraer snippets.

    Returns:
    - str: el texto texto completo de cada bodie de las num_pages urls
    """
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    pages = search_results['webPages']
    results = pages['value']
    web_body_texts=[]
    for result in results[:num_pages]:
        response = requests.get(url= result['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.find('body').get_text().strip()
        cleaned_text = ' '.join(text.split())
        web_body_texts.append(cleaned_text)
    return '\n'.join(web_body_texts)