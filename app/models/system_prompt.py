from . import db

class SystemPrompt(db.Model):
    __tablename__ = 'system_prompt'
    
    system_prompt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    system_prompt = db.Column(db.Text, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'))
    
    lesson = db.relationship('Lesson', back_populates='system_prompt')