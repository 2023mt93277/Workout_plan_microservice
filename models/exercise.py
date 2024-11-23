from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    duration_min = Column(Integer, nullable=True)
    calories_burned = Column(Integer, nullable=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.id"))

    workout_plan = relationship("WorkoutPlan", back_populates="exercises")
