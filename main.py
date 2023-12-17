from src.data_extraction import scraper_web
from src.data_summarizer import api_chatgpt
from src.logic import data_logic
import pandas as pd
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

logger.level = logging.INFO

FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"

if __name__ == "__main__":
    df = data_logic.data_extraction(FILE_PATH)

    data_sample = data_logic.take_few_rows(data=df, num_rows=5)
    data_sample["Description"] = np.nan
    data_sample["Description"] = data_sample["Description"].astype(object)

    for i, row in data_sample.iterrows():
        print(row["Company_NAME"])
        html = scraper_web.request_html(row["URL"])

        if str(html).lower().find("error!:") != -1:
            continue

        text = scraper_web.clean_html_text(html)
        if len(text) >= 4096:
            text = text[:4096]
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
        data_sample.at[i, "Description"] = description

        # Wait 30 segs (ChatGpt requirement -> 3req/segs)
        time.sleep(30)

    new_csv_file = "data/Mod_POC Description of operations - Sheet3.csv"
    data_sample.to_csv(new_csv_file, index=False, sep=",")
