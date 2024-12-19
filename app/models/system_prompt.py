from . import db

class SystemPrompt(db.Model):
    __tablename__ = 'system_prompt'
    
    system_prompt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    system_prompt = db.Column(db.Text, nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.lecture_id'))
    
    lecture = db.relationship('Lecture', back_populates='system_prompt')