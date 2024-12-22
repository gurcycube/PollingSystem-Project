from typing import Optional
from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    age: str
    address: str
    joining_date: datetime
    is_registered: bool

