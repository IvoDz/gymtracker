from enum import Enum as PythonEnum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ExerciseType(PythonEnum):
    LEGS = "legs"
    CHEST = "chest"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    BACK = "back"
    SHOULDERS = "shoulders"
    
class WorkoutType(PythonEnum):
    LEGS = "legs"
    PUSH = "push"
    PULL = "pull"
    
print(WorkoutType.LEGS)
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(ExerciseType))

    sets = relationship("Set", back_populates="exercise")

class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    date = Column(Date)
    weight = Column(Integer)
    repetitions = Column(Integer)

    exercise = relationship("Exercise", back_populates="sets")
    workout_sets = relationship("WorkoutSet", back_populates="set")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    type = Column(Enum(WorkoutType))

    sets = relationship("WorkoutSet", back_populates="workout")

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    set_id = Column(Integer, ForeignKey('sets.id'))

    workout = relationship("Workout", back_populates="sets")
    set = relationship("Set", back_populates="workout_sets")
