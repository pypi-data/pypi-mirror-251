import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class List:
    def __init__(self, author: str, title: str) -> None:
        if not re.match("^[A-Za-z0-9_]*$", author):
            raise Exception("Invalid author")

        self.title = title.replace(' ', '-').lower()
        self.author = author.lower()
        self.url = "https://letterboxd.com/" + self.author +"/list/" + self.title + "/"

        page = self.get_parsed_page(self.url)
    
        self.description(page)
        self.film_count(self.url)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://letterboxd.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def list_title(self, page: None) -> str:
        data = page.find("meta", attrs={'property': 'og:title'})
        return data['content']

    def author(self, page: None) -> str:
        data = page.find("span", attrs={'itemprop': 'name'})
        return data.text

    def description(self, page: None) -> str:
        try:
            data = page.find_all("meta", attrs={'property': 'og:description'})
            self.description = data[0]['content']
        except:
            return None

    def film_count(self, url: str) -> int: #and movie_list!!
        prev = count = 0
        curr = 1
        movie_list = []
        while prev != curr:
            count += 1
            prev = len(movie_list)
            page = self.get_parsed_page(url + "page/" + str(count) + "/")

            img = page.find("ul",{"class": ["js-list-entries poster-list -p125 -grid film-list"], })
            img = img.find_all("img", {"class": ["image"], })

            for item in img:
                movie_url = item.parent['data-film-slug']
                movie_list.append((item['alt'], movie_url))
                
            curr = len(movie_list)

        self.filmCount = curr
        self.movies = movie_list

        if self.filmCount == 0:
            raise Exception("No list exists")
            
def date_created(list: List) -> list:
    if type(list) != List:
        raise Exception("Improper parameter")

    page_data = list.get_parsed_page(list.url)
    data = page_data.find("span", {"class": "published is-updated", })
    if type(data) != type(None):
        data = data.findChild("time")
    else:
        data = page_data.find("span", {"class": "published", })
    return data.text


# Returns date last updated, falling back to date created.
def date_updated(list: List) -> list:
    if type(list) != List:
        raise Exception("Improper parameter")

    page_data = list.get_parsed_page(list.url)
    data = page_data.find("span", {"class": "updated", })
    if type(data) != type(None):
        data = data.findChild("time")
    else:
        data = page_data.find("span", {"class": "published", })
    return data.text
    
def list_tags(list: List) -> list:
    if type(list) != List:
        raise Exception("Improper parameter")

    ret = []

    data = list.get_parsed_page(list.url)
    data = data.find("ul", {"class": ["tags"], })
    data = data.findChildren("a")

    for item in data:
        ret.append(item.text)

    return ret

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    list = List("eddiebergman", "movie-references-made-in-nbcs-community")
    #print(list)
    print(list_tags(list))
