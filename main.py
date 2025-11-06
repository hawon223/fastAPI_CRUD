from fastapi import FastAPI
from database import Base, engine
from routers import item_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "FastAPI CRUD Example")

app.include_router(item_router.router)

@app.get("/")
def root():
    return {"message":"Welcome to FastAPI CRUD"}