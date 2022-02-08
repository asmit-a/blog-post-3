import scrapy
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    # Doctor Who (2005)'s IMDB page
    start_urls = ['https://www.imdb.com/title/tt0436992/']


    def parse(self, response):
        """
        Assumes we start on a movie's main page and navigates to 
        movie's Cast & Crew page. 

        @param self: an instance of this class.  
        @param response: the result of scrapy's HTTP request. 
        """

        movie_url = "https://www.imdb.com/title/tt0436992/"
        credits_url = movie_url + "fullcredits/"
        yield Request(credits_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Assumes we start on a movie's Cast & Crew page and navigates
        to the pages of each of the cast members listed on it. 

        @param self: an instance of this class.  
        @param response: the result of scrapy's HTTP request. 
        """
        # retrieves all the relative paths to the actors
        # listed on the Cast & Crew page
        actor_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        base_url = "https://www.imdb.com"
        
        # loops through each of the relative actor urls
        for url in actor_urls: 
            full_actor_url = base_url + url
            yield Request(full_actor_url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        name_string = response.css("td.name-overview-widget__section h1.header span::text").get()
        filmography_rows = response.css("div.filmo-row")
        filmography = [row.css("a::text").get() for row in filmography_rows]

        for film in filmography: 
            yield {
                "actor": name_string, 
                "movie_or_TV_name": film
            }



# to run 
# scrapy crawl imdb_spider -o movies.csv


        