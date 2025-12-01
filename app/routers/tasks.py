from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import AsyncSessionLocal
from .. import schemas, crud
from ..background import background_task

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@router.get("/tasks")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db)

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    return task

@router.post("/tasks")
async def create_task(data: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, data)

@router.patch("/tasks/{task_id}")
async def update_task(task_id: int, data: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    return await crud.update_task(db, task, data)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    await crud.delete_task(db, task)
    return {"status": "deleted"}

@router.post("/task-generator/run")
async def run_generator(db: AsyncSession = Depends(get_db)):
    await background_task(db)
    return {"status": "started"}