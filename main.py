from LetterScraper import LetterScraper
from TMDBClient import TMDBClient
import time
import pandas as pd

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # 1. Configuración inicial
    API_KEY = 'TU_CLAVE_API_AQUI' 
    REGION = 'AR'


    # 2. Instanciamos nuestras clases
    user = input("Enter your LB username... \n")
    OUT_FILE = f'Watchlist_{user}_Plataformas.csv'
    Scraper = LetterScraper(username=user)
    tmdb = TMDBClient(API_KEY, REGION)

    # 3. Extraemos las películas
    movie_list = Scraper.getWatchList()
    print(f"\n¡Éxito! Se encontraron {len(movie_list)} películas en tu Watchlist.\n")

    if len(movie_list) > 0:
        resultados = []
        print("Searching availability in AR platforms...")

        # 4. Consultamos la API para cada película
        for i, titulo in enumerate(movie_list, 1):
            print(f"[{i}/{len(movie_list)}] Searching: {titulo}...")
            
            plataformas = tmdb.buscar_plataformas(titulo)
            
            resultados.append({
                'Película': titulo,
                'Plataformas (AR)': plataformas
            })
            time.sleep(0.2) # Respetamos el límite de peticiones de TMDB

        # 5. Exportamos los datos
        df = pd.DataFrame(resultados)
        df.to_csv(OUT_FILE, sep=';', index=False)
        print(f"\n¡Proceso terminado al 100%! Revisá el archivo: {OUT_FILE}")
    else:
        print("No se encontraron películas. Revisá que tu usuario sea correcto y tu perfil público.")