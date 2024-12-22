from typing import Optional
from pydantic import BaseModel

class CustomerOrder(BaseModel):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    item_name: str
    price: float