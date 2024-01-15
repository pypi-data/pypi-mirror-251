from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Personality:
    """Personality type based on the Myers-Briggs Type Indicator (MBTI)"""
    extroversion: float
    introversion: float
    sensing: float
    intuition: float
    thinking: float
    feeling: float
    judging: float
    perceiving: float


@dataclass
class Person:
    id: str
    born: date
    personality: Personality
    interests: List[str]
    adopted: float

    def __repr__(self):
        return self.adopted


class Contagious:
    """Contagious type based on the Contagious: Why Things Catch On book"""
    social_currency: float
    triggers: float
    emotion: float
    public: float
    practical_value: float
    stories: float


@dataclass
class Meme:
    """A unit of cultural information based on Dawkin's definition"""
    id: str
    description: str
    tags: List[str]


if __name__ == "__main__":
    p = Person("1", 20, ["music", "sports"])
    print(p)
