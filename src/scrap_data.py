from scrapers import scraper_web, wikipedia_scraper, ddgo_scraper, bing_scraper, google_scraper
import pandas as pd
import os
import sys
import random

if __name__ == "__main__":
    csv_file = "data/data_coverwallet90.csv"
    df = pd.read_csv(csv_file)

    csv_file = "data/data_coverwallet.csv"
    df = pd.read_csv(csv_file)
    df_tratar = df[df['WEB'].isnull()].reset_index()

    # # # # # df["WEB"] = df["URL"].apply(scraper_web.extract_all_data)
    # # # # # df["wikipedia_v1"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v1)
    # # # # # df["wikipedia_v2"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v2)
    # # # # # df["wikipedia_v3"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v3)

    for i, query in enumerate(df_tratar['Company_NAME']):
        print(f'Vamos por el numero {i}')
        df_tratar.at[i, 'bing_v1'] = bing_scraper.bing_v1(query)
        df_tratar.at[i, 'bing_v2'] = bing_scraper.bing_v2(query)
        df_tratar.at[i, 'google_v1'] = google_scraper.google_v1(query)
        df_tratar.at[i, 'google_v2'] = google_scraper.google_v2(query)
        df_tratar.at[i, 'duckduckgo'] = ddgo_scraper.duckduckgo_search(query)
    df_tratar.to_csv('data/data_coverwallet90.csv', index=False, sep=',')