from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
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
                message="Name must be capital letters"
                )
        ]
    )

    semester = QuerySelectField(
        'Semester',
        query_factory=lambda: semester.query.all(),
        get_label='__repr__',
        allow_blank=False
    )
    submit = SubmitField()