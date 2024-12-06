from . import db

class Lesson(db.Model):
    __tablename__ = 'lesson'
    
    lesson_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    lesson_name = db.Column(db.String, nullable=True)
    lesson_number = db.Column(db.Integer, autoincrement=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    course = db.relationship('Course', back_populates='lessons')
    exercises = db.relationship('Exercise', back_populates='lesson', cascade='all, delete-orphan')
    system_prompt = db.relationship('SystemPrompt', back_populates='lesson', cascade='all, delete-orphan')
    
    def __repr__(self):
        if self.lesson_name:
            return f"{self.lesson_name}"
        else:
            return f"Lesson #{self.lesson_number}"
