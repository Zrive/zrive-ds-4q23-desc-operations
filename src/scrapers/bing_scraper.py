import requests
import sys
import re
sys.path.append("..")
from credentials import keys
from bs4 import BeautifulSoup

subscription_key = keys.Bing_API_KEY
search_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def parser(texto_originario:str, Cat_url:bool=False) -> str:
    if not Cat_url:
        patron = re.compile(r"'snippet': '(.*?)',")
        coincidencias = re.findall(patron, texto_originario)
        resultado_final = '\n'.join(coincidencias)
        return resultado_final
    else:
        patron_url = re.compile(r"'displayUrl': '(.*?)',")
        urls_encontradas = re.findall(patron_url, texto_originario)
        urls_filtradas = [url for url in urls_encontradas if 'linkedin' not in url]
        return urls_filtradas

def bing_v1(query:str) -> str:
    """
    Realiza la solicitud a la API, sin contemplar muchos errores.
    Concatena los snippets de las 5 (default) primeras urls
    Parameters:
    - query (str): La palabra de busqueda.
    - num_pages (int): El numero de urls de las que se quieren extraer snippets.

    Returns:
    - str: el texto snippet de las num_pages urls
    """
    try:
        params = {"q": query,'textFormat':'HTML', 'count': 20, 'offset':0, 'responseFilter':'Webpages',}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        search_results_pages = str(search_results['webPages']['value'])
        if search_results_pages:
            return parser(texto_originario=search_results_pages)
        else:
            return None
    except Exception as e:
        print(f"Error en bing_v1 para {query}: {e}")
        return None

def bing_v2(query:str) -> str:
    """
    Realiza la solicitud a la API, sin contemplar muchos errores.
    Concatena los bodies de los htmls de las 3 (default) primeras urls
    Parameters:
    - query (str): La palabra de busqueda.
    - num_pages (int): El numero de urls de las que se quieren extraer snippets.

    Returns:
    - str: el texto texto completo de cada bodie de las num_pages urls
    """
    try:
        params = {"q": query,'textFormat':'HTML', 'count': 3, 'offset':0, 'responseFilter':'Webpages',}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        search_results_pages = str(search_results['webPages']['value'])
        if (search_results_pages is not None) and (parser(texto_originario=search_results_pages, Cat_url=True) is not None):
            urls = parser(texto_originario=search_results_pages, Cat_url=True)
            web_body_texts=[]
            for url in urls:
                try:
                    response = requests.get(url= url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text = soup.find('body').get_text().strip()
                    cleaned_text = ' '.join(text.split())
                    web_body_texts.append(cleaned_text)
                except Exception as e:
                    continue
            return '\n'.join(web_body_texts)
        else:
            return None
    except Exception as e:
        print(f"Error en bing_v2 para {query}: {e}")
        return None