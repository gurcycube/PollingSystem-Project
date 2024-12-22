from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database
from controller import customer_controller,main_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(customer_controller.router)
app.include_router(main_controller.router)