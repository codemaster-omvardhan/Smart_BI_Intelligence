from fastapi import FastAPI
from api.routes import router
from api.auth import router as auth_router
from db.session import engine
from db.base import Base
from api.datasets import router as dataset_router


app = FastAPI(title="Smart BI Platform API")

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(auth_router)
app.include_router(dataset_router)

@app.get("/")
def root():
    return {"message": "Smart BI Backend is Running"}