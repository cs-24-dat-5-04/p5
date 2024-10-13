from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Lesson(Base):
    __tablename__ = 'lesson'
    
    lesson_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    lesson_name = Column(String, nullable=True)
    lesson_number = Column(Integer, autoincrement=True, nullable=False)
    course_id = Column(Integer, ForeignKey('course.course_id'), nullable=False)
    # system_prompt = Column(nullable=True)

    course = relationship('Course', back_populates='lessons')
    # exercises = relationship('Exercise', back_populates='lesson')
    
    def __repr__(self):
        if self.lesson_name:
            return f"{self.lesson_name}"
        else:
            return f"Lesson #{self.lesson_number}"
