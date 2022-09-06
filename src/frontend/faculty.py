from dataclasses import dataclass, field
from typing import List

import pandas as pd

from .facultymember import FacultyMember


@dataclass
class Faculty:
    faculty_list: List[FacultyMember] = field(default_factory=list)

    def append(self, faculty_member: FacultyMember):
        self.faculty_list.append(faculty_member)
    # def p(self):
    #     for i in self.faculty_list:
    #         print(i.name)

    def links(self) -> List[str]:
        return ["http://127.0.0.1:5000/profile/" +
                f"{faculty.name.replace(' ', '+')}"
                for faculty in self.faculty_list]

    def get_member(self, name: str):
        # need to check for exception
        return [faculty for faculty in self.faculty_list
                if faculty.name == name][0]

    def to_dataframe(self):
        return pd.DataFrame.from_records([
            member.to_dict() for member in self.faculty_list
                                         ])
