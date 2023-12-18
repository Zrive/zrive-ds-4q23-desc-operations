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
<<<<<<< HEAD
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
from src.logic import data_logic
import pandas as pd
import time
import numpy as np
=======
from src.data_processing import data_logic


>>>>>>> 18280b1 (tt)

FILE_PATH = "/home/unai/datasets/Original_POC Description of operations - Sheet3.csv"

<<<<<<< HEAD
if __name__ == "__main__":
    df = data_logic.data_extraction(FILE_PATH)
=======
def main():

    data = data_logic.data_load(ORIGINAL_FILE_PATH)
>>>>>>> d379a3c (Archivo main and hugging_face summarizers)

<<<<<<< HEAD
    few_data = data_logic.take_few_rows(data=df, num_rows=5)
    few_data["Description"] = np.nan
    few_data["Description"] = few_data["Description"].astype(object)

    for i, row in few_data.iterrows():
        print(row["Company_NAME"])
        html = scraper_web.request_html(row["URL"])

<<<<<<< HEAD
        if str(html).lower().find("error!:") != -1:
            continue

        text = scraper_web.clean_html_text(html)
        if len(text) >= 4096:
            text = text[:4096]
        description = api_chatgpt.chatgpt_call(text, row["Company_NAME"])
        few_data.at[i, "Description"] = description

        # Wait 30 segs (ChatGpt requirement -> 3req/segs)
        time.sleep(30)
=======
    data_sample = data_logic.take_few_rows(data=df, num_rows=5)

    data_sample["Description"] = data_sample.apply(
        data_logic.obtain_organization_description, axis=1
    )
>>>>>>> bf1d840 (main refactorized)

    new_csv_file = "/home/unai/datasets/Mod_POC Description of operations - Sheet3.csv"
<<<<<<< HEAD
    data_15.to_csv(new_csv_file, index=False, sep=",")
>>>>>>> 685ba7e (Executable: Web_Scraper + Api_ChatGpt)
=======
    few_data.to_csv(new_csv_file, index=False, sep=",")
>>>>>>> b70535e (fixed key exposure)
=======
    data_sample.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")

    hugging_face_summary = get_summary(data_sample)
    hugging_face_summary.to_csv(MODIFIED_FILE_PATH,index=False, sep=",")


if __name__ == "__main__":
    main()
>>>>>>> d379a3c (Archivo main and hugging_face summarizers)
