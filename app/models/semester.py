from . import db

class Semester(db.Model):
    __tablename__ = 'semester'
    semester_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    semester_name = db.Column(db.Text, nullable=False)
    
    courses = db.relationship('Course', back_populates='semester', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"{self.semester_name}"
