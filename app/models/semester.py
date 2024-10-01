from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Semester(Base):
    __tablename__ = 'semester'
    
    semester_id = Column(Integer, primary_key=True)
    semester_name = Column(Text, nullable=False)
    
    courses = relationship('Course', back_populates='semester')