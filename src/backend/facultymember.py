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
    citedby: int = field(default=0)
    biography: str = field(default="")
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

    @property
    def link(self):
        return f"http://127.0.0.1:5000/profile/{self.name.replace(' ', '+')}"

    def published(self) -> List[str]:
        '''
        returns name of all publications
        '''
        return [pubs[0] for pubs in self.publications]

    def match_interests(self, query: str) -> bool:
        for i in self.interests:
            if query in i.lower():
                return True
        return False

    def match_grants(self, query: str) -> bool:
        for i in self.grants:
            if query in i.lower():
                return True
        return False

    def match_publications(self, query: str) -> bool:
        for i in self.publications:
            if query in i[0].lower():
                return True
        return False

    def match_citations(self, **kwargs) -> bool:
        year_range: List[int] = kwargs["year_range"]
        cits_range: List[int] = kwargs["cits_range"]
        sum = 0
        for i in self.citesperyear.keys():
            # only looking at 1 year
            # not outside bc year may or may not exist.
            if len(year_range) == 1:
                if int(i) == year_range[0]:
                    sum += self.citesperyear[i]
            elif len(year_range) == 2:
                if (int(i) > year_range[0] and int(i) < year_range[1]):
                    sum += self.citesperyear[i]
        # if only looking at 1 target citation value
        if len(cits_range) == 1:
            if sum == cits_range[0]:
                return True
        elif len(cits_range) == 2:
            if (sum > cits_range[0] and sum < cits_range[1]):
                return True
        return False
