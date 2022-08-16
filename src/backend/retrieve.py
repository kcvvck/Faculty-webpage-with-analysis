from dataclasses import dataclass, field

import dblp
import validators

from crawl import Crawl
from faculty import Faculty
from facultymember import FacultyMember
from utils import *

'''
TODO do the next page by changing the webpage
TODO get number of citations
TODO clean up code
TODO add logging for errors
TODO pytest check
'''

@dataclass
class Retrieve:
    url: str
    tag: str
    class_: str
    faculty: Faculty = field(default_factory=Faculty)
    
    def __post_init__(self) -> None:
        if not validators.url(self.url):
            raise Exception("Invalid URL.")
        
    def retrieve_info(self):
        count = 0
        all_info = Crawl(self.url).get_info()
        faculty_list = all_info.find("table", attrs={"class": "table table-hover"})
        faculty_data = faculty_list.find_all("tr")
        # skip the headings, we will add that later
        for data in faculty_data[1:]:
            name = data.find('a').text
            email = data.find_all("td")[2].text
            if name in AKA.keys():  # some names are not the same in dblp for some reason
                name = AKA[name]
            try:
                dblp_: str = dblp.search(name)[0].homepages[0]
            except IndexError as e:
                print(name)
                break;
            dblp_site = dblp_.replace("homepages", "https://dblp.org/pid") + ".html"
            dr_site = "https://dr.ntu.edu.sg" + data.find('a')['href']
            # ----
            dr_info = Crawl(dr_site).get_info()
            personal_web = dr_info.find_all("div", id=WEBSITE)
            # -----
            self.faculty.append(FacultyMember(
                name=name,
                email=email,
                dr_ntu=dr_site,
                website=(personal_web[0].find('a')['href'] if personal_web[0].find('a') else None),
                dblp=dblp_site,
                citations=None
                                        ))
            

f = Retrieve(URL, TAG, CLASS)
f.retrieve_info()
dat = f.faculty.to_dataframe()
print(dat)
