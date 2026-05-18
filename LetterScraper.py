import requests
from bs4 import BeautifulSoup
import time

#   @class: LetterScraper
#   @brief: 
#   @author:
#   @version: 

class LetterScraper: 
    """Class that will retrieve the information from the users watchlist"""

    def __init__(self,username):
        self.username = username
        self.headers= { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        #init empy list movies
        self.movies = []
    

    #return 

    #   @fn:    print_movies
    #   @brief: prints all the scraped movies
    #   @author: I.S.
    #   @version: 1.0
    def print_movies(self):
        if self.movies == []:
            print('nothing to print')

        for movie in self.movies:
            print(movie)

    #   @fn:        getWatchList
    #   @brief:     scraps the user's Letterbox watchlist and stores the movie titles
    #   @author:    I.S.        
    #   @version:   1.0
    def getWatchList(self):
        print(f"Connecting to the {self.username} watchlist...")
        

        #initialize watchliste page
        page = 1

        while True:
            #define the URL to scrap
            if page == 1:
                url = f"https://letterboxd.com/{self.username}/watchlist/"    
            else:
                url = f"https://letterboxd.com/{self.username}/watchlist/page/{page}/"
            
            #get the URL
            response = requests.get(url,headers=self.headers)

            #check if the response status is correct
            if not response.ok:
                print(f"Error getting the page. Response = {response}")
                break 

            #
            soup = BeautifulSoup(response.text, 'html.parser')
            #we get all the film posters of the page
            posters = soup.find_all('div', class_='film-poster')
            
            #of there are't posters on the page, we get out
            if not posters:
                break
                
            #for each poster, we get the "alt" text, and we stored it into the "movies" list    
            for poster in posters:
                img = poster.find('img')
                if img and img.has_attr('alt'):
                    self.movies.append(img['alt'])
                    
            print(f"Page {page} extracted...")

            #increment the page number
            page += 1
            time.sleep(0.5)


    #   @fn:    print_movies_to_file
    #   @brief: prints all the scraped movies to a file
    #   @author: I.S.
    #   @version: 1.0
    def print_movies_to_file(self):
        if self.movies == []:
            print('nothing to print')

        file_name = self.username + '_watchlist.txt'
        with open(file_name, 'w') as wf:
            for movie in self.movies:
                wf.write(f"{movie}\n")
