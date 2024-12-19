from . import db

class Lecture(db.Model):
    __tablename__ = 'lecture'
    
    lecture_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    lecture_name = db.Column(db.String, nullable=True)
    lecture_number = db.Column(db.Integer, autoincrement=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    course = db.relationship('Course', back_populates='lectures')
    exercises = db.relationship('Exercise', back_populates='lecture', cascade='all, delete-orphan')
    system_prompt = db.relationship('SystemPrompt', back_populates='lecture', cascade='all, delete-orphan')
    
    def __repr__(self):
        if self.lecture_name:
            return f"{self.lecture_name}"
        else:
            return f"Lecture #{self.lecture_number}"
