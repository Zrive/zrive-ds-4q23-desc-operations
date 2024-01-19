import requests
from bs4 import BeautifulSoup
import html2text
import logging
import re
import time
from src.data_extraction.utils.web_requests import request_with_cooloff

logger = logging.getLogger(__name__)

logger.level = logging.INFO


def request_html(url: str) -> BeautifulSoup:
    """
    This function collapses the company URL to the HTTPS protocol for performing a request.

    url: The company's URL.
    """
    url_base = "https://"
    url_complete = url_base + str(url)
    api_usage = False
    html = request_with_cooloff(url = url_complete, api_usage=api_usage)
    return html


def clean_html_text(html: BeautifulSoup) -> str:
    """
    This function cleans an HTML result using the HTML2Text() external library with
    the purpose of extracting the web body text.

    html: A web HTML as a BeautifulSoup (bs4) object.
    """
    if str(html).lower().find("error!:") != -1:
        return None
    else:
        cleaner = html2text.HTML2Text()
        cleaner.ignore_links = True
        text = cleaner.handle(html.prettify())
        only_words = re.sub(r"[^a-zA-Z\s]", "", text)
        text_no_links = re.sub(r"\b(.*image.*|.*png.*|.*http.*)\b", "", only_words)
        return text_no_links
