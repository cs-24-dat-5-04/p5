from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Prompt(Base):
    __tablename__ = 'prompt'
    
    prompt_id = Column(Integer, autoincrement=True, primary_key=True)
    user_prompt = Column(Text, nullable=False)
    completion = Column(Text, nullable=True)
    
    solutions = relationship('Exercise', foreign_keys='Exercise.proposed_solution_id', back_populates='proposed_solution')
    new_questions = relationship('Exercise', foreign_keys='Exercise.proposed_new_question_id', back_populates='proposed_new_question')
    new_solutions = relationship('Exercise', foreign_keys='Exercise.proposed_new_solution_id', back_populates='proposed_new_solution')
    
    #fine_tuning_id = Column(Integer, ForeignKey('fine_tuning.fine_tuning_id'), nullable=False)
    #fine_tuning = relationship('FineTuning', back_populates='prompts')