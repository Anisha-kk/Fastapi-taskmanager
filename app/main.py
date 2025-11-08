from fastapi import FastAPI
from app.routers import auth, task
from app.db.session import Base, engine
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Task Manager API")

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(task.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
