import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import dblp
import requests
import validators
from bs4 import BeautifulSoup
from config import config
from scholarly import ProxyGenerator, scholarly
from tqdm import tqdm

pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)


@dataclass
class Retrieve:
    '''
    Retrieve information from dblp, drntu, google scholar
    and output as JSON file
    '''
    urls: List[str]
    tag: str
    class_: str

    def __post_init__(self) -> None:
        '''
        validate website
        '''
        for url in self.urls:
            if not validators.url(url):
                raise Exception("Invalid URL.")

    def retrieve_info(self):
        '''
        retrieve information given a list of starting urls
        '''
        Path(config.DATA_FILE).mkdir(exist_ok=True)
        for url in self.urls:
            get_dr_ntu(url)


def get_dr_ntu(url):
    '''
    Main retrieve function
    '''
    all_info = get_info(url)
    faculty_list = all_info.find("table", attrs={"class": "table table-hover"})
    faculty_data = faculty_list.find_all("tr")
    for data in tqdm(faculty_data[1:]):
        # -- name
        name = data.find('a').text
        # -- email
        email = data.find_all("td")[2].text
        # -- dblp
        if name in config.AKA.keys():
            # some names are not the same in dblp for some reason
            name = config.AKA[name]
        try:
            dblp_: str = dblp.search(name)[0].homepages[0]
            dblp_site = dblp_.replace("homepages",
                                      "https://dblp.org/pid") + ".html"
        except IndexError as e:
            dblp_site = None
            continue
        # -- drntu
        dr_site = "https://dr.ntu.edu.sg" + data.find('a')['href']
        dr_info = get_info(dr_site)
        # -- personal website (if any)
        personal_web = dr_info.find_all("div", id=config.WEBSITE)
        # -- biography
        biography = dr_info.find_all("div", id="biographyDiv")
        # -- grants
        try:
            grants_ = dr_info.find_all("div", id="currentgrantsDiv")
            grants = grants_[0].get_text(separator=';; ').split(";; ")
            grants = list(filter(None, grants))
        except IndexError as e:
            grants = []  # no grants
        time.sleep(10)
        # -- google scholar (citations)
        try:
            author = next(scholarly.search_author(name+', ntu'))
            full_info = scholarly.fill(author)
            full_info['ntu_email'] = email
            full_info['dr_ntu'] = dr_site
            full_info['website'] = (
                personal_web[0].find('a')['href']
                if personal_web[0].find('a') else None
                    )
            full_info['dblp'] = dblp_site
            full_info['grants'] = list(filter(lambda item: item[0].isalpha(),
                                              grants))
            full_info['biography'] = biography[0].text
        except StopIteration as e:
            full_info = {
                "name": name,
                "ntu_email": email
            }
            logging.error(f"Could not find {name} in google scholar!")
            pass
        # -- write all information to JSON file
        with open(
                   f'src/backend/data/{name.replace(" ", "_")}.json', 'w'
                 ) as out_file:
            out_file.write(json.dumps(full_info))


def get_info(url) -> BeautifulSoup:
    '''
    get website's html using BeautifulSoup
    '''
    page = requests.get(url)
    info = BeautifulSoup(page.text, 'html.parser')
    return info
