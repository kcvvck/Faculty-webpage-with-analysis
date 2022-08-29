from dataclasses import dataclass


@dataclass
class FacultyMember:
    name: str
    email: str
    dr_ntu: str
    website: str
    dblp: str
    citations: str

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'dr_ntu': self.dr_ntu,
            'website': self.website,
            'dblp': self.dblp,
            'citations': self.citations
        }
