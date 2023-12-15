from src.Hugging_face_summarizers.Hugging_face_sum1 import get_summary
import pandas as pd


def main():
    PATH_CSV = "/home/pamalo9/zrive-ds-4q23-desc-operations/src/data/POC Description of operations - Sheet3_final.csv"
    df_data = pd.read_csv(PATH_CSV)

    # Call function
    final_df = get_summary(df_data)

    FINAL_PATH_CSV = "/home/pamalo9/zrive-ds-4q23-desc-operations/src/data/FINAL.csv"

    # Final CSV
    final_df.to_csv(FINAL_PATH_CSV, index=False)


if __name__ == "__main__":
    main()
