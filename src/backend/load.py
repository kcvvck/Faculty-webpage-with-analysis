import json
import os

from config import config
from backend.faculty import Faculty
from backend.facultymember import FacultyMember


def load_in(dir: str) -> Faculty:
    """
    Read in records as Faculty Members
    """
    all_members = Faculty()
    for f in os.listdir(dir):
        with open(os.path.join(dir, f), 'r') as out:
            info = json.load(out)
            # -- clean coauthors
            coauthors = [c["name"] for c in info["coauthors"]]
            # -- clean publications
            publications = [
                            [c["bib"]["title"],
                             c["bib"]["pub_year"],
                             c["num_citations"]]
                            for c in info["publications"]
                            if c["num_citations"] > 0
                            and "pub_year" in c["bib"]
                           ]
            all_members.append(
                FacultyMember(name=info["name"],
                              urlpicture=info["url_picture"],
                              email=info["ntu_email"],
                              drntu=info["dr_ntu"],
                              website=info["website"],
                              dblp=info["dblp"],
                              citedby=info["citedby"],
                              biography=info["biography"],
                              interests=info["interests"],
                              grants=info["grants"],
                              citesperyear=info["cites_per_year"],
                              coauthors=coauthors,
                              publications=publications
                              ))
    return all_members


db = load_in(config.DATA_FILE)
