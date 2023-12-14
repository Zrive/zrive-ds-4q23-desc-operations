from src.data_extraction import scraper_web
from src.data_summarizer import api_chatgpt
import pandas as pd
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

logger.level = logging.INFO

if __name__ == "__main__":
    csv_file = "/home/unai/datasets/Original_POC Description of operations - Sheet3.csv"
    df = pd.read_csv(csv_file)

    random_rows = np.random.choice(df.index, 15, replace=False)
    data_15 = df.loc[random_rows]
    data_15["Description"] = np.nan
    data_15["Description"] = data_15["Description"].astype(object)

    for i, row in data_15.iterrows():
        print(row["Company_NAME"])
        html = scraper_web.request_html(row["URL"])

        if str(html).lower().find("error!:") != -1:
            continue

        text = scraper_web.clean_html_text(html)
        if len(text) >= 4096:
            text = text[:4096]
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
        data_15.at[i, "Description"] = description

        # Wait 30 segs (ChatGpt requirement -> 3req/segs)
        time.sleep(30)

    new_csv_file = "/home/unai/datasets/Mod_POC Description of operations - Sheet3.csv"
    data_15.to_csv(new_csv_file, index=False, sep=",")
