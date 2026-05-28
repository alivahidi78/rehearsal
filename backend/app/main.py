from fastapi import FastAPI
from app.database import engine

app = FastAPI(title="Rehearsal")

@app.get("/")
def root():
    return {"message": "Rehearsal API"}