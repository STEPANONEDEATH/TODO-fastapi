import httpx
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Task

async def fetch_task():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return r.json()

async def background_task(db: AsyncSession):
    data = await fetch_task()
    task = Task(
        title=data["title"],
        description="from api",
        completed=data["completed"]
    )
    db.add(task)
    await db.commit()

async def periodic_task(db: AsyncSession):
    while True:
        await background_task(db)
        await asyncio.sleep(20)