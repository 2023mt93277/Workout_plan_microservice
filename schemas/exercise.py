from pydantic import BaseModel

class ExerciseCreate(BaseModel):
    name: str
    duration_min: int
    calories_burned: int
    plan_id: int
