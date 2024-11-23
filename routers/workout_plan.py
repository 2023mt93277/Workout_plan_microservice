from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.workout_plan import WorkoutPlan
from models.exercise import Exercise
from schemas.workout_plan import WorkoutPlan as WorkoutPlanSchema, WorkoutPlanCreate
from schemas.exercise import ExerciseCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new workout plan
@router.post("/", response_model=WorkoutPlanSchema)
def create_workout_plan(plan: WorkoutPlanCreate, db: Session = Depends(get_db)):
    db_plan = WorkoutPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# Get all workout plans
@router.get("/", response_model=list[WorkoutPlanSchema])
def get_workout_plans(db: Session = Depends(get_db)):
    return db.query(WorkoutPlan).all()

# Get details of a specific workout plan
@router.get("/{goal_type}", response_model=list[WorkoutPlanSchema])
def get_workout_plan(goal_type: str, db: Session = Depends(get_db)):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.goal_type  == goal_type ).all()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout Plan not found")
    return plan

# Add exercises to a workout plan
@router.post("/{plan_id}/exercises", response_model=ExerciseCreate)
def add_exercise_to_plan(plan_id: int, exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return ExerciseCreate(**db_exercise.__dict__)

# Get exercises of a workout plan
@router.get("/{plan_id}/exercises", response_model=list[ExerciseCreate])
def get_plan_exercises(plan_id: int, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(Exercise.plan_id == plan_id).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found for this plan")
    return [ExerciseCreate(**exercise.__dict__) for exercise in exercises]
