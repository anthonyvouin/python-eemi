from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from ..services.home_service import getHtmlContent

router = APIRouter()

@router.get("/{name}")
def read_root(name: str):
   return HTMLResponse(content=getHtmlContent(name))