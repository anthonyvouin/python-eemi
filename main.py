from fastapi import FastAPI
from src.controllers.test_controller import router as test_router
from src.config.db import create_database

create_database()
app = FastAPI()
app.include_router(test_router, prefix="/api")

