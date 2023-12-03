import requests
import pandas as pd
import re
#from credentials import API_KEY, Search_Engine_ID

API_KEY = ""
Search_Engine_ID = ""
URL = "https://www.googleapis.com/customsearch/v1"
class GoogleSearch:

    def __init__(self):
        self.api_key = API_KEY
        self.engine = Search_Engine_ID

    def build_payload(self, query: str, **kwargs) -> dict:
        return {
            "key": self.api_key,
            "q": query,
            "cx": self.engine,
        }.update(kwargs)

    def make_request(self, payload: dict) -> dict:
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()  # Verifica si hay errores en la respuesta HTTP
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error de conexión: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Tiempo de espera agotado: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Error desconocido: {err}")
    
    def search_in_google(self, query: str, **kwargs) -> str:
        payload = self.build_payload(query, **kwargs)
        response = self.make_request(payload)
        return response["items"][0]["link"]

