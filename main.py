from src.data_processing import data_logic
from src.data_summarizer.bart_large_text_summarizer import get_summary
import numpy as np
import pandas as pd

ORIGINAL_FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"
MODIFIED_FILE_PATH = "data/Mod_POC Description of operations - Sheet3.csv"

def main():
    PATH_CSV = "data/POC Description of operations - Sheet3_final.csv"
    FINAL_PATH_CSV = "data/FINAL.csv"

    df_data = pd.read_csv(PATH_CSV)

    # Call function
    final_df = get_summary(df_data)

    final_df.to_csv(FINAL_PATH_CSV, index=False)

    """"
    data = data_logic.data_load(ORIGINAL_FILE_PATH)

    data_sample = data.sample(n=5, random_state=1)

    data_sample["Description"] = data_sample.apply(data_logic.get_description, axis=1)

    data_sample.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")

    hugging_face_summary = get_summary(data_sample)
    hugging_face_summary.to_csv(MODIFIED_FILE_PATH,index=False, sep=",")
"""
if __name__ == "__main__":
   main()
