from fastapi import FastAPI
from .database import Base, engine
from .routers import user, todo
from . import models   # 🔥 VERY IMPORTANT

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)
