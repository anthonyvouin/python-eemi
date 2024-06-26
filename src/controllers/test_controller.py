from fastapi import APIRouter

router = APIRouter()

@router.get("/{name}")
def read_root(name: str):
   return f"<h1>Hello <span>{name}</span></h1>"