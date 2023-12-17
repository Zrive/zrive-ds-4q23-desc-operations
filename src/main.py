if __name__ == "__main__":
    print('Hello Team')
    # csv_file = "data/data_coverwallet90.csv"
    # df = pd.read_csv(csv_file)

    # csv_file = "data/data_coverwallet.csv"
    # df = pd.read_csv(csv_file)
    # df_tratar = df[df['WEB'].isnull()].reset_index()

    # # # # # df["WEB"] = df["URL"].apply(scraper_web.extract_all_data)
    # # # # # df["wikipedia_v1"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v1)
    # # # # # df["wikipedia_v2"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v2)
    # # # # # df["wikipedia_v3"] = df["Company_NAME"].apply(wikipedia_scraper.wikipedia_v3)
    #query = 'TEMPE BODY SHOP, INC.'
    
    # print(bing_scraper.bing_v1(query))
    # print('\n', '###################################################', '\n')
    # print(bing_scraper.bing_v2(query))
    # print('\n', '###################################################', '\n')
    #print(google_scraper.google_v1(query))
    #print('\n', '###################################################', '\n')
    #print(google_scraper.google_v2(query))
    # print('\n', '###################################################', '\n')
    # print(ddgo_scraper.duckduckgo_search(query))
    # print('\n', '###################################################', '\n')

    #print(ddgo_scraper.test(query))
    
    #print(bing_scraper.bing_urls(query))
    #print('\n', '###################################################', '\n')
    # print(google_scraper.google_urls(query))
    # print('\n', '###################################################', '\n')


    # for i, query in enumerate(df_tratar['Company_NAME']):
    #     print(f'Vamos por el numero {i}')
    #     df_tratar.at[i, 'bing_v1'] = bing_scraper.bing_v1(query)
    #     df_tratar.at[i, 'bing_v2'] = bing_scraper.bing_v2(query)
    #     df_tratar.at[i, 'google_v1'] = google_scraper.google_v1(query)
    #     df_tratar.at[i, 'google_v2'] = google_scraper.google_v2(query)
    #     df_tratar.at[i, 'duckduckgo'] = ddgo_scraper.duckduckgo_search(query)
    # df_tratar.to_csv('data/data_coverwallet90.csv', index=False, sep=',')