from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FacultyMember(dict):
    '''
    Class for faculty member object
    '''
    name: str
    email: str
    urlpicture: str = None
    drntu: str = None
    website: str = None
    dblp: str = None
    citedby: str = None
    biography: str = None
    interests: List[str] = field(default_factory=list)
    grants: List[str] = field(default_factory=list)
    citesperyear: Dict[str, int] = field(default_factory=lambda: defaultdict(dict))
    coauthors: List[str] = field(default_factory=list)
    publications: List[str] = field(default_factory=list)

    def __post_init__(self):
        '''
        Converts all interests strings to lower
        '''
        self.interests = [i.lower() for i in self.interests]

    def published(self) -> List[str]:
        '''
        returns name of all publications
        '''
        return [pubs[0] for pubs in self.publications]
