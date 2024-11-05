from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class FineTuning(Base):
    __tablename__ = 'fine_tuning'
    
    fine_tuning_id = Column(Integer, primary_key=True, autoincrement=True)
    fine_tuning_name = Column(nullable=False)
    
    #prompts = relationship('Prompt', back_populates='fine_tuning')