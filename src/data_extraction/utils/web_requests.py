import scrapy
import json
import bs4
import logging
import random
import time
import requests
from typing import Dict
from src.data_extraction.utils.text_parsers import (
    readability,
    remove_duplicate_empty_lines,
)

logging.getLogger("scrapy").propagate = False
logging.getLogger("urllib3").propagate = False
logging.getLogger("httpcore").propagate = False


class MySpider(scrapy.Spider):
    """
    This is the spider that will be used to crawl the webpages. It is provided to the Scrapy crawler.

    start_urls: List of the starting URLs to scrap
    """

    name = "myspider"
    start_urls = None
    results = []

    def __init__(self, start_urls, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            body_html = response.body.decode("utf-8")
            url = response.url
            soup = bs4.BeautifulSoup(body_html, "html.parser")
            title = soup.title.string
            text = soup.get_text()
            text = remove_duplicate_empty_lines(text)
            useful_text = readability(body_html)
            useful_text = remove_duplicate_empty_lines(useful_text)
            self.results.append(
                {"url": url, "title": title, "text": text, "useful_text": useful_text}
            )
            links = response.css("a::attr(href)").getall()
            selected_links = random.sample(links, min(3, len(links)))
            for link in selected_links:
                yield scrapy.Request(url=link, callback=self.parse_subpage)
        except Exception as e:
            self.results.append({"url": "", "title": "", "useful_text": ""})

    def parse_subpage(self, response: list[str]) -> dict:
        try:
            body_html = response.body.decode("utf-8")
            url = response.url
            soup = bs4.BeautifulSoup(body_html, "html.parser")
            title = soup.title.string
            useful_text = readability(input_text=body_html)
            useful_text = remove_duplicate_empty_lines(input_text=useful_text)
            self.results.append(
                {"url": url, "title": title, "useful_text": useful_text}
            )
        except Exception as e:
            self.results.append({"url": "", "title": "", "useful_text": ""})


def _request_with_cooloff(
    url: str, headers: Dict[str, any], params: Dict[str, any], num_attempts: int
):
    """
    Call the url using requests. If the endpoint returns an error wait a cooloff
    period and try again, doubling the period each attempt up to a max num_attempts.

    url: the URL to call
    headers: request headers
    params: request parameters
    num_attempts: The number of attemps before canceling conexion
    """
    cooloff = 1
    for call_count in range(num_attempts):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=360)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            if call_count != (num_attempts - 1):
                time.sleep(cooloff)
                cooloff *= 2
                call_count += 1
                continue
            else:
                raise
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise
            if call_count != (num_attempts - 1):
                time.sleep(cooloff)
                cooloff *= 2
                call_count += 1
                continue
            else:
                raise
        return response


def request_with_cooloff(
    url: str, headers: Dict[str, any], params: Dict[str, any], num_attempts: int = 3
):
    """
    Call the url using requests. If the endpoint returns an error wait a cooloff
    period and try again, doubling the period each attempt up to a max num_attempts.

    url: the URL to call
    headers: request headers
    params: request parameters
    num_attempts: The number of attemps before canceling conexion
    """
    return _request_with_cooloff(url, headers, params, num_attempts)
