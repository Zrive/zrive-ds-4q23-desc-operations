<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_processing import data_logic
import numpy as np

ORIGINAL_FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"
MODIFIED_FILE_PATH = "data/Mod_POC Description of operations - Sheet3.csv"

if __name__ == "__main__":
    data = data_logic.data_load(ORIGINAL_FILE_PATH)

    data_sample = data.sample(n=5, random_state=1)

    data_sample["Description"] = data_sample.apply(data_logic.get_description, axis=1)

    data_sample.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")
=======
from src.Hugging_face_summarizers.Hugging_face_sum1 import get_summary
=======
from src.Hugging_face_summarizer.Hugging_face_sum1 import get_summary
>>>>>>> b50d2f2 (Take the final summarizer in src and change path in main)
=======
from src.data_summarizer.bart_large_text_summarizer import get_summary
>>>>>>> fb3aed8 (Changes)
import pandas as pd


PATH_CSV = "data/POC Description of operations - Sheet3_final.csv"
FINAL_PATH_CSV = "data/company_summary.csv"


def main():
    df_data = pd.read_csv(PATH_CSV)

    final_df = get_summary(df_data)
    final_df.to_csv(FINAL_PATH_CSV, index=False)


if __name__ == "__main__":
    main()
<<<<<<< HEAD
>>>>>>> a69df44 (Archivo main and hugging_face summarizers)
=======
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
>>>>>>> 685ba7e (Executable: Web_Scraper + Api_ChatGpt)
