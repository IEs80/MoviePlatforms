import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#   @class:     TMDBClient
#   @brief:     class that interacts with the "Themoviedb" API
#   @author:    I.S.
#   @version:   1.0
class TMDBClient:
    
    
    def __init__(self, api_key, region='AR'):
        self.api_key = api_key
        self.region = region
        self.base_url = "https://api.themoviedb.org/3"
        
    def _buscar_id_pelicula(self, titulo):
        """Método interno para obtener el ID de la película."""
        search_url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': titulo
        }
        response = requests.get(search_url, params=params).json()
        
        if response.get('results'):
            return response['results'][0]['id']
        return None

    def buscar_plataformas(self, titulo):
        """Devuelve un string con las plataformas disponibles o un mensaje de error."""
        try:
            movie_id = self._buscar_id_pelicula(titulo)
            
            if not movie_id:
                return "No encontrada"
                
            providers_url = f"{self.base_url}/movie/{movie_id}/watch/providers"
            params = {'api_key': self.api_key}
            providers_response = requests.get(providers_url, params=params).json()
            
            resultados_region = providers_response.get('results', {}).get(self.region, {})
            plataformas = []
            
            if 'flatrate' in resultados_region:
                for proveedor in resultados_region['flatrate']:
                    plataformas.append(proveedor['provider_name'])
                    
            return ", ".join(plataformas) if plataformas else "No disponible en suscripción plana"
                
        except Exception:
            return "Error en la búsqueda"



