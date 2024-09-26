from app import db

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(), unique=True, nullable=False)
    output = db.Column(db.String(), unique=True, nullable=False)
    
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    output = db.Column(db.String(), unique=True, nullable=False)
    prompts = db.relationship('Prompt', backref='conversation', lazy=True)