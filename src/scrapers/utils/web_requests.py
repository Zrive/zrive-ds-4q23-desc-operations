import bs4
import logging
import random
import time
import requests
from typing import Dict
from text_parsers import readability, remove_duplicate_empty_lines

logging.getLogger('scrapy').propagate = False
logging.getLogger('urllib3').propagate = False
logging.getLogger('httpcore').propagate = False

import scrapy
class MySpider(scrapy.Spider):
    '''
    This is the spider that will be used to crawl the webpages. We give this to the scrapy crawler.
    '''
    name = 'my_spider'
    results = []
    def __init__(self, start_url, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = start_url

    def parse(self, response:list[str]) -> dict:
        try:
            body_html = response.body.decode('utf-8')
            url = response.url
            soup = bs4.BeautifulSoup(body_html, 'html.parser')
            title = soup.title.string
            useful_text = readability(body_html)
            useful_text = remove_duplicate_empty_lines(useful_text)
            self.results.append({
                'url': url,
                'title': title,
                'useful_text': useful_text
            })
            links = response.css('a::attr(href)').getall()
            selected_links = random.sample(links, min(3, len(links)))
            for link in selected_links:
                yield scrapy.Request(url=link, callback=self.parse_subpage)
        except Exception as e:
            self.results.append({
                'url': '',
                'title': '',
                'useful_text': ''
            })
    def parse_subpage(self, response:list[str]) -> dict:
        try:
            body_html = response.body.decode('utf-8')
            url = response.url
            soup = bs4.BeautifulSoup(body_html, 'html.parser')
            title = soup.title.string
            useful_text = readability(body_html)
            useful_text = remove_duplicate_empty_lines(useful_text)
            self.results.append({
                'url': url,
                'title': title,
                'useful_text': useful_text
            })
        except Exception as e:
            self.results.append({
                'url': '',
                'title': '',
                'useful_text': ''
            })

logger = logging.getLogger(__name__)
def request_with_cooloff(
    session: requests.Session, url: str, headers: Dict[str, any], params: Dict[str, any], num_attempts: int=5
):
    """
    Call the url using requests. If the endpoint returns an error wait a cooloff
    period and try again, doubling the period each attempt up to a max num_attempts.
    """
    cooloff = 1
    for call_count in range(num_attempts):
        try:
            response = session.get(url, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            logger.info("API refused the connection")
            logger.warning(e)
            if call_count != (num_attempts - 1):
                time.sleep(cooloff)
                cooloff *= 2
                call_count += 1
                continue
            else:
                raise
        except requests.exceptions.HTTPError as e:
            logger.warning(e)
            if response.status_code == 404:
                raise
            logger.info(f"API return code {response.status_code} cooloff at {cooloff}")
            if call_count != (num_attempts - 1):
                time.sleep(cooloff)
                cooloff *= 2
                call_count += 1
                continue
            else:
                raise