"""Constants are stored here."""

from .models import ExerciseType

DATABASE_URL = "sqlite:///test.db" 

EXERCISES = [
    ("Bench Press", ExerciseType.CHEST),
    ("Hammer Incline", ExerciseType.CHEST),
    ("Chest Fly", ExerciseType.CHEST),
    ("Seated Press Machine", ExerciseType.CHEST),
    ("Shoulder Press Machine", ExerciseType.SHOULDERS),
    ("Shoulder Press Dumbells", ExerciseType.SHOULDERS),
    ("Lateral Raises", ExerciseType.SHOULDERS),
    ("French Press", ExerciseType.TRICEPS),
    ("Tricep Cable", ExerciseType.TRICEPS),
    ("Hammer Curls", ExerciseType.BICEPS),
    ("Barbell Curls", ExerciseType.BICEPS),
    ("Preacher Curl Machine", ExerciseType.BICEPS),
    ("Dumbell Curls", ExerciseType.BICEPS),
    ("Lat Pulldown", ExerciseType.BACK),
    ("Seated Row (Wide)", ExerciseType.BACK),
    ("Seated Row (Narrow)", ExerciseType.BACK),
    ("Facepulls", ExerciseType.BACK),
    ("Pull Ups", ExerciseType.BACK),
    ("Leg Press", ExerciseType.LEGS),
    ("Leg Extension", ExerciseType.LEGS),
    ("Squat", ExerciseType.LEGS),
    ("Leg Raise", ExerciseType.LEGS),
]