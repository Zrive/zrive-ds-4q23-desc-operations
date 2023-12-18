from src.data_processing import data_logic
from src.data_summarizer.bart_large_text_summarizer import get_summary


ORIGINAL_FILE_PATH = "data/PROBANDO.csv"
MODIFIED_FILE_PATH = "data/FUNCIONA_C.csv"
MODIFIED_FILE_PATH1 = "data/FUNCIONA_H.csv"

# If SUMMARIZER_SELECTOR is 0, Code will execute api_chatgpt. For other cases, hugging_face model
SUMMARIZER_SELECTOR = 1
def main():
  
    data = data_logic.data_load(ORIGINAL_FILE_PATH)
    
    data_sample = data.sample(n=10, random_state=1)

    data_sample["Description"] = data_sample.apply(data_logic.get_description, axis=1, summarizer_selector = SUMMARIZER_SELECTOR)
    
    data_sample.to_csv(MODIFIED_FILE_PATH1, index=False, sep=",")
   
    

if __name__ == "__main__":
   main()
