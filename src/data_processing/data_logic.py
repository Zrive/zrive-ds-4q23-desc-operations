from src.data_extraction import (
    scraper_web,
    bing_scraper,
    ddgo_scraper,
    google_scraper,
    wikipedia_scraper,
)
from src.data_summarizer import api_chatgpt
from src.data_summarizer import bart_large_text_summarizer
from src.data_extraction.utils import error_parser
import pandas as pd
import numpy as np


def data_load(file_path: str) -> pd.DataFrame:
    """
    Reads the CSV data and aggregates a new column where descriptions will be placed.

    fle_path: rhe path to csv data.
    """

    df = pd.read_csv(file_path)
    df["Description"] = np.nan
    df["Description"] = df["Description"].astype(object)
    df["Status"] = np.nan
    df["Status"] = df["Status"].astype(object)
    df["Error"] = np.nan
    df["Error"] = df["Error"].astype(object)
    return df


def get_description(row: pd.Series, summarizer_selector: int) -> tuple[str, int, str]:
    """
    Given a selected summarizer and a DataFrame row, this function performs the data logic to
    obtain a description of the company. If the company URL is available, the web scraper
    engine will be launched. Otherwise, the search engines will be launched with this priority:
    [Bing, DDG, Google, Wikipedia], ensuring that the text comes from the first search engine
    that does not produce an error.

    row: A pd.Series object.
    summary_selector: Choose between the summarizers to perform the summary, where 0=OpenAI ChatGPT
    and 1=bart_large_text_summarizer().
    """
    error = ";"
    status = 0
    print(row["Company_NAME"])

    html = scraper_web.request_html(row["URL"])

    if str(html).lower().find("error!:") != -1:
        search_engine_funcitons = [
            bing_scraper.bing,
            ddgo_scraper.ddg,
            google_scraper.google,
            wikipedia_scraper.wikipedia,
        ]
        error = error + error_parser.parse_error(html)
        for i, function in enumerate(search_engine_funcitons, start=1):
            try:
                status = status + 1
                text = function(row["Company_NAME"])
                if str(text).lower().find("error!:") == -1 and (
                    text and isinstance(text, str)
                ):
                    break
                error = error + error_parser.parse_error(text)
                if i > 3:
                    status = status + 1
                    return pd.Series([np.nan, status, error])
            except Exception as e:
                print(f"Error in {function.__name__}: {e}")
    else:
        text = scraper_web.clean_html_text(html)
        if len(text) >= 4096:
            text = text[:4096]

    if summarizer_selector == 0:
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
        # time.sleep(20)

    elif summarizer_selector == 1:
        description = bart_large_text_summarizer.get_summary(text)

    else:
        raise ValueError("The value of  'SUMMARIZER_SELECTOR' must be 0 or 1")

    return pd.Series([description, status, error])
