from . import db

class Prompt(db.Model):
    __tablename__ = 'prompt'
    
    prompt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    system_prompt = db.Column(db.Text, nullable=True)
    user_prompt = db.Column(db.Text, nullable=False)
    completion = db.Column(db.Text, nullable=True)
    fine_tuning_id = db.Column(db.Integer, db.ForeignKey('fine_tuning.fine_tuning_id'))

    solutions = db.relationship(
        'Exercise',
        foreign_keys='Exercise.proposed_solution_id',
        back_populates='proposed_solution'
    )
    new_questions = db.relationship(
        'Exercise',
        foreign_keys='Exercise.proposed_new_question_id',
        back_populates='proposed_new_question'
    )
    new_solutions = db.relationship(
        'Exercise',
        foreign_keys='Exercise.proposed_new_solution_id',
        back_populates='proposed_new_solution'
    )
    fine_tuning = db.relationship('FineTuning', back_populates='prompts')