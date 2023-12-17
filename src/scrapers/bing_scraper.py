import sys
sys.path.append("..")
from scrapy.crawler import CrawlerProcess
from utilities.web_requests import request_with_cooloff, MySpider
from utilities.text_parsers import parser_request_response, get_result_lines
from credentials import keys

subscription_key = keys.Bing_API_KEY
search_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

def bing(query:str) -> str:
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
        response = request_with_cooloff(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        search_results_pages = str(search_results['webPages']['value'])
        if (search_results_pages is not None) and (parser_request_response(texto_originario=search_results_pages, Cat_url=True) is not None):
            urls = parser_request_response(texto_originario=search_results_pages, Cat_url=True)
            try:
                process = CrawlerProcess()
                process.crawl(MySpider, urls[0])
                process.start()
                results = MySpider.results
                result_lines = get_result_lines(results, shorten=False)
                return result_lines
            except Exception as e:
                return f'Exception ({e}) error'
        else:
            return None
    except Exception as e:
        print(f"Error en bing_v2 para {query}: {e}")
        return None