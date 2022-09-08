from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FacultyMember:
    name: str
    urlpicture: str
    email: str
    drntu: str
    website: str
    dblp: str
    citedby: str
    biography: str
    interests: List[str]
    grants: List[str]
    citesperyear: Dict[str, int]
    coauthors: List[str]
    publications: List[str]

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'email': self.email,
            'dr_ntu': self.drntu,
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
