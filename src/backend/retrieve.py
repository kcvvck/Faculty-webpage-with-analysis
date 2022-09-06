import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import dblp
import validators
from config import config
from scholarly import ProxyGenerator, scholarly
from tqdm import tqdm

# from .faculty import Faculty
# from .facultymember import FacultyMember
from .utils import *

pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)


@dataclass
class Retrieve:
    urls: List[str]
    tag: str
    class_: str
    # faculty: Faculty = field(default_factory=Faculty)

    def __post_init__(self) -> None:
        for url in self.urls:
            if not validators.url(url):
                raise Exception("Invalid URL.")

    def retrieve_info(self):
        Path(config.DATA_FILE).mkdir(exist_ok=True)
        for url in self.urls:
            get_dr_ntu(url)


def get_dr_ntu(url):
    count = 0
    all_info = get_info(url)
    faculty_list = all_info.find("table", attrs={"class": "table table-hover"})
    faculty_data = faculty_list.find_all("tr")
    for data in tqdm(faculty_data[1:]):
        count = count + 1
        name = data.find('a').text
        email = data.find_all("td")[2].text
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
        dr_site = "https://dr.ntu.edu.sg" + data.find('a')['href']
        # ----
        dr_info = get_info(dr_site)
        personal_web = dr_info.find_all("div", id=config.WEBSITE)
        biography = dr_info.find_all("div", id="biographyDiv")
        grants = dr_info.find_all("div", id="currentgrantsDiv")
        grants_ = grants[0].get_text(separator=';; ').split(";; ")
        # -----
        time.sleep(10)
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
            full_info['grants'] = list(filter(None, grants_))
            full_info['biography'] = biography[0].text
        except StopIteration as e:
            full_info = {
                "name": name,
                "email": email
            }
            logging.error(f"Could not find {name} in google scholar!")
            pass
        with open(f'data/{name.replace(" ", "_")}.json', 'w+') as out_file:
            out_file.write(json.dumps(full_info))
        if count == 2:
            break
