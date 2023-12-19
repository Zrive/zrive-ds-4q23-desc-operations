from scrapy.crawler import CrawlerProcess
from credentials import keys
from utils import web_requests, text_parsers


SUBSCRIPTION_KEY = keys.BING_API_KEY
SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
HEADERS = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}

def _bing_query(query:str, numresults:int=1) -> dict:
    try:
        params = {"q": query,'textFormat':'HTML', 'count': numresults, 'offset':0, 'responseFilter':'Webpages'}
        response = web_requests.request_with_cooloff(url=SEARCH_URL, headers=HEADERS, params=params)
        return response
    except Exception as e:
        print(f"Error in bing for {query}: {e}")
        return None
    
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
        query_result = _bing_query(query=query)
        search_results_pages = str(query_result['webPages']['value'])
        if (search_results_pages is not None) and (text_parsers.parser_request_response(original_text=search_results_pages, Cat_url=True) is not None):
            urls = text_parsers.parser_request_response(original_text=search_results_pages, Cat_url=True)
            try:
                process = CrawlerProcess()
                process.crawl(web_requests.MySpider, urls)
                process.start()
                results = web_requests.MySpider.results
                result_lines = text_parsers.get_result_lines(results=results, shorten=False)
                return '\n'.join(result_lines)
            except Exception as e:
                return f'Exception ({e}) error'
        else:
            return None
    except Exception as e:
        print(f"Error in bing for {query}: {e}")
        return None