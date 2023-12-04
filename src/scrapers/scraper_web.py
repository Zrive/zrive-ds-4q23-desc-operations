import requests
from bs4 import BeautifulSoup
from boilerpy3 import extractors
import numpy as np
import html2text


def extract_all_text(url: str):
    url_base = "https://"
    url_complete = url_base + url
    html = html_request(url_complete)
    if str(html).lower().find("error!:") != -1:
        return None
    else:
        h = html2text.HTML2Text()
        html_compelte = html.prettify()
        h.ignore_links = False
        return h.handle(html.prettify())


def extract_all_data(url: str):
    url_base = "https://"
    url_complete = url_base + url
    html = html_request(url_complete)
    if str(html).lower().find("error!:") != -1:
        return None
    else:
        html_compelte = html.prettify()
        return html_to_text(html_compelte)


def html_request(url: str):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Lanzar una excepción para errores HTTP

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Parsear el contenido HTML de la página
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            return f"ERROR!: {response.status_code}"

    except requests.exceptions.RequestException as e:
        # Capturar excepción de solicitud y devolver un mensaje de error
        return f"Request_error!: {e}"

    except Exception as e:
        # Capturar cualquier otra excepción y devolver un mensaje de error
        return f"Unexpected_error!: {e}"


def html_to_text(html):
    parsed_text = parse_html(html)
    return parsed_text


def parse_html(html):
    html_extractor = extractors.ArticleExtractor()
    return html_extractor.get_content(html)
