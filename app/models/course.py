from . import db

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    course_name = db.Column(db.Text, nullable=False)
    course_year = db.Column(db.Integer, nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id'), nullable=False)
    
    semester = db.relationship('Semester', back_populates='courses')
    lessons = db.relationship('Lesson', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.course_name}"