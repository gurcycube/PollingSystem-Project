from database import  database
from typing import List
from model.user import User

async def get_all(response_model=List[User]):
    q = "SELECT * FROM users"
    return await database.fetch_all(q)

async def get_by_id(user_id: int):
    q = "SELECT * FROM users WHERE id=:c_id"
    return await database.fetch_one(q , values={"c_id":user_id})

async def create_user(user: User):
    q = "INSERT INTO users (first_name, last_name,email,age,address,joining_date,is_registered) VALUES (:first_name,:last_name,:email,:age,:address,:joining_date,:is_registered)"
    return await database.execute(q , values={"first_name":user.first_name,
                                              "last_name": user.last_name,
                                              "email":user.email,
                                              "age":user.age,
                                              "address":user.address,
                                              "joining_date":user.joining_date,
                                              "is_registered":user.is_registered} )

async def update_user(user_id: int, user: User):
    q = """
    UPDATE users
    SET first_name = :first_name,
        last_name = :last_name,
        email = :email,
        age = :age,
        address = :address,
        joining_date = :joining_date,
        is_registered = :is_registered
    WHERE id = :user_id
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
        "joining_date": user.joining_date,
        "is_registered": user.is_registered,
        "user_id": user_id
    }
    return await database.execute(q, values=values)
