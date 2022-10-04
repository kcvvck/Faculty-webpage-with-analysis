from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FacultyMember(dict):
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

    def __post_init__(self):
        self.interests = [i.lower() for i in self.interests]

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

    def published(self) -> List[str]:
        return [info[0] for info in self.publications]

    def interest_check(self, interest: str) -> bool:
        if interest in self.interests:
            return True
