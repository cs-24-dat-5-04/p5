from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompt'
    
    prompt_id = Column(Integer, primary_key=True)
    system_prompt = Column(Text, nullable=False)
    user_prompt = Column(Text, nullable=False)
    completion = Column(Text)
    fine_tuning_id = Column(Integer, ForeignKey('fine_tuning.fine_tuning_id'))
    
    fine_tuning = relationship('FineTuning', back_populates='prompts')
