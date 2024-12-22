from fastapi import APIRouter, HTTPException
from repository import customer_repository
from repository import user_repository
from model.customer import Customer
from model.customer_order_request import CustomerOrderRequest
from model.customer_order_response import CustomerOrderResponse

from database import  database

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
async def get_users():
    return await user_repository.get_all()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    customer = await customer_repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with id: {customer_id} not found")
    return customer

@router.post("/")
async def create_customer(customer: Customer):
    return await customer_repository.create_customer(customer)


@router.post("/x")
async def x(obj: CustomerOrderRequest):
    q = "SELECT * FROM customer"
    return await database.fetch_all(q)