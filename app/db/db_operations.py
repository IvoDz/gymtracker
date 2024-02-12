from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .constants import DATABASE_URL, EXERCISES
from .models import Exercise, Set, Workout, WorkoutSet, WorkoutType, ExerciseType

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
    exercise_id = db.query(Exercise).filter(Exercise.name == exercise_name).first().id
    exercise_type = get_exercise_by_id(exercise_id).type
    workout_type = get_workout_type(exercise_type)
    
    if not today_workout:    
        today_workout = initialize_workout(db, date.today(), workout_type)

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

def get_workout_by_date(db ,date: date):
    """Retrieve a workout for a specific date."""
    return db.query(Workout).filter(Workout.date == date).first()

def get_workout_by_id(id: int):
    """Retrieve a workout for a specific ID."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db.query(Workout).filter(Workout.id == id).first()

def initialize_workout(db: Session, workout_date: date ,type: WorkoutType):
    """Initialize a new workout for a specific date."""
    workout = Workout(date=workout_date, type=type) 
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



def preload_exercise_names(db: Session):
    try:
        for name, type in EXERCISES:
            exercise = Exercise(name=name, type=type)
            db.add(exercise)
        db.commit()
    finally:
        db.close()
        
def get_exercises():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    exercises = db.query(Exercise).all()
    db.close()
    return [exercise for exercise in exercises]

def get_set_by_id(id: int):
    """Retrieve a set data for a specific ID."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db.query(Set).filter(Set.id == id).first()

def get_exercise_by_id(id: int):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db.query(Exercise).filter(Exercise.id == id).first()

def get_workout_type(exercise_type: ExerciseType):
    """Retrieve a workout type for a specific exercise type."""
    if exercise_type in [ExerciseType.CHEST, ExerciseType.SHOULDERS, ExerciseType.TRICEPS]:
        return WorkoutType.PUSH
    elif exercise_type in [ExerciseType.BICEPS, ExerciseType.BACK]:
        return WorkoutType.PULL
    elif exercise_type == ExerciseType.LEGS:
        return WorkoutType.LEGS
    else:
        return None
    
    
def get_workout_date_by_set_id(set_id: int):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    workout_id = db.query(WorkoutSet).filter(WorkoutSet.set_id == set_id).first().workout_id
    workout_date =  get_workout_date_by_id(workout_id)

    return workout_date

def delete_workout(workout_id):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    workout = session.query(Workout).filter_by(id=workout_id).first()
    if workout:
        workout_sets = session.query(WorkoutSet).filter_by(workout_id=workout_id).all()
        for workout_set in workout_sets:
            session.delete(workout_set)
        
        sets = session.query(Set).join(WorkoutSet).filter(WorkoutSet.workout_id == workout_id).all()
        for s in sets:
            session.delete(s)
        
        session.delete(workout)
        session.commit()
        return True
    return False


def get_progress_for_exercise(exercise_id: int):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    sets = db.query(Set).join(Exercise).filter(Exercise.id == exercise_id).all()
    
    pairs = [(s.repetitions, s.weight, get_workout_date_by_set_id(s.id)) for s in sets]
    db.close()
    return pairs

def check_exercises(db):
    exercises = db.query(Exercise).all()
    if not exercises:
        preload_exercise_names(db)
    db.close()
    return True