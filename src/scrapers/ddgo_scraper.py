from duckduckgo_search import ddg
from scrapy.crawler import CrawlerProcess
from utils.web_requests import MySpider
from utils.text_parsers import get_result_lines
def ddgo_query(query:str, numresults:int=2) -> dict:
    '''
    This function performs a search on duckduckgo and returns the results.
    It uses the scrapy library to download the pages and extract the useful information.
    It extracts useful information from the pages using either the readability library 
    or openai, depending on the value of clean_with_llm.
    
    query: the query to search for
    numresults: the number of results to return
    clean_with_llm: if True, use openai to clean the text. If False, use readability.
    loglevel: the log level to use, a string. Can be DEBUG, INFO, WARNING, ERROR, or CRITICAL.
    '''

    results = ddg(query, max_results=numresults)
    urls = [result['href'] for result in results]
    urls = urls[:numresults]
    if urls:
        process = CrawlerProcess()
        process.crawl(MySpider, urls[0])
        process.start()
        return MySpider.results
    else:
        return None

def duckduckgo_search(query:str, numresults:int=3) -> str:
    '''
    This function gather the duckduckgo search (via the Scrapy.Spider) and the get_result_lines()
    function to parse the results and perform a clean text.
    '''
    try:
        results = ddgo_query(query, numresults)
        result_lines = get_result_lines(results, shorten=False)
        return '\n'.join(result_lines)
    except Exception as e:
        print(f"Error en duckduckgo para {query}: {e}")
        return None