from typing import List
from pydantic import BaseModel
from model.customer import Customer
from model.customer_order import CustomerOrder

class CustomerOrderResponse(BaseModel):
    customer: Customer
    customer_orders: List[CustomerOrder]