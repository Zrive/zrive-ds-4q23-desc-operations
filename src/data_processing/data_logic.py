from src.data_extraction import (
    scraper_web,
    bing_scraper,
    ddgo_scraper,
    google_scraper,
    wikipedia_scraper,
)
from src.data_summarizer import api_chatgpt
from src.data_summarizer import bart_large_text_summarizer
import pandas as pd
import numpy as np
import time


def data_load(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["Description"] = np.nan
    df["Description"] = df["Description"].astype(object)
    df["Status"] = np.nan
    df["Status"] = df["Status"].astype(object)
    return df


def get_description(row: pd.Series, summarizer_selector: int) -> tuple[str, int]:
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
        for i, function in enumerate(search_engine_funcitons, start=1):
            try:
                print("HOLAAAAA")
                status = status + 1
                text = function(row["Company_NAME"])
                if text and isinstance(text, str):
                    break
                if i > 3:
                    status = status + 1
                    return pd.Series([np.nan, status])
            except Exception as e:
                print(f"Error in {function.__name__}: {e}")
    else:
        text = scraper_web.clean_html_text(html)
        if len(text) >= 4096:
            text = text[:4096]

    if summarizer_selector == 0:
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
        time.sleep(25)

    elif summarizer_selector == 1:
        description = bart_large_text_summarizer.get_summary(text)

    else:
        raise ValueError("The value of  'SUMMARIZER_SELECTOR' must be 0 or 1")

    return pd.Series([description, status])
