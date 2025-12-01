from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Task

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def create_task(db: AsyncSession, data):
    task = Task(**data.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def update_task(db: AsyncSession, task: Task, data):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task: Task):
    await db.delete(task)
    await db.commit()