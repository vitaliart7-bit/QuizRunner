from dataclasses import field,dataclass
from typing import List,Optional


@dataclass

class Choice:
  text: str
  is_correct: bool
  id: Optional[int] = None


@dataclass

class Question:
  text: str
  choices: List[Choice] = field(default_factory=list)
  id: Optional[int] = None


@dataclass

class TestSet:
  title: str
  description: Optional[str] = ""
  questions: List[Question] = field(default_factory=list)
  id: Optional[int] = None
