from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Lesson(Base):
    __tablename__ = 'lesson'
    
    lesson_id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey('course.course_id'), nullable=False)
    system_prompt = Column(nullable=True)
    
    course = relationship('Course', back_populates='lessons')
    exercises = relationship('Exercise', back_populates='lesson')