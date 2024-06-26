from fastapi import FastAPI
from src.config.db import create_database
from src.controllers.user_controller import router as user_router
from src.controllers.student_controller import router as student_router

create_database()
app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(student_router, prefix="/student")

