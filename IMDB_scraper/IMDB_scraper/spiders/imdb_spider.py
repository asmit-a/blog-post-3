# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    # start url contains the url to arcane's IMDB page
    start_urls = ['https://www.imdb.com/title/tt0417299/']

    # assumes you start on a movie page, navigates to cast&crew page, 
    # calls parse_full_credits
    def parse(self, response):
        # need to define what url is
        movie_url = "https://www.imdb.com/title/tt0417299/"
        credits_url = movie_url + "fullcredits/"
        yield Request(credits_url, callback = self.parse_full_credits)

    # assumes you start on cast&crew page, leads to page of each actor,
    # calls parse_actor_page
    def parse_full_credits(self, response):
        base_url = "https://www.imdb.com"
        # need to retrieve list of all actors 
        # cast_table = response.css("table.cast_list")
        # cast_rows = cast_table.css("td")
        # cast_names = cast_rows.css("a")

        # cast_links = [link.attrib["href"] for link in cast_names]
        # THINK ABOUT WHY THIS DOESN'T WORK.

        actor_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        # gives all the relative paths to the actors

        for url in actor_urls: 
            full_actor_url = base_url + url
            yield Request(full_actor_url, callback = self.parse_actor_page)

        # using css selectors

        # need to loop through each actor
        # and call a scrapy request

    # assumes you start on page of actor, yields dictionary
    def parse_actor_page(self, response):
        
        # on the page of an actor

        # need to determine name of actor

        # retrieve each of the movies/tv shows they've worked on
        # input to dictionary

        # to get NAME: 
        name_string = response.css("td.name-overview-widget__section h1.header span::text").get()

        # to get all of their FILMS:
        filmography_rows = response.css("div.filmo-row")
        filmography = [row.css("a::text").get() for row in filmography_rows]

        for film in filmography: 
            yield {
                "actor": name_string, 
                "movie_or_TV_name": film
            }

        # yields dictionary

        