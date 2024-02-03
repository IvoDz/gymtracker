from fastapi import APIRouter, Request, Depends, Form
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
    exercises = get_exercise_names()
    return templates.TemplateResponse("add_set.html", {"request": request, "exercises": exercises})

@router.post("/submit_set")
def submit_form(exercise: str = Form(...), weight: int = Form(...), reps: int = Form(...)):
    add_new_set(exercise, weight, reps)
    return {"Status": "Set Added Successfully!"}