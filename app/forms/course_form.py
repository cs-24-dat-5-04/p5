from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

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
    year = IntegerField(
        'Year',
        validators=[
            DataRequired(),
            NumberRange(
                min=1890,
                max=2100,
                message="Year must be between 1890 and 2100"),
        ]
    )
    
    # Gets data from the URL routing
    semester = HiddenField()

    submit = SubmitField()