from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.exercise import Exercise
from schemas.exercise import ExerciseCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new exercise
@router.post("/", response_model=ExerciseCreate)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

# Get all exercises
@router.get("/", response_model=list[ExerciseCreate])
def get_all_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()

# Get exercise by ID
@router.get("/{exercise_id}", response_model=ExerciseCreate)
def get_exercise_by_id(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

# Update an existing exercise
@router.put("/{exercise_id}", response_model=ExerciseCreate)
def update_exercise(exercise_id: int, updated_exercise: ExerciseCreate, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    for key, value in updated_exercise.dict().items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)
    return exercise

# Delete an exercise
@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()
    return {"message": f"Exercise with ID {exercise_id} has been deleted"}
