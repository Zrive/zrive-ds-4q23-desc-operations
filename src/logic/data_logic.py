import pandas as pd
import numpy as np


def data_extraction(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def take_few_rows(data: pd.DataFrame, num_rows: int = 15) -> pd.DataFrame:
    random_rows = np.random.choice(data.index, num_rows, replace=False)
    selected_data = data.loc[random_rows]
    return selected_data
