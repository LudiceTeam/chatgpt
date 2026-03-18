from sqlalchemy import text,select,and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime,timedelta
from typing import List,Literal
from sqlalchemy.orm import sessionmaker
import asyncpg
import os
from dotenv import load_dotenv
from payment_models import metadata_obj,table
import asyncio
import atexit
from sqlalchemy import func
#backend.database.
import uuid 
from typing import Literal


load_dotenv()


async_engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/payment_db",
    pool_size=20,          
    max_overflow=50,        
    pool_recycle=3600,      
    pool_pre_ping=True,     
    echo=False
)



AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def drop_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)



async def create_payment(price:int,user_id:str) -> str:
    payment_id = str(uuid.uuid4())
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            stmt = table.insert().values(
                payment_id = payment_id,
                user_id = user_id,
                status = "pending",
                price = price
            )
            await conn.execute(stmt)
            return payment_id

async def get_payment_status(payment_id:str) -> str:
    async with AsyncSession(async_engine) as conn:
        stmt = select(table.c.status).where(table.c.payment_id == payment_id)
        res = await conn.execute(stmt)
        data = res.scalar_one_or_none()
        return data

async def change_payment_state(payment_id:str,new_status:str = Literal["paid","failed","canceled"]):
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            stmt = table.update().where(table.c.payment_id == payment_id).values(
                status = new_status
            )
            await conn.execute(stmt)

            
async def get_payment_by_id(payment_id:str) -> dict[str,str] | dict:
    async with AsyncSession(async_engine) as conn:
        stmt = select(table.c.user_id,
                      table.c.status,
                      table.c.price
                      ).where(table.c.payment_id == payment_id)
        
        res = await conn.execute(stmt)
        data = res.fetchone()

        if not data:
            return {}

        user_id,status,price = data

        return {
            "payment_id":payment_id,
            "user_id":user_id,
            "status":status,
            "price":price
        }


