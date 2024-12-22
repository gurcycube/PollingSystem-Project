from pydantic import BaseModel
from model.customer import Customer
from model.customer_order import CustomerOrder

class CustomerOrderRequest(BaseModel):
    customer: Customer
    customer_order: CustomerOrder