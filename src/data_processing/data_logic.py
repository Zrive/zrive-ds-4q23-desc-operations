from src.data_extraction import scraper_web
from src.data_summarizer import api_chatgpt
from src.data_summarizer import bart_large_text_summarizer
import pandas as pd
import numpy as np
import time


def data_load(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["Description"] = np.nan
    df["Description"] = df["Description"].astype(object)
    return df


def get_description(row: pd.Series, summarizer_selector: int) -> str:
    print(row["Company_NAME"])
    html = scraper_web.request_html(row["URL"])

    if str(html).lower().find("error!:") != -1:
        # TODO: CALL SEARCH_ENGINE. If fails:
        return np.nan

    text = scraper_web.clean_html_text(html)
    if len(text) >= 4096:
        text = text[:4096]

    if summarizer_selector == 0:
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
    else:
        description = bart_large_text_summarizer.get_summary(text)

    time.sleep(30)

    return description
