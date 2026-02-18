from dataclasses import field,dataclass
from typing import List,Optional


@dataclass

class Choice:
  text: str
  is_correct: bool


@dataclass

class Question:
  text: str
  choices: List[Choice] = field(default_factory=list)


@dataclass

class TestSet:
  title: str
  description: Optional[str] = ""
  quiestions: List[Question] = field(default_factory=list)
