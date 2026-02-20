from fastapi import FastAPI
from routes import router
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Carbon Footprint API")

app.include_router(router)

@app.get("/")
def root():
    return {"msg": "Carbon API Running"}

# Run: uvicorn backend.main:app --reload --port 8000