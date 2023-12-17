from readability import Document
import logging
import bs4
import re

logging.getLogger('readability').propagate = False
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