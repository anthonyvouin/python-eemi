from fastapi import FastAPI
from src.controllers.test_controller import router as test_router

app = FastAPI()
app.include_router(test_router, prefix="/api")

