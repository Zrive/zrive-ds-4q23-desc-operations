from duckduckgo_search import ddg
from scrapy.crawler import CrawlerProcess
from src.data_extraction.utils import web_requests, text_parsers


def _ddgo_query(query: str, numresults: int = 1) -> list:
    """
    This function performs a search on duckduckgo and returns the results.
    It uses the scrapy library to download the pages and extract the useful information.
    It extracts useful information from the pages using the readability library.

    query: the query to search for
    numresults: the number of results to return
    """
    results = ddg(query, max_results=numresults)
    urls = [result["href"] for result in results]
    urls = urls[:numresults]
    if urls:
        process = CrawlerProcess()
        process.crawl(web_requests.MySpider, urls)
        process.start()
        return web_requests.MySpider.results
    else:
        return f"ERROR!: 555 "


def duckduckgo_search(query: str, numresults: int = 1) -> str:
    """
    This function gather the duckduckgo search (via the Scrapy.Spider) and the get_result_lines()
    function to parse the results and perform a clean text.

    query: the query to search for
    numresults: the number of results to return
    """
    try:
        results = _ddgo_query(query=query, numresults=numresults)
        result_lines = text_parsers.get_result_lines(results=results, shorten=False)
        return "\n".join(result_lines)
    except Exception as e:
        print(f"Error for duckduckgo in {query}: {e}")
        return f"ERROR!: 555 "


def ddgo(query: str) -> str:
    """
    Calls Duck Duck Go Engine.

    query: the query to search for
    """
    return duckduckgo_search(query, numresults=1)
