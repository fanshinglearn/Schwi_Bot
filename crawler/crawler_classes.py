import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, 'html.parser')