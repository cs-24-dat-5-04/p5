from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Exercise(Base):
    __tablename__ = 'exercise'
    
    exercise_id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    lesson_id = Column(Integer, ForeignKey('lesson.lesson_id'), nullable=False)
    
    lesson = relationship('Lesson', back_populates='exercises')
