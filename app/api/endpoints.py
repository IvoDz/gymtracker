from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db.db_operations import *

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
    response = RedirectResponse(url="/")
    response.status_code = 302
    return response

@router.get("/past_workouts")
def workout_history(request: Request):
    workouts = get_all_past_workouts()
    return templates.TemplateResponse("past_workouts.html", {"request": request, "workouts": workouts})

@router.get("/workout/{workout_id}")
def workout_details(request: Request, workout_id: int):
    date = get_workout_date_by_id(workout_id)
    workout_sets = get_workout_sets(workout_id)
    
    sets = [get_set_by_id(set.id) for set in workout_sets]
    exercises = [get_exercise_by_id(set.exercise_id) for set in sets]
    
    sets = list(zip(exercises, sets))
    
    print(sets)
    
    return templates.TemplateResponse("workout_details.html", {"request": request, "date": date, "sets": sets})

#TODO: exercise/{id}/progress,  /exercises