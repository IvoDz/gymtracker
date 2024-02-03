from fastapi import APIRouter, Request, Depends
from db.db_operations import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")

@router.get("/", response_class=HTMLResponse)
def get_endpoint(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/add_set", response_class=HTMLResponse)
def add_set(request: Request):
    return templates.TemplateResponse("add_set.html", {"request": request})