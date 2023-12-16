import pandas as pd
import requests
from bs4 import BeautifulSoup

# To display all the text of the column
pd.set_option("display.max_colwidth", None)

data = pd.read_csv(
    "/home/pamalo9/zrive-ds-4q23-desc-operations/src/data/POC Description of operations - Sheet3.csv"
)


def realizar_scraping(url):
    # Add http:// to avoid errors
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Take all the text  of the web
        web_text = soup.get_text(separator=" ", strip=True)

        if web_text:
            web_information = {"web_text": web_text}
            return web_information
        else:
            print(f"Not relevant information{url}")
            return None

    except Exception as e:
        print(f"Scrapping error {url}: {e}")
        return None


# Add new column to dataset
data["description"] = None

# Go through each row
for index, row in data.iterrows():
    company_name = row["Company_NAME"]
    url_company = row["URL"]

    # Call the function
    description = realizar_scraping(url_company)

    # Update column
    data.at[index, "description"] = description


data.to_csv(
    "/home/pamalo9/zrive-ds-4q23-desc-operations/src/data/POC Description of operations - Sheet3_updated.csv",
    index=False,
)
