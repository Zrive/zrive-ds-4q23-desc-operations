from scrapers import scraper_web, wikipedia_scraper
import pandas as pd

if __name__ == "__main__":
    path = "../data/data.csv"
    df = pd.read_csv(path, sep=",")
    df["wikipedia_v1"] = df["Company name"].apply(wikipedia_scraper.wikipedia_v1)
    df["wikipedia_v2"] = df["Company name"].apply(wikipedia_scraper.wikipedia_v2)
    df["wikipedia_v3"] = df["Company name"].apply(wikipedia_scraper.wikipedia_v3)

    df.to_csv(path, index=False, sep=",")
