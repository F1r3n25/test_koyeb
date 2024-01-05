from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.database.db import get_db
from src.routes import notes, tags, auth, users
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def startup(app: FastAPI):
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


app = FastAPI(lifespan=startup)


app.include_router(auth.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(users.router, prefix="/api")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
