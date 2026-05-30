from fastapi import FastAPI
from app.database import engine
from app.api.characters import router as characters_router
from app.api.scenarios import router as scenarios_router

app = FastAPI(title="Rehearsal")
app.include_router(characters_router)
app.include_router(scenarios_router)

@app.get("/")
def root():
    return {"message": "Rehearsal API"}