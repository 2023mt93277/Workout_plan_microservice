from pydantic import BaseModel
from typing import List

class Exercise(BaseModel):
    id: int
    name: str
    duration_min: int
    calories_burned: int

    class Config:
        orm_mode = True

class WorkoutPlan(BaseModel):
    id: int
    name: str
    description: str
    goal_type: str
    exercises: List[Exercise] = []

    class Config:
        orm_mode = True

class WorkoutPlanCreate(BaseModel):
    name: str
    description: str
    goal_type: str
