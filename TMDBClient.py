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
        
        if response.get('results'):
            if self.debug == 1:
                print(response['results'][0]['id'])
            return response['results'][0]['id']
        return None

    #   @class:     search_platforms
    #   @brief:     Search the platforms in which a specific title is available
    #   @author:    I.S.
    #   @version:   1.0  
    def search_platforms(self, title):
        """Search the platforms in which a specific title is available."""
        try:
            movie_id = self.get_movie_id(title)
            
            if not movie_id:
                return "Movie not found"
                
            providers_url = f"{self.base_url}/movie/{movie_id}/watch/providers"
            params = {'api_key': self.api_key}
            providers_response = requests.get(providers_url, params=params).json()
            
            regional_results = providers_response.get('results', {}).get(self.region, {})
            platforms = []
            
            if 'flatrate' in regional_results:
                for proveedor in regional_results['flatrate']:
                    platforms.append(proveedor['provider_name'])
                    
            return ", ".join(platforms) if platforms else "Movie not available on platforms in this region"
                
        except Exception:
            return "*Error searching platforms*"


