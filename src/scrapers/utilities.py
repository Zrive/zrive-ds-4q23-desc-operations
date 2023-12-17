from readability import Document
import bs4
import logging
import random
import re
from typing import Dict
import time
import requests

logging.getLogger('scrapy').propagate = False
logging.getLogger('readability').propagate = False
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

    def parse(self, response):
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
    def parse_subpage(self, response):
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

def parser_request_response(texto_originario:str, Cat_url:bool=False) -> str:
    '''
    This function will use the bing search results as a text input and will
    return a list object with all URLs associated.
    '''
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

def readability(input_text):
    '''
    This function will use the readability library to extract the useful information from the text.
    Document is a class in the readability library. That library is (roughly) a python
    port of readability.js, which is a javascript library that is used by firefox to
    extract the useful information from a webpage. We will use the Document class to
    extract the useful information from the text.
    '''

    doc = Document(input_text)
    summary = doc.summary()
    # the summary is html, so we will use bs4 to extract the text
    soup = bs4.BeautifulSoup(summary, 'html.parser')
    summary_text = soup.get_text()
    return summary_text

def remove_duplicate_empty_lines(input_text):
    '''
    This function removes all duplicate empty lines from the lines
    '''
    lines = input_text.splitlines()
    fixed_lines = []
    for index, line in enumerate(lines):
        if line.strip() == '':
            if index != 0 and lines[index-1].strip() != '':
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)

def get_result_lines(results, shorten):
    '''
    This function will select only lines with >15 words (thus avoiding titles, headers and no usefull data)
    and if shorten is selected, will retunr the first 50 lines
    '''
    result_lines = []
    for result in results:
        result_lines.append(f"Title: {result['title']}")
        result_text = result['useful_text'].replace('\r\n', '')
        line = result_text.split('\n')
        filtered_lines = [linea for linea in line if len(linea.split()) > 15]
        if shorten:
            result_lines.append("Cleaned Text (shortened):")
            filtered_lines = filtered_lines['useful_text'].splitlines()[:50]
        filtered_text = '\n'.join(filtered_lines)
        result_lines.append(filtered_text)
        result_lines.append('\n')
    return result_lines