from fastapi import FastAPI
from db import api
from db.database import init_db, close_db
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield
    close_db()  

app = FastAPI(title="Unimicro TODO API", lifespan=lifespan)

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
