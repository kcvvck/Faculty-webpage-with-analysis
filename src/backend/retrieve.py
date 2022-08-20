from dataclasses import dataclass, field
import time
from typing import List

import dblp
import validators

from .faculty import Faculty
from .facultymember import FacultyMember
from .utils import *
from config import config
from tqdm import tqdm

from scholarly import scholarly
from scholarly import ProxyGenerator

'''
TODO clean up code
TODO add logging for errors
TODO pytest check
TODO check and validate record kind of like cleaning data
TODO put this on jupyter
'''

pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

@dataclass
class Retrieve:
    urls: List[str]
    tag: str
    class_: str
    faculty: Faculty = field(default_factory=Faculty)
    
    def __post_init__(self) -> None:
        for url in self.urls:
            if not validators.url(url):
                raise Exception("Invalid URL.")
        
    def retrieve_info(self) -> Faculty:
        all_staffs: List[FacultyMember] = []
        for url in self.urls:
            all_staffs.extend(get_dr_ntu(url))
        return Faculty(faculty_list=all_staffs)

def get_dr_ntu(url) -> List[FacultyMember]:
    faculty: List[FacultyMember] = []
    all_info = get_info(url)
    faculty_list = all_info.find("table", attrs={"class": "table table-hover"})
    faculty_data = faculty_list.find_all("tr")
    for data in tqdm(faculty_data[1:]):
        name = data.find('a').text
        email = data.find_all("td")[2].text
        if name in config.AKA.keys():  # some names are not the same in dblp for some reason
            name = config.AKA[name]
        try:
            dblp_: str = dblp.search(name)[0].homepages[0]
            dblp_site = dblp_.replace("homepages", "https://dblp.org/pid") + ".html"
        except IndexError as e:
            dblp_site = None
            continue;
        dr_site = "https://dr.ntu.edu.sg" + data.find('a')['href']
        # ----
        dr_info = get_info(dr_site)
        personal_web = dr_info.find_all("div", id=config.WEBSITE)
        # -----
        time.sleep(5)
        search_query = scholarly.search_author(name+', ntu')
        time.sleep(5)
        try:
            first_author_result = next(search_query)
            total_cites = first_author_result['citedby']
        except StopIteration as e:
            total_cites = None
        # -----
        faculty.append(FacultyMember(
            name=name,
            email=email,
            dr_ntu=dr_site,
            website=(personal_web[0].find('a')['href'] if personal_web[0].find('a') else None),
            dblp=dblp_site,
            citations=total_cites
                                    ))
    return faculty




