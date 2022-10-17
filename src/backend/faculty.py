from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from .facultymember import FacultyMember

SPLIT = ",|-"


@dataclass
class Faculty:
    faculty_list: List[FacultyMember] = field(default_factory=list)

    def extend(self, faculty_member: FacultyMember):
        '''
        Appends a single instance of faculty member to
        list of faculty
        '''
        self.faculty_list.extend(faculty_member)

    def links(self) -> List[str]:
        '''
        returns the url of a single faculty member's profile
        '''
        return [faculty.link for faculty in self.faculty_list]

    @property
    def citations(self) -> List[int]:
        '''
        returns the number of citations of faculty members in the form:
        [citedby1: int, ...]
        '''
        print([faculty.citedby for faculty in self.faculty_list])
        return [faculty.citedby for faculty in self.faculty_list]

    @property
    def publications(self) -> List[int]:
        '''
        returns length of publications of faculty members in the form:
        [len(pub1): int, ...]
        '''
        return [len(faculty.publications) for faculty in self.faculty_list]

    @property
    def faculty(self) -> List[str]:
        '''
        returns name of all faculty members in the form:
        [name1: str, ...]
        '''
        return [faculty.name for faculty in self.faculty_list]

    @property
    def grants(self) -> List[int]:
        '''
        returns number of grants of all faculty members in the form:
        [no_grants1: int, ...]
        '''
        return [len(faculty.grants) for faculty in self.faculty_list]

    @property
    def interests(self) -> List[str]:
        '''
        returns list of all unique interests of faculty members
        '''
        return list(set((i for f in self.faculty_list for i in f.interests)))

    def unique_interest(self) -> Dict[str, List[FacultyMember]]:
        '''
        returns dictionary in the form of
        {"edge ai": [FacultyMember(Tim), ...], ...}
        '''
        interest = {k: [] for k in self.interests}
        # loop through all faculty member
        for f in self.faculty_list:
            # loop through all interests
            for i in f.interests:
                if i in interest:
                    temp = interest.get(i)
                    temp.append(f)
                    interest[i] = temp
        return interest

    def recommend_grants(self, interest: str) -> List[str]:
        '''
        recommend grants based on faculty member sharing interests
        '''
        interests = self.unique_interest()
        fmembers = interests.get(interest)
        grants = set((g for f in fmembers for g in f.grants))
        return list(grants)

    def get_member(self, name: str) -> FacultyMember:
        '''
        get FacultyMember object using name
        '''
        try:
            member = [faculty for faculty in self.faculty_list
                      if faculty.name == name][0]
        except Exception as e:
            logging.error(f"{name} not in faculty list")
            return None
        return member

    def set_pub(self, name1: str, name2: str) -> Set[str]:
        '''
        returns common publications between 2 faculty members, given name.
        '''
        member1, member2 = self.get_member(name1), self.get_member(name2)
        return set(
                    member1.published()
                  ).intersection(set(member2.published()))

    def filter_authors(self) -> None:
        '''
        remove co-authors not in NTU
        '''
        members = [faculty.name for faculty in self.faculty_list]
        remove = []
        # loop through all faculty members
        for f in self.faculty_list:
            # loop through their coauthors
            for coauthor in f.coauthors:
                if coauthor not in members:
                    remove.append(coauthor)
            f.coauthors = [x for x in f.coauthors if x not in remove]

    def find_all(self, query_type: str, query: str) -> List[FacultyMember]:
        """find FacultyMembers with queried parameters

        Args:
            query_type (str): interests/grants etc,..
            query (str): keywords
        """
        fac = []
        query = query.lower()
        if query_type == "Citations":
            newy, newc = cits_query(query)
        for fm in self.faculty_list:
            func = getattr(fm, f'match_{query_type.lower()}')
            if query_type == "Citations":
                res = func(year_range=newy, cits_range=newc)
            else:
                res = func(query)
            if res:
                fac.append(fm)
        return fac


def cits_query(query: str) -> Tuple[List[int], List[int]]:
    """
    format citation queries for faculty member objs
    """
    query = query.replace(" ", "")  # remove any whitespace
    try:
        # extract year range and cit range
        year, cits = query.split("/")
        # only extract digits/range
        # e.g. yearr: ["2013", "2017"]
        # e.g. range: [">1000"]
        yearr = re.split(SPLIT, year)
        range = re.split(SPLIT, cits)
        if ((len(yearr) != 1 or len(yearr) != 2) and
           (len(range) != 1 or len(range) != 2)):
            raise ValueError("No such years and citation range,"
                             "try again.")
    except Exception as e:
        logging.error(f"Error is {e.args}")

    newy = []
    newc = []

    try:
        if len(yearr) == 2:  # check year range
            newy.extend(yearr)
        if len(range) == 2:  # check citations range
            newc.extend(range)
        if len(yearr) == 1:
            # check valid ranges
            if not (yearr[0].isnumeric() or
                    ">" in yearr[0] or
                    "<" in yearr[0]):
                raise ValueError("Year is wrong.")
            # edit ranges
            elif ">" in yearr[0]:
                yearr.insert(1, 4000)
                yearr[0] = re.sub('[^0-9]', '', yearr[0])
            elif "<" in yearr[0]:
                yearr.insert(0, 0)
                yearr[1] = re.sub('[^0-9]', '', yearr[1])
            newy.extend(yearr)
        if len(range) == 1:
            if not (range[0].isnumeric() or
                    ">" in range[0] or
                    "<" in range[0]):
                raise ValueError("Citations are wrong.")
            elif ">" in range[0]:
                range.insert(1, 100000)
                range[0] = re.sub('[^0-9]', '', range[0])
            elif "<" in range[0]:
                range.insert(0, 0)
                range[1] = re.sub('[^0-9]', '', range[1])
            newc.extend(range)
        newy, newc = sorted(map(int, newy)), sorted(map(int, newc))
    except Exception as e:
        logging.error(f"Error is {e.args}")
    return newy, newc
