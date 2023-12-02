from scrapers import scraper_web
import pandas as pd

if __name__ == "__main__":
    csv_file = "/home/unai/datasets/POC Description of operations - Sheet3.csv"
    df = pd.read_csv(csv_file)
    df["WEB"] = df["URL"].apply(scraper_web.extract_all_data)

    df.to_csv(csv_file, index=False, sep=",")
