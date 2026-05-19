from LetterScraper import LetterScraper
from TMDBClient import TMDBClient
import time
import pandas as pd
import sys


if __name__ == "__main__":

    #set region
    REGION = 'AR'

    #set out Letterboxd user
    user = input("Enter your LB username... \n")
    #set output file name
    OUT_FILE = f'Watchlist_{user}_Plataformas.csv'
    #Initialize Scraper
    Scraper = LetterScraper(username=user)
    #Initialize TMDB Client
    tmdb = TMDBClient(REGION)
    #Set the API KEY
    tmdb.setApiKey('API_KEY.txt')


    #Get watchlist
    use_file = input("Use watchlist file? Y/N \n")
    while use_file != "Y" and use_file != "N":
        use_file = input("Use watchlist file? Y/N \n")
    
    #if the user wants to use a file, we try to open it
    if use_file == 'Y':
        try:
            file_name = Scraper.username + '_watchlist.txt'
            print(file_name)
            f = open(file_name,'r')
            for x in f.readlines():
                Scraper.movies.append(x.rstrip("\n").replace(' ','-').lower())
            f.close()
        except OSError:
            print("Couldn't open file. Searching the web...")
            #Scraper.getWatchList()
            sys.exit()
    else:
        Scraper.getWatchList()
        #store_in_file = input("Want to store watchlist in file? Y/N \n")
        #while store_in_file != "Y" and use_file != "N":
        #    use_file = input("Use watchlist file? Y/N \n")
        #if store_in_file == "Y":
        #    Scraper.print_movies_to_file()

        

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