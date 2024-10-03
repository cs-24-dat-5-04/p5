from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import semester

class SemesterForm(FlaskForm):
    semester = StringField(
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
        'Year',
        validators=[
            DataRequired(),
            NumberRange(
                min=1890,
                max=2100,
                message="Year must be between 1890 and 2100"),
            Length(equal=4,
                   message="Year must be four digits"
                   )
            ]
    )

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
                message="Name must be capital letters"
                )
        ]
    )
    lessons = IntegerField(
        'Number of lessons',
        validators=[
            NumberRange(
                min=1,
                max=24,
                message="You must have at least one lecture and can't have more than 24"
            )
        ]
    )
    semester = QuerySelectField(
        'Semester',
        query_factory=lambda: semester.query.all(),
        get_label='full_label',
        allow_blank=False   
    )