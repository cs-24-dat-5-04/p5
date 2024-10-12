from sqlalchemy import Column, Integer, Text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Semester(Base):
    __tablename__ = 'semester'
    semester_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    semester_name = Column(Text, nullable=False)
    
    courses = relationship('Course', back_populates='semester')
    
    def __repr__(self):
        return f"{self.semester_name}"
