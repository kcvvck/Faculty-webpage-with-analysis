from dataclasses import dataclass, field
import logging
from typing import List

import pandas as pd

from .facultymember import FacultyMember


@dataclass
class Faculty:
    faculty_list: List[FacultyMember] = field(default_factory=list)

    def append(self, faculty_member: FacultyMember):
        self.faculty_list.append(faculty_member)

    def links(self) -> List[str]:
        return ["http://127.0.0.1:5000/profile/" +
                f"{faculty.name.replace(' ', '+')}"
                for faculty in self.faculty_list]

    @property
    def citations(self) -> List[int]:
        return [faculty.citedby for faculty in self.faculty_list]

    @property
    def publications(self) -> List[int]:
        return [len(faculty.publications) for faculty in self.faculty_list]

    @property
    def faculty(self) -> List[str]:
        return [faculty.name for faculty in self.faculty_list]

    @property
    def grants(self) -> List[int]:
        return [len(faculty.grants) for faculty in self.faculty_list]

    def get_member(self, name: str) -> FacultyMember:
        # need to check for exception
        # l = [faculty.name for faculty in self.faculty_list]
        # print(l)
        try:
            member = [faculty for faculty in self.faculty_list
                      if faculty.name == name][0]
        except Exception as e:
            logging.error(f"{name} not in faculty list")
            return None
        return member

    def set_pub(self, name1: str, name2: str):
        member1, member2 = self.get_member(name1), self.get_member(name2)
        return set(
                    member1.publications
                  ).intersection(set(member2.publications))

    def filter_authors(self) -> None:
        members = [faculty.name for faculty in self.faculty_list]
        remove = []
        for f in self.faculty_list:
            for coauthor in f.coauthors:
                if coauthor not in members:
                    remove.append(coauthor)
            f.coauthors = [x for x in f.coauthors if x not in remove]

    def to_dataframe(self):
        return pd.DataFrame.from_records([
            member.to_dict() for member in self.faculty_list
                                         ])
