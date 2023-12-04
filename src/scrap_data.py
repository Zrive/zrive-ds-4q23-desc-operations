from scrapers import scraper_web
import pandas as pd

if __name__ == "__main__":
    csv_file = "/home/unai/datasets/POC Description of operations - Sheet3.csv"
    df = pd.read_csv(csv_file)
    df["WEB_2"] = df.head(15)["URL"].apply(scraper_web.extract_all_text)

    df.to_csv(csv_file, index=False, sep=",")
