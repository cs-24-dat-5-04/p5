from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class SystemPrompt(Base):
    __tablename__ = 'system_prompt'
    
    system_prompt_id = Column(Integer, autoincrement=True, primary_key=True)
    system_prompt = Column(nullable=False)
    lession_id = Column(Integer, ForeignKey('lesson.lesson_id'))