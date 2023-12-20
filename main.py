from src.data_processing import data_logic


ORIGINAL_FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"
MODIFIED_FILE_PATH = "data/Mod_POC Description of operations - Sheet3.csv"

SUMMARIZER_SELECTOR = 0

""" 
If SUMMARIZER_SELECTOR is 0, Code will execute api_chatgpt. 
If SUMMARIZER_SELECTOR is 1, Code will execute hugging_face model
For other cases, ERROR
STATUS: 
- 0 -> WEB SCARPING
- 1 -> SEARCH_ENIGNE BING
- 2 -> SEARCH_ENIGNE DDG
- 3 -> SEARCH_ENIGNE GOOGLE
- 4 -> SEARCH_ENIGNE WIKIPEDIA
- 5 -> ERROR
"""


def main():
    data = data_logic.data_load(ORIGINAL_FILE_PATH)

    # data_sample = data.sample(n=3, random_state=1)

    data[["Description", "Status", "Error"]] = data.apply(
        data_logic.get_description, axis=1, summarizer_selector=SUMMARIZER_SELECTOR
    )

    data.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")


if __name__ == "__main__":
    main()
