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
import pandas as pd


def main():
    PATH_CSV = "src/data/POC Description of operations - Sheet3_final.csv"
    df_data = pd.read_csv(PATH_CSV)

    # Call function
    final_df = get_summary(df_data)

    FINAL_PATH_CSV = "src/data/company_summary.csv"

    # Final CSV src/data/FINAL.csv
    final_df.to_csv(FINAL_PATH_CSV, index=False)


if __name__ == "__main__":
    main()
>>>>>>> a69df44 (Archivo main and hugging_face summarizers)
