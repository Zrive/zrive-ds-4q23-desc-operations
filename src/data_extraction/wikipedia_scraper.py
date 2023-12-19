import wikipediaapi

def wikipedia(query: str):
    """
    Call the wikipediaapi for a query search and extract the full web page. No
    correction applied if the query result and the Company Name doesn't match
    """
    global wiki_wiki
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="BusinesParse (ramoncormo8@gmail.com)",
            language="en",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )
        text = wiki_wiki.page(query).text
        if text.strip() == "":
            return None
        else:
            return text
    except Exception as e:
        print(f"Error in Wikipedia for {query}: {e}")
        return None
