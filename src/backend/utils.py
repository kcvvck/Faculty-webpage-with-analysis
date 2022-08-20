import requests
from bs4 import BeautifulSoup


def get_info(url) -> None:
    page = requests.get(url)
    info = BeautifulSoup(page.text, 'html.parser')
    return info
