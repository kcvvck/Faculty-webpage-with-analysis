from dataclasses import dataclass, field
import logging
from typing import Dict, List, Set

import pandas as pd

from .facultymember import FacultyMember


@dataclass
class Faculty:
    faculty_list: List[FacultyMember] = field(default_factory=list)
    # u_interest: List[str] = field(default_factory=list)

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

    @property
    def interests(self) -> List[str]:
        return set((i for f in self.faculty_list for i in f.interests))

    def unique_interest(self) -> Dict[str, FacultyMember]:
        # print("wewqeqw")
        interest = {k: [] for k in self.interests}
        for f in self.faculty_list:
            for i in f.interests:
                if i in interest:
                    temp = interest.get(i)
                    temp.append(f)
                    interest[i] = temp
        return interest

    def recommend_grants(self, interest: str) -> List[str]:
        # print("RUNNIdsdasdadasdasdadasdNG&")
        # avail_grants = set()
        interests = self.unique_interest()
        # for i in interest_list:
        fmembers = interests.get(interest)
        grants = set((g for f in fmembers for g in f.grants))
        # avail_grants.update(grants)
        return list(grants)

    def get_member(self, name: str) -> FacultyMember:
        try:
            member = [faculty for faculty in self.faculty_list
                      if faculty.name == name][0]
        except Exception as e:
            logging.error(f"{name} not in faculty list")
            return None
        return member

    def set_pub(self, name1: str, name2: str) -> Set[str]:
        member1, member2 = self.get_member(name1), self.get_member(name2)
        return set(
                    member1.published()
                  ).intersection(set(member2.published()))

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
