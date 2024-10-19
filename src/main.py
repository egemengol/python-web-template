from typing_extensions import Annotated
from fastapi import Depends, FastAPI
import asyncpg
import os
from typing import AsyncGenerator, Any

app = FastAPI()

async def db_pool():
    dsn = os.environ["DATABASE_URL"]
    async with asyncpg.create_pool(dsn) as pool:
        yield pool

async def db_conn(db_pool: Annotated[asyncpg.Pool, Depends(db_pool)]):
    async with db_pool.acquire() as conn:
        conn: asyncpg.Connection
        yield conn


@app.get("/")
async def root(db_pool:Annotated[asyncpg.Pool, Depends(db_pool)]):
    async with db_pool.acquire() as conn:
        conn: asyncpg.Connection
        rows = await conn.fetch("SELECT id FROM my_table")
        for r in rows:
            print(r[0])
    return {"message": "Hello World"}
