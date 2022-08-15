import logging
from dataclasses import dataclass

import validators

from crawl import Crawl
from faculty import Faculty
from facultymember import FacultyMember
from utils import *


@dataclass
class Retrieve:
    url: str
    tag: str
    class_: str
    
    def __init__(self, url, tag, class_) -> None:
        if not validators.url(url):
            raise Exception("Invalid URL.")
        self.url = url
        self.tag = tag
        self.class_ = class_
        
    def retrieve_info(self):
        faculty = Faculty()
        all_info = Crawl(self.url).get_info()
        faculty_list = all_info.find("table", attrs={"class": "table table-hover"})
        faculty_data = faculty_list.find_all("tr")
        # skip the headings, we will add that later
        for data in faculty_data[1:]:
            dr_site = "https://dr.ntu.edu.sg" + data.find('a')['href']
            dr_info = Crawl(dr_site).get_info()
            personal_web = dr_info.find_all("div", id=WEBSITE)
            faculty.append(FacultyMember(
                name=data.find('a').text,
                email=data.find_all("td")[2].text,
                dr_ntu=dr_site,
                website=(personal_web[0].find('a')['href'] if personal_web[0].find('a') else None),
                dblp=None,
                citations=None
                                        ))
        return faculty
            # except:
        #         TODO faculty member does not have any personal websites!
        #         pass
            # else:
            #     print(personal_web[0])
            #     print(f"{data.find('a').text} does not have a personal website!")
        #             faculty_info[faculty.find('a').text] = faculty.find('a')['href']
        #         else:  # for if faculty does not have a link
        #             # TODO: note thee faculty member down
        #             logging.info(f"{faculty} does not have a link.")
        # except AttributeError as e:
        #     logging.error(f"Exception is {e.args}. Could not find tag {self.tag} with class {self.class_}")
            

f = Retrieve(URL, TAG, CLASS)
fac = f.retrieve_info()
dat = fac.to_dataframe()
print(dat)
