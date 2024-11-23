from fastapi import FastAPI
from routers import workout_plan, exercise
from database import Base, engine

app = FastAPI(
    title="Workout Plan Service",
    description="Manages workout plans and exercises",
    version="1.0.0",
)

app.include_router(workout_plan.router, prefix="/api/plans", tags=["Workout Plans"])
app.include_router(exercise.router, prefix="/api/exercises", tags=["Exercises"])

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Workout Plan Service is running"}
