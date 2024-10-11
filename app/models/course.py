from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import Base
from .semester import Semester

class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    course_name = Column(Text, nullable=False, primary_key=True)
    semester_id = Column(Integer, ForeignKey('semester.semester_id'), nullable=False)
    
    semester = relationship('Semester', back_populates='courses')
    lessons = relationship('Lesson', back_populates='course')

    def __repr__(self):
        return f"{self.course_name}"