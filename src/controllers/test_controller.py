from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.get("/test")
def test_route():
    return {"message": "This is a test route"}