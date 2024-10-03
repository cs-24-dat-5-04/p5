from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    course_name = Column(nullable=False, primary_key=True)
    semester_id = Column(ForeignKey('semester.semester_id'), nullable=False)
    
    semester = relationship('Semester', back_populates='courses')
    lessons = relationship('Lesson', back_populates='course')