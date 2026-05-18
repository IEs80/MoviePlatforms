from LetterScraper import LetterScraper
from TMDBClient import TMDBClient
import time
import pandas as pd
import sys

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # 1. Configuración inicial

    REGION = 'AR'


    # 2. Instanciamos nuestras clases
    user = input("Enter your LB username... \n")
    OUT_FILE = f'Watchlist_{user}_Plataformas.csv'
    Scraper = LetterScraper(username=user)
    tmdb = TMDBClient(REGION)


    # 3. Extraemos las películas
    use_file = input("Use watchlist file? Y/N \n")
    while use_file != "Y" and use_file != "N":
        use_file = input("Use watchlist file? Y/N \n")
    
    #4. if the user wants to use a file, we try to open it
    if use_file == 'Y':
        try:
            file_name = Scraper.username + '_watchlist.txt'
            print(file_name)
            f = open(file_name,'r')
            for x in f.readlines():
                Scraper.movies.append(x)
            f.close()
        except OSError:
            print("Couldn't open file. Searching the web...")
            #Scraper.getWatchList()
            sys.exit()
    else:
        Scraper.getWatchList()

    print(f"\n{len(Scraper.movies)} movies on your Watchlist!\n")

    
    if len(Scraper.movies) > 0:
        resultados = []
        print("Searching availability in AR platforms...")

        # 5. Consultamos la API para cada película
        for i, titulo in enumerate(Scraper.movies, 1):
            print(f"[{i}/{len(Scraper.movies)}] Searching: {titulo}...")
            
            plataformas = tmdb.search_platforms(titulo)
            
            resultados.append({
                'Película': titulo,
                'Plataformas (AR)': plataformas
            })
            time.sleep(0.2) # Respetamos el límite de peticiones de TMDB

        # 6. Exportamos los datos
        df = pd.DataFrame(resultados)
        df.to_csv(OUT_FILE, sep=';', index=False)
        print(f"\n¡Proceso terminado al 100%! Revisá el archivo: {OUT_FILE}")
    else:
        print("No se encontraron películas. Revisá que tu usuario sea correcto y tu perfil público.")