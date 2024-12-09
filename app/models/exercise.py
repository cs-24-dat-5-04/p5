from . import db

class Exercise(db.Model):
    __tablename__ = 'exercise'
    
    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_name = db.Column(db.Text, nullable=True)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_content = db.Column(db.Text, nullable=True)
    exercise_solution = db.Column(db.Text, nullable=True)
    exercise_type = db.Column(db.Text, default="simple")
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False)
    proposed_solution_id = db.Column(db.Integer, db.ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_new_question_id = db.Column(db.Integer, db.ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_new_solution_id = db.Column(db.Integer, db.ForeignKey('prompt.prompt_id'), nullable=True)
    proposed_solution_validation = db.Column(db.Boolean, nullable=True)
    proposed_new_question_validation = db.Column(db.Boolean, nullable=True)
    proposed_new_solution_validation = db.Column(db.Boolean, nullable=True)
    
    # Relationships
    lesson = db.relationship('Lesson', back_populates='exercises')
    proposed_solution = db.relationship(
        'Prompt',
        foreign_keys=[proposed_solution_id],
        back_populates='solutions'
    )
    proposed_new_question = db.relationship(
        'Prompt',
        foreign_keys=[proposed_new_question_id],
        back_populates='new_questions'
    )
    proposed_new_solution = db.relationship(
        'Prompt',
        foreign_keys=[proposed_new_solution_id],
        back_populates='new_solutions'
    )
    fine_tunings = db.relationship('FineTuning', back_populates='exercise')

    def __repr__(self):
        if self.exercise_name:
            return f"{self.exercise_name}"
        else:
            return f"Exercise #{self.exercise_number}"
