from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp
from app.models import semester

class CourseForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=5,
                message="Name must not be longer than five characters"
            ),
            Regexp(
                r'^[A-Z]+$',
                message="Name must be letters"
                )
        ]
    )
    
    # Gets data from the URL routing
    semester = HiddenField()

    submit = SubmitField()