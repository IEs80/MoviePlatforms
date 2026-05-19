import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import sys

#   @class:     TMDBClient
#   @brief:     class that interacts with the "Themoviedb" API
#   @author:    I.S.
#   @version:   1.0
class TMDBClient:
    
    
    def __init__(self, api_key, region='AR'):
        self.api_key = ""
        self.region = region
        self.base_url = "https://api.themoviedb.org/3"
        self.debug = 0

    #   @class:     getApiKey
    #   @brief:     method to read the API KEY in the API_KEY.txt
    #   @author:    I.S.
    #   @version:   1.0
    def setApiKey(self,filename):
        try:
            f = open(filename)
        except OSError:
            print ("Could not open/read file:", filename)
            sys.exit()

        #if we can open the file, we read the API KEY
        self.api_key = f.read()
        #close the file
        f.close()
        if self.debug == 1:
            print(self.api_key)

    #   @class:     getApiKey
    #   @brief:     Mehod to get a specific movie id from the database
    #   @author:    I.S.
    #   @version:   1.0       
    def get_movie_id(self, title):
        """Mehod to get a specific movie id from the database"""
        
        search_url = f"{self.base_url}/search/movie"
        search_url = search_url + f"?query={title}&include_adult=true&language=en-US&page=1"
        if self.debug == 1:
            print(search_url)
  
        headers = {
            'accept': "application/json",
            "Authorization": "Bearer "+f"{self.api_key}"
        }

        response = requests.get(search_url, headers=headers).json()
        
        if self.debug >= 1:
            print(response)
            auth = "Bearer "+f"{self.api_key}"
            print(f"api_key = {auth}")

        if self.debug == 1:
            print(f"movie_id = {response['results'][0]['id']}")

        if response.get('results'):
            return response['results'][0]['id']
        else:
            print("ID not found!\n")
            return None

    #   @class:     search_platforms
    #   @brief:     Search the platforms in which a specific title is available
    #   @author:    I.S.
    #   @version:   1.0  
    def search_platforms(self, title):
        """Search the platforms in which a specific title is available."""
        
        movie_id = self.get_movie_id(title)
        
        if self.debug == 1:
            print(f"movie_id on search = {movie_id}")

        if not movie_id:
            if self.debug == 1:
                print(f"No movie id found")
            return "Movie not found"
            
        providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer "+f"{self.api_key}"
        }

        providers_response = requests.get(providers_url, headers=headers).json()
        
        with open("providers_response.txt", 'w') as f:
            f.write(str(providers_response))

        if self.debug > 1:
            print(providers_response)

        regional_results = providers_response.get('results', {}).get(self.region, {})
        platforms = []
        
        if 'flatrate' in regional_results:
            for proveedor in regional_results['flatrate']:
                platforms.append(proveedor['provider_name'])
                
        return ", ".join(platforms) if platforms else "Movie not available on platforms in this region"
            

