from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class Crawl:
    url: str
    info: List[str]

    def __init__(self, url) -> None:
        self.url = url
        
    def get_info(self) -> None:
        page = requests.get(self.url)
        self.info = BeautifulSoup(page.text, 'html.parser')
        return self.info





