from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

class SemesterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(
                max=5,
                message="Name must not be longer than five characters"
            ),
            Regexp(
                r'^[A-Za-z]{1,3}\d{1,2}$',
                message="Input must be up to 3 letters followed by up to 2 digits (e.g., ABC12)"
            )
        ]
    )
    year = IntegerField(
        'year',
        validators=[
            DataRequired(),
            NumberRange(
                min=1890,
                max=2100,
                message="Year must be between 1890 and 2100"),
        ]
    )
    submit = SubmitField()