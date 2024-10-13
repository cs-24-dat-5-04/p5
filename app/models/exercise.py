from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Exercise(Base):
    __tablename__ = 'exercise'
    
    exercise_id = Column(Integer, primary_key=True)
    exercise_name = Column(Text, nullable=True)
    exercise_number = Column(Integer, nullable=False)
    exercise_content = Column(Text, nullable=True)
    exercise_solution = Column(Text, nullable=True)
    lesson_id = Column(Integer, ForeignKey('lesson.lesson_id'), nullable=False)
    
    lesson = relationship('Lesson', back_populates='exercises')
    
    def __repr__(self):
        if self.exercise_name:
            return f"{self.exercise_name}"
        else:
            return f"Exercise #{self.exercise_number}"
