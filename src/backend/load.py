import json
import os
import pickle
from typing import List

from config import config

from backend.faculty import Faculty
from backend.facultymember import FacultyMember


def load_in(dir: str) -> Faculty:
    """
    Read in records as Faculty Members
    """
    all_members = []
    for f in os.listdir(dir):
        if f.endswith(".json"):
            with open(os.path.join(dir, f), 'r') as out:
                info = json.load(out)
                try:
                    # -- clean coauthors
                    coauthors = [c["name"] for c in info["coauthors"]]
                    # -- clean publications
                    # [title, year, citations]
                    publications = [
                                    [c["bib"]["title"],
                                     c["bib"]["pub_year"],
                                     c["num_citations"]]
                                    for c in info["publications"]
                                    if c["num_citations"] > 0
                                    and "pub_year" in c["bib"]
                                    and c["bib"]["title"].encode(
                                        'ascii', errors='ignore'
                                        )
                                ]
                    # -- append as objects
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
                except Exception as e:
                    # -- if information not fully retrieved
                    all_members.append(
                        FacultyMember(name=info["name"],
                                      email=info["ntu_email"],
                                      ))
    return all_members


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    db: List[FacultyMember] = load_in(config.DATA_FILE)
    save_object(db, 'faculty.pkl')
