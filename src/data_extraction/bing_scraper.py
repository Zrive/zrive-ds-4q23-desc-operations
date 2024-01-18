from scrapy.crawler import CrawlerProcess
from src.data_extraction.utils import web_requests, text_parsers, keys


SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
BING_KEYS_PATH = "keys/bing.txt"


def _bing_query(query: str, numresults: int = 1) -> dict:
    """
    Provides necessary Bing API parameters and headers to perform a request_with_cooloff() request.

    query: The word to search on the engines.
    numresults: The number of links to display in the query.
    """
    try:
        api_usage = True
        params = {
            "q": query,
            "textFormat": "HTML",
            "count": numresults,
            "offset": 0,
            "responseFilter": "Webpages",
        }
        api_key = keys.load_api_key(BING_KEYS_PATH)
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response = web_requests.request_with_cooloff(
            url=SEARCH_URL, api_usage = api_usage, headers=headers, params=params
        )
        return response
    except Exception as e:
        print(f"Error in bing for {query}: {e}")
        return f"ERROR!: {response.status_code}"


def bing(query: str) -> str:
    """
    Makes a request to the API, without handling many errors.
    Concatenates the bodies of the HTMLs from the first 3 (default) URLs.

    query: The search term.
    num_pages: The number of URLs from which snippets are to be extracted.
    """
    try:
        query_result = _bing_query(query=query)
        if str(query_result).lower().find("error!:") != -1:
            return query_result
        search_results_pages = str(query_result["webPages"]["value"])
        if (search_results_pages is not None) and (
            text_parsers.parser_request_response(
                original_text=search_results_pages, Cat_url=True
            )
            is not None
        ):
            urls = text_parsers.parser_request_response(
                original_text=search_results_pages, Cat_url=True
            )
            try:
                process = CrawlerProcess()
                process.crawl(web_requests.MySpider, urls)
                process.start()
                results = web_requests.MySpider.results
                result_lines = text_parsers.get_result_lines(
                    results=results, shorten=False
                )
                return "\n".join(result_lines)
            except Exception as e:
                return f"Exception ({e}) error"
        else:
            return None
    except Exception as e:
        print(f"Error in bing for {query}: {e}")
        return None
