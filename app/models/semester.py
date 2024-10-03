from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Semester(Base):
    __tablename__ = 'semester'
    
    semester_year = Column(Integer, primary_key=True, nullable=False)
    semester_name = Column(primary_key=True, nullable=False)
    
    courses = relationship('Course', back_populates='semester')