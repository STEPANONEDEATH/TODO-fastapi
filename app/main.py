import asyncio
from fastapi import FastAPI, WebSocket
from .database import engine, Base, AsyncSessionLocal
from .routers import tasks
from .websocket import manager
from .background import periodic_task

app = FastAPI()
app.include_router(tasks.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = AsyncSessionLocal()
    asyncio.create_task(periodic_task(db))

@app.websocket("/ws/tasks")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(data)
    except:
        manager.disconnect(ws)