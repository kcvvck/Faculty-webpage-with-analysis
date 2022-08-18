from dataclasses import dataclass, field
from typing import List

import dblp
import validators

from .faculty import Faculty
from .facultymember import FacultyMember
from .utils import *
import regex as re
from config import config

'''
TODO do the next page by changing the webpage
TODO get number of citations  --> have to find anoother way bc i get blocked
TODO clean up code
TODO add logging for errors
TODO pytest check
'''

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
    for data in faculty_data[1:]:
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
        # scholar_html = Crawl(f"http://scholar.google.se/scholar?hl=en&q=${name}").get_info()
        # tables = scholar_html.findAll("table")
        
        total_cites = None
        # if tables:  # get first match
        #     # print(tables[0].text)
        #     cited: str = re.search("Cited by [\d]*", tables[0].text)
        #     print(cited.group(0))
        #     total_cites = (
        #                     [x for x in cited.group(0).split() if x.isdigit()] if cited else None
        #                   )
        #     if not total_cites:
        #         print(f"{name} Does not have citations!")
        # .search('Fetch', tag.text)
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




