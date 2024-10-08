from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Semester(Base):
    __tablename__ = 'semester'
    
    semester_year = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    semester_name = Column(primary_key=True, nullable=False)
    
    def str(self):
        return f"{self.semester_year} - {self.semester_name}"