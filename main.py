from src.data_processing import data_logic


ORIGINAL_FILE_PATH = "data/Original_POC Description of operations - Sheet3.csv"
MODIFIED_FILE_PATH = "data/Mod_POC Description of operations - Sheet3.csv"


""" 
If SUMMARIZER_SELECTOR is 0, Code will execute api_chatgpt. 
If SUMMARIZER_SELECTOR is 1, Code will execute hugging_face model
For other cases, ERROR
"""
SUMMARIZER_SELECTOR = 1

def main():
  
    data = data_logic.data_load(ORIGINAL_FILE_PATH)
    
    data_sample = data.sample(n=10, random_state=1)

    data_sample["Description"] = data_sample.apply(data_logic.get_description, axis=1, summarizer_selector = SUMMARIZER_SELECTOR)
    
    data_sample.to_csv(MODIFIED_FILE_PATH, index=False, sep=",")
   
    

if __name__ == "__main__":
   main()
