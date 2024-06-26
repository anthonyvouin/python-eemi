from fastapi import FastAPI
from src.config.db import create_database
from src.controllers.home_controller import router as home_router
from src.controllers.student_controller import router as student_router
from src.controllers.export_controller import router as export_router
from src.controllers.user_controller import router as user_router


create_database()
app = FastAPI()
app.include_router(home_router)
app.include_router(student_router, prefix="/student")
app.include_router(export_router, prefix="/export")
app.include_router(user_router, prefix="/user")


