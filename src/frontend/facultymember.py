from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FacultyMember:
    name: str
    url_picture: str
    email: str
    dr_ntu: str
    website: str
    dblp: str
    citedby: str
    biography: str
    interests: List[str]
    grants: List[str]
    cites_per_year: Dict[str, int]
    coauthors: List[str]
    publications: List[str]

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'email': self.email,
            'dr_ntu': self.dr_ntu,
            'website': self.website,
            'dblp': self.dblp,
            'citations': self.citedby,
            'biography': self.biography,
            'research_interests': self.interests,
            'grants': self.grants
        }

    def interest_check(self, interest: str) -> bool:
        if interest in self.interests:
            return True
