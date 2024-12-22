from database import  database
from typing import List
from model.customer import Customer

async def get_all(response_model=List[Customer]):
    q = "SELECT * FROM customer"
    return await database.fetch_all(q)

async def get_by_id(customer_id: int):
    #    q = f"SELECT * FROM customer WHERE id={customer_id}"
    q = "SELECT * FROM customer WHERE id=:c_id"
    return await database.fetch_one(q , values={"c_id":customer_id})


async def create_customer(customer: Customer):
    q = "INSERT INTO customer (first_name, last_name,email) VALUES (:first_name,:last_name,:email)"
    return await database.execute(q , values={"first_name":customer.first_name, "last_name": customer.last_name, "email":customer.email} )