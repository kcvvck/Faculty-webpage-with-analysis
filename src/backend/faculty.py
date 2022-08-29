from dataclasses import dataclass, field
from typing import List

import pandas as pd

from .facultymember import FacultyMember


@dataclass
class Faculty:
    faculty_list: List[FacultyMember] = field(default_factory=list)

    def append(self, faculty_member: FacultyMember):
        self.faculty_list.append(faculty_member)

    def to_dataframe(self):
        return pd.DataFrame.from_records([
            member.to_dict() for member in self.faculty_list
                                         ])
