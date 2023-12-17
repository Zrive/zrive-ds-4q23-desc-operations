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
>>>>>>> a69df44 (Archivo main and hugging_face summarizers)
