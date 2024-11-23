from database import SessionLocal, engine
from models.workout_plan import WorkoutPlan
from models.exercise import Exercise
from database import Base

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        workout_plan1 = WorkoutPlan(name="Weight Loss Plan", description="A plan focused on losing weight", goal_type="weight_loss")
        workout_plan2 = WorkoutPlan(name="Muscle Gain Plan", description="Build muscles effectively", goal_type="muscle_gain")

        db.add(workout_plan1)
        db.add(workout_plan2)
        db.commit()

        db.refresh(workout_plan1)
        db.refresh(workout_plan2)

        exercise1 = Exercise(name="Running", duration_min=30, calories_burned=300, plan_id=workout_plan1.id)
        exercise2 = Exercise(name="Cycling", duration_min=45, calories_burned=400, plan_id=workout_plan1.id)

        exercise3 = Exercise(name="Bench Press", duration_min=20, calories_burned=200, plan_id=workout_plan2.id)
        exercise4 = Exercise(name="Deadlift", duration_min=25, calories_burned=250, plan_id=workout_plan2.id)

        db.add_all([exercise1, exercise2, exercise3, exercise4])
        db.commit()

        print("Database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
