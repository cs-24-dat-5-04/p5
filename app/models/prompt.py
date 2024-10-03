from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompt'
    
    prompt_id = Column(Integer, autoincrement=True, primary_key=True)
    user_prompt = Column(nullable=False)
    completion = Column()
    #fine_tuning_id = Column(Integer, ForeignKey('fine_tuning.fine_tuning_id'), nullable=False)
    
    #fine_tuning = relationship('FineTuning', back_populates='prompts')


