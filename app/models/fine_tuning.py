from . import db

class FineTuning(db.Model):
    __tablename__ = 'fine_tuning'
    fine_tuning_id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, nullable=False)
    fine_tuning_model_id = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'))

    exercise = db.relationship('Exercise', back_populates='fine_tunings')
    prompts = db.relationship('Prompt', back_populates='fine_tuning')