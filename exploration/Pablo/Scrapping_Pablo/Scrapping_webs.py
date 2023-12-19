import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

PATH = "data/POC Description of operations - Sheet3.csv"
PATH_RESULT =  "data/POC Description of operations - Sheet3_updated.csv"

pd.set_option("display.max_colwidth", None)

data = pd.read_csv(PATH)


def realizar_scraping(url):
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

       
        web_text = soup.get_text(separator=" ", strip=True)

        if web_text:
            web_information = {"web_text": web_text}
            return web_information
        else:
            print(f"Not relevant information{url}")
            return None

    except Exception as e:
        logging.error(f"Scrapping error {url}: {e}")
        return None


data['description'] = None

for index, row in data.iterrows():
    company_name = row['Company_NAME']
    url_company = row['URL']

  
    description = realizar_scraping(url_company)

    
    data.at[index, 'description'] = description


data.to_csv(PATH_RESULT, index=False)

