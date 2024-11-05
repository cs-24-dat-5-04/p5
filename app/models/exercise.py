from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Exercise(Base):
    __tablename__ = 'exercise'
    
    exercise_id = Column(Integer, autoincrement=True, primary_key=True)
    exercise_name = Column(Text, nullable=True)
    exercise_number = Column(Integer, nullable=False)
    exercise_content = Column(Text, nullable=True)
    exercise_solution = Column(Text, nullable=True)
    lesson_id = Column(Integer, ForeignKey('lesson.lesson_id'), nullable=False)
    proposed_solution_id = Column(Integer, ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_new_question_id = Column(Integer, ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_new_solution_id = Column(Integer, ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_solution_validation = Column(Boolean, nullable=True)
    proposed_new_question_validation = Column(Boolean, nullable=True)
    proposed_new_solution_validation = Column(Boolean, nullable=True)
    
    lesson = relationship('Lesson', back_populates='exercises')
    proposed_solution = relationship('Prompt', foreign_keys=[proposed_solution_id], back_populates='solutions')
    proposed_new_question = relationship('Prompt', foreign_keys=[proposed_new_question_id], back_populates='new_questions')
    proposed_new_solution = relationship('Prompt', foreign_keys=[proposed_new_solution_id], back_populates='new_solutions')
    
    def __repr__(self):
        if self.exercise_name:
            return f"{self.exercise_name}"
        else:
            return f"Exercise #{self.exercise_number}"