from fastapi import APIRouter

router = APIRouter()


# create a student
@router.post("/")
def read_root(name: str):
   return f"<h1>Hello <span>{name}</span></h1>"


#return a student by id
@router.get("/")
def read_root(name: str):
   return f"<h1>Hello <span>{name}</span></h1>"