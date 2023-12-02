import requests
import pandas as pd
import re
#from credentials import API_KEY, Search_Engine_ID

API_KEY = ""
Search_Engine_ID = ""

class GoogleSearch:

    def __init__(self):
        self.api_key = API_KEY
        self.engine = Search_Engine_ID

