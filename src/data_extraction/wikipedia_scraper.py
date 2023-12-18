import wikipedia
import wikipediaapi

def key_words(categories:list):
    text = ' '.join(categories)
    key_words = ['company', 'companies', 'business', 'businesses', 'corporate', 'corporates', 'university']
    key_words = [key_word.lower() for key_word in key_words]
    text_lower = text.lower()
    for category in key_words:
        if category in text_lower:
            return True
    return False

def keys_format(json_keys:dict) -> list:
    categories_result = []
    for key in json_keys.keys():
        key_formated = key.replace('Category:', '')
        categories_result.append(key_formated)
    return categories_result

def wikipedia_v1(subject: str):
    subjects = wikipedia.search(subject)
    if subjects:
        for subject in subjects:
            try:
                categories_subject = wikipedia.page(subject).categories
                if key_words(categories_subject):
                    return wikipedia.page(subject).content
            except wikipedia.DisambiguationError:
                continue
            except wikipedia.PageError:
                return None
    return None

def wikipedia_v2(subject: str):
    global wiki_wiki
    wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='BusinesParse (ramoncormo8@gmail.com)',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    subjects = wikipedia.search(subject)
    if subjects:
        for subject in subjects:
            categories_subject = keys_format(json_keys=wiki_wiki.page(subject).categories)
            if key_words(categories_subject):
                return wiki_wiki.page(subject).text
    return None

def wikipedia_v3(subject: str):
    global wiki_wiki
    wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='BusinesParse (ramoncormo8@gmail.com)',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    text = wiki_wiki.page(subject).text
    if text.strip() == '':
        return None
    else:
        return text