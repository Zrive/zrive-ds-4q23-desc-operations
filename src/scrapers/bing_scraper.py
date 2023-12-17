import sys
sys.path.append("..")
from scrapy.crawler import CrawlerProcess
from utils.web_requests import request_with_cooloff, MySpider
from utils.text_parsers import parser_request_response, get_result_lines
from credentials import keys

SUBSCRIPTION_KEY = keys.BING_API_KEY
search_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}

def bing(query:str) -> str:
    """
    Makes a request to the API, without handling many errors.
    Concatenates the bodies of the HTMLs from the first 3 (default) URLs.
    Parameters:
    - query (str): The search term.
    - num_pages (int): The number of URLs from which snippets are to be extracted.

    Returns:
    - str: The complete text of each body from the num_pages URLs.
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