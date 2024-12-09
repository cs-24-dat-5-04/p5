from . import db

class FineTuning(db.Model):
    __tablename__ = 'fine_tuning'
    fine_tuning_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    filename = db.Column(db.Text)
    model_id = db.Column(db.Text)

    exercise = db.relationship('Exercise', back_populates='fine_tunings')
    prompts = db.relationship('Prompt', back_populates='fine_tuning')