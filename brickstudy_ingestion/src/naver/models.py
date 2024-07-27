from dataclasses import dataclass, field
from typing import Literal


@dataclass
class NewsApiCharacterSchema:
    title: str
    originallink: str
    link: str
    description: str
    pubDate: str


@dataclass
class NewsApiResponse:
    lastBuildDate: str
    total: int
    start: int
    display: int
    items: NewsApiCharacterSchema

    def __post_init__(self):
        self.items = [NewsApiCharacterSchema(**x) for x in self.items]


@dataclass
class ApiParameters:
    query: str
    display: int = field(default=10)
    start: int = field(default=1)
    sort: Literal["sim", "date"] = field(default="sim")
