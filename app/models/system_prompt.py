from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class SystemPrompt(Base):
    __tablename__ = 'system_prompt'
    
    system_prompt_id = Column(Integer, autoincrement=True, primary_key=True)
    system_prompt = Column(nullable=False)
    lesson_id = Column(Integer, ForeignKey('lesson.lesson_id'))
    
    lesson = relationship('Lesson', back_populates='system_prompt')