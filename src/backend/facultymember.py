from dataclasses import dataclass
from typing import Dict


@dataclass
class FacultyMember:
    name: str
    email: str
    dr_ntu: str
    website: str
    dblp: str
    # citations: Dict[str, int]
    citations: str

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'dr_ntu': self.dr_ntu,
            'website': self.website,
            'dblp': self.dblp,
            # 'citations': sum((self.citations).values())
            'citations': self.citations
        }
