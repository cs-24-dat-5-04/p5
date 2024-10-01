from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    
    course_id = Column(Integer, primary_key=True)
    course_name = Column(Text, nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.semester_id'), nullable=False)
    
    semester = relationship('Semester', back_populates='courses')
    lessons = relationship('Lesson', back_populates='course')