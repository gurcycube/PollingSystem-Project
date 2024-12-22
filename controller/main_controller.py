import json

from fastapi import APIRouter, HTTPException
from repository import customer_repository
from model.customer import Customer
from model.customer_order import CustomerOrder
from model.customer_order_request import CustomerOrderRequest
from model.customer_order_response import CustomerOrderResponse
from typing import List
import httpx
from database import  database
from repository.cache_repository import CacheRepository

router = APIRouter(
    #prefix="/",
    tags=["main"]
)

cache_repo = CacheRepository(ttl=3600)


@router.get("/customer/{customer_id}" , response_model=Customer)
async def get_customer_by_id(customer_id: int):
    # check if exists in cache
    if cache_repo.exists(str(customer_id)):
        # load from cache, and convert from json to dictionary
        customer_data = json.loads( cache_repo.get(str(customer_id)) )

        # unpacking customer_data to params (key=value , key=value....)
        return Customer(**customer_data)
    else:

        q = "SELECT * FROM customer WHERE id=:c_id"
        customer = await database.fetch_one(q, values={"c_id": customer_id})
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer with id: {customer_id} not found")

        # save to cache
        c = Customer(**customer)
        cache_repo.set(str(customer_id) ,c.json() )
        return customer


# create a new customer
@router.post("/customer")
async def create_new_customer(customer: Customer):
    q = "INSERT INTO customer (first_name,last_name,email) VALUES(:first_name,:last_name,:email) "
    return await database.execute(q, values={"first_name": customer.first_name, "last_name":customer.last_name, "email": customer.email} )


# update a  customer by id
@router.post("/customer/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    q = """
    UPDATE customer SET
        first_name=:first_name,
        last_name=:last_name,
        email=:email
    WHERE id=:customer_id
    """
    return await database.execute(q, values={"customer_id": customer_id  ,  "first_name": customer.first_name, "last_name":customer.last_name, "email": customer.email} )


# new customer order
@router.post("/customer_order")
async def create_new_customer_order(customer_order: CustomerOrder):
    q = """
        INSERT INTO customer_order 
        (customer_id,item_name,price) 
        VALUES
        (:customer_id,:item_name,:price)
    """
    return await database.execute(q, values={"customer_id": customer_order.customer_id, "item_name":customer_order.item_name, "price": customer_order.price} )


# get all customer orders
@router.get("/customer_order")
async def get_all_customer_orders():
    q = """
    
    SELECT *,  
            customer_order.id AS order_id, 
            customer_id AS customer_id
        FROM 
            customer_order LEFT JOIN customer 
        ON 
            customer_order.customer_id = customer.id
    """
    return await database.fetch_all(q)

# get  customer  orders by id
@router.get("/customer/{customer_id}/orders" , response_model=CustomerOrderResponse)
async def get_customer_order_by_customer_id(customer_id: int):

    # get customer info
    customer = await get_customer_by_id(customer_id)

    # get orders
    q = """
       SELECT *
           FROM 
               customer_order 
            WHERE customer_order.customer_id=:customer_id
       """
    customer_orders = await database.fetch_all(q, values={"customer_id":customer_id})

    response = CustomerOrderResponse(customer=customer , customer_orders=customer_orders)

    return response



# new customer order
@router.post("/customer_order_bulk")
async def create_new_customer_order_bulk(customer_orders: List[CustomerOrder]):

    async with database.transaction():
        for customer_order in customer_orders:
            q = """
                INSERT INTO customer_order 
                (customer_id,item_name,price) 
                VALUES
                (:customer_id,:item_name,:price)
            """
            await database.execute(q, values={"customer_id": customer_order.customer_id, "item_name": customer_order.item_name,
                                        "price": customer_order.price})
            # בכוונה שאילתא שלא אמורה לעבוד
            q = """
                       INSERT INTO moshe_table 
                       (customer_id,item_name,price) 
                       VALUES
                       (1,1,1)
                   """
            await database.execute(q)

    return True


# update order by id (update only item name and price)
# update a  customer_order by id
@router.post("/customer_order/{customer_order_id}")
async def update_customer_order(customer_order_id: int, customer_order: CustomerOrder):
    q = """
    UPDATE customer_order SET
        item_name=:item_name,
        price=:price 
    WHERE id=:customer_order_id
    """
    return await database.execute(q, values={"customer_order_id":customer_order_id, "item_name": customer_order.item_name  ,  "price": customer_order.price} )

# {"id":30,"url":"https://www.tvmaze.com/shows/30/american-horror-story","name":"American Horror Story","type":"Scripted","language":"English","genres":["Drama","Horror","Thriller"],"status":"Running","runtime":60,"averageRuntime":61,"premiered":"2011-10-05","ended":null,"officialSite":"http://www.fxnetworks.com/shows/american-horror-story","schedule":{"time":"22:00","days":["Wednesday"]},"rating":{"average":7.5},"weight":99,"network":{"id":13,"name":"FX","country":{"name":"United States","code":"US","timezone":"America/New_York"},"officialSite":null},"webChannel":null,"dvdCountry":null,"externals":{"tvrage":28776,"thetvdb":250487,"imdb":"tt1844624"},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_portrait/473/1183640.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/473/1183640.jpg"},"summary":"<p><b>American Horror Story </b>is an horror television anthology series. Each season is conceived as a self-contained miniseries, following a disparate set of characters and settings, and a storyline with its own beginning, middle, and end. While some actors appear for more than one year, they play completely different roles in each season.</p>","updated":1722222153,"_links":{"self":{"href":"https://api.tvmaze.com/shows/30"},"previousepisode":{"href":"https://api.tvmaze.com/episodes/2766867","name":"The Auteur"}}}

@router.get("/httpx/{show_id}")
async def get_show_details(show_id):
    try:
        TV_MAZE_BASE_URL = "https://api.tvmaze.com"
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TV_MAZE_BASE_URL}/shows/{show_id}")
            data = response.json()
            return data.get('image',{} ).get('original')
    except httpx.HTTPStatusError as e:
        print(f"cannot fetch show {show_id} : {e}")
        return None

# /search/shows?q=:query


@router.get("/search/{query}")
async def search_tvmaze(query):
    try:
        TV_MAZE_BASE_URL = "https://api.tvmaze.com"
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TV_MAZE_BASE_URL}/search/shows?q={query}")
            data = response.json()
            shows = []
            for dict in data:
                shows.append(dict.get('show',{}).get('name'))
            return shows
    except httpx.HTTPStatusError as e:
        print(f"cannot fetch show {query} : {e}")
        return None


@router.get("/service")
async def use_service():
    try:
        url = "http://127.0.0.1:8001/user"
        async with httpx.AsyncClient() as client:
            params = {"name":"bill gates"}
            response = await client.post(url, json=params)
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"cannot fetch: {e}")
        return None

# get  customer  orders by id
@router.get("/customer/{customer_id}/summary")
async def get_customer_order_summary_by_customer_id(customer_id: int):

    # get orders
    q = """
       SELECT sum(price) as total_price ,count(id) as amount
           FROM 
               customer_order 
            WHERE customer_order.customer_id=:customer_id
       """
    customer_orders = await database.fetch_all(q, values={"customer_id":customer_id})

    return customer_orders



@router.post("/cache/set")
def set_cache(key: str, value: str):
    return cache_repo.set(key, value)

@router.get("/cache/get")
def get_cache(key: str):
    return {"key": key, "value": cache_repo.get(key)}
