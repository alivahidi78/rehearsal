from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.api.characters import router as characters_router
from app.api.scenarios import router as scenarios_router
from app.api.sessions import router as sessions_router
from app.graph.graph import conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # app runs here
    conn.close()  # cleanup on shutdown

app = FastAPI(title="Rehearsal", lifespan=lifespan)
app.include_router(characters_router)
app.include_router(scenarios_router)
app.include_router(sessions_router)

@app.get("/")
def root():
    return {"message": "Rehearsal API"}