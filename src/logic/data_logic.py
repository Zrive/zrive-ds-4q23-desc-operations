import pandas as pd
import numpy as np


def data_extraction(file_path: str) -> pd.DataFrame:
    csv_file = "/home/unai/datasets/Original_POC Description of operations - Sheet3.csv"
    df = pd.read_csv(csv_file)
    return df


def take_few_rows(data: pd.DataFrame, num_rows: int = 15) -> pd.DataFrame:
    random_rows = np.random.choice(data.index, num_rows, replace=False)
    selected_data = data.loc[random_rows]
    return selected_data
