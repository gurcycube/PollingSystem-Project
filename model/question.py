from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    id: Optional[int] = None
    question_title: str
    a1: str
    a2: str
    a3: str
    a4: str
    

