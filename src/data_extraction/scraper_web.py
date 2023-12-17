import requests
from bs4 import BeautifulSoup
import html2text
import logging
import re
import time

logger = logging.getLogger(__name__)

logger.level = logging.INFO


def request_html(url: str) -> BeautifulSoup:
    url_base = "https://"
    url_complete = url_base + url
    html = html_request_with_cooloff(url_complete)
    return html


def html_request_with_cooloff(url: str, num_attempts: int = 2):
    """
    Call the url using requests. If the endpoint returns an error wait a cooloff
    period and try again, doubling the period each attempt up to a max num_attempts.
    """
    cooloff = 1

    for call_count in range(num_attempts):
        try:
            response = requests.get(url)
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
                return "error!:"

        except requests.exceptions.HTTPError as e:
            logger.warning(e)
            if response.status_code == 404:
                return "error!:"

            logger.info(f"API return code {response.status_code} cooloff at {cooloff}")
            if call_count != (num_attempts - 1):
                time.sleep(cooloff)
                cooloff *= 2
                call_count += 1
                continue
            else:
                return "error!:"

        soup = BeautifulSoup(response.text, "html.parser")
        return soup


def clean_html_text(html: BeautifulSoup) -> str:
    if str(html).lower().find("error!:") != -1:
        return None
    else:
        cleaner = html2text.HTML2Text()
        cleaner.ignore_links = True
        text = cleaner.handle(html.prettify())
        only_words = re.sub(r"[^a-zA-Z\s]", "", text)
        text_no_links = re.sub(r"\b(.*image.*|.*png.*|.*http.*)\b", "", only_words)
        return text_no_links
