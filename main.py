from src.data_processing import data_logic
import numpy as np

ORIGINAL_FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"
MODIFIED_FILE_PATH = "data/Mod_POC Description of operations - Sheet3.csv"

if __name__ == "__main__":
    df = data_logic.data_extraction(ORIGINAL_FILE_PATH)

    data_sample = data_logic.take_few_rows(data=df, num_rows=5)

    data_sample["Description"] = data_sample.apply(
        data_logic.obtain_organization_description, axis=1
    )

    data_sample.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")
