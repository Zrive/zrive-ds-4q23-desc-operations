import argparse
import bs4
from duckduckgo_search import ddg
from readability import Document

# ******
# this is a hack to stop scrapy from logging its version info to stdout
# there should be a better way to do this, but I don't know what it is

import scrapy
from scrapy.crawler import CrawlerProcess

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
    lines = input_text.splitlines()
    # this function removes all duplicate empty lines from the lines
    fixed_lines = []
    for index, line in enumerate(lines):
        if line.strip() == '':
            if index != 0 and lines[index-1].strip() != '':
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)


class MySpider(scrapy.Spider):
    '''
    This is the spider that will be used to crawl the webpages. We give this to the scrapy crawler.
    '''
    name = 'myspider'
    start_urls = None
    results = []

    def __init__(self, start_urls, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        body_html = response.body.decode('utf-8')
        url = response.url
        soup = bs4.BeautifulSoup(body_html, 'html.parser')
        title = soup.title.string
        text = soup.get_text()
        text = remove_duplicate_empty_lines(text) 
        useful_text = readability(body_html)
        useful_text = remove_duplicate_empty_lines(useful_text)
        self.results.append({
            'url': url,
            'title': title,
            'text': text,
            'useful_text': useful_text
        })

def ddgo_query(query, numresults=10):
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

    # perform the search
    results = ddg(query, max_results=numresults)
    # get the urls
    urls = [result['href'] for result in results]
    urls = urls[:numresults]
    process = CrawlerProcess()
    process.crawl(MySpider, urls)
    process.start()
    # here the spider has finished downloading the pages and cleaning them up
    return MySpider.results

def get_result_lines(results, shorten):
    result_lines = []
    for index, results in enumerate(results):
        result_lines.append(f"Result {index+1}")
        result_lines.append(f"Url: {results['url']}")
        result_lines.append(f"Title: {results['title']}")
        if shorten:
            result_lines.append("Cleaned Text (shortened):")
            useful_lines = results['useful_text'].splitlines()[:20]
            short_useful_text = '\n'.join(useful_lines)
            result_lines.append(short_useful_text)
        else:
            result_lines.append("Cleaned Text:")
            result_lines.append(results['useful_text'].replace('\r\n', ' '))
        result_lines.append('')
    return result_lines

def duckduckgo_search(query:str, numresults:int) -> str:
    results = ddgo_query(query, numresults)
    result_lines = get_result_lines(results, shorten=False)
    return '\n'.join(result_lines)


def file_handeler(**kwargs):
    # usage: python ddgsearch.py query [--numresults <numresults=10>] [--clean_with_llm] [--outfile <outfile name>] [--loglevel <loglevel=ERROR>] [--noprint]
    # ddgsearch performs the search, gets the results, and downloads the pages and prints the text.
    # parse command line arguments
    parser = argparse.ArgumentParser()

    import os
    import re

    parser.add_argument('query', help='the query to search for')
    parser.add_argument('--numresults', help='the number of results to return', default=10)
    parser.add_argument('--outfile', help='the name of the file to write the results to', default=None)
    parser.add_argument('--noprint', help='do not print the results to the screen', action='store_true')

    args = parser.parse_args()

    query = args.query
    numresults = int(args.numresults)

    def make_filename_safe(input_string):
        # replace all non-alphanumeric characters with underscores
        return re.sub(r'\W+', '_', input_string)
    default_outfile = os.path.join('working', f'{make_filename_safe(query)}.txt')

    outfile = args.outfile or default_outfile
    noprint = args.noprint

    results = ddgo_query(query, numresults)

    if outfile:
        # make sure this is unicode safe
        with open(outfile, 'w', encoding='utf-8') as f:
            result_lines = get_result_lines(results, shorten=False)
            f.writelines([f"{result}\n" for result in result_lines])

    if not noprint:
        shortened_result_lines = get_result_lines(results, shorten=True)
        for line in shortened_result_lines:
            print(line)