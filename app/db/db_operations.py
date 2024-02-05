from .constants import EXERCISES, DATABASE_URL
from .models import Exercise, Set, Workout, WorkoutSet, WorkoutType
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#TODO: Implement error handling, exceptions
## ---------------------------------------------------- CORE OPERATIONS ---------------------------------------------------- ##
def create_workout_set(db: Session, workout_id: int, set_id: int):
    """Create a relationship between a workout and a set."""
    workout_set = WorkoutSet(workout_id=workout_id, set_id=set_id)
    db.add(workout_set)
    db.commit()
    db.refresh(workout_set)
    
    db.close()
    return True


def add_new_set(exercise_name: str, weight: int, repetitions: int):
    """Add a set to a workout, initializing a new workout if needed."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    today_workout = get_workout_by_date(db, date.today())

    if not today_workout:
        today_workout = initialize_workout(db, date.today())

    exercise_id = db.query(Exercise).filter(Exercise.name == exercise_name).first().id

    set = Set(exercise_id=exercise_id, weight=weight, repetitions=repetitions, date=date.today())
    db.add(set)
    db.commit()
    db.refresh(set)

    create_workout_set(db, today_workout.id, set.id)
    
    db.close()
    return True

def get_workout_sets(workout_id: int):
    """Retrieve sets recorded in a specific workout."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    return (
        db.query(WorkoutSet)
        .filter(WorkoutSet.workout_id == workout_id)
        .all()
    )
    
def get_workout_date_by_id(id: int):
    """Retrieve a workout for a specific date."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db.query(Workout).filter(Workout.id == id).first().date

def get_workout_date_by_date(db ,date: date):
    """Retrieve a workout for a specific date."""
    return db.query(Workout).filter(Workout.date == date).first()

def initialize_workout(db: Session, workout_date: date):
    """Initialize a new workout for a specific date."""
    workout = Workout(date=workout_date, type=WorkoutType.PUSH) #TODO: Implement logic to determine workout type
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

def get_all_past_workouts():
    """Retrieve all past workouts."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    workouts = db.query(Workout).all()
    
    return workouts

def get_all_exercise_history():
    # TODO
    ...
    
def get_progress_for_exercise():
    # TODO
    ...

def preload_exercise_names(db: Session):
    try:
        for name, type in EXERCISES:
            exercise = Exercise(name=name, type=type)
            db.add(exercise)
        db.commit()
    finally:
        db.close()
        
def get_exercise_names():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    exercises = db.query(Exercise).all()
    db.close()
    return [exercise.name for exercise in exercises]