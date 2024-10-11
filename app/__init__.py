from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from openai import OpenAI
import sys
import markdown
import json
from .forms.semester_form import SemesterForm
from .forms.course_form import CourseForm


with open('secrets.json', 'r') as file:
    secrets = json.load(file)
    
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets["csrf_token"]
engine = create_engine('sqlite:///./database.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from .models import Semester, Course, Lesson, Exercise, FineTuning, Prompt

@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    output = "Hello! How can I assist you today?"
    if request.method == 'POST':
        prompt = request.form['prompt']
        model = request.form['model']

        client = OpenAI(
        organization = secrets["organization"],
        project = secrets["project"],
        api_key = secrets["api_key"],
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user","content": prompt},
            ],
            max_tokens = 50
        )
        output = completion.choices[0].message.content
        # markdown.markdown(completion.choices[0].message.content)

        form_submission = Prompt(user_prompt = prompt, completion = output)
        session.add(form_submission)
        session.commit()

    return render_template("prompt.html", output=output, active_page='prompt')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/semester', methods=['GET', 'POST'])
def semester():
    form = SemesterForm()
    if request.method == 'POST' and form.validate_on_submit():
        form_submission = Semester(semester_name = semester.name.data, semester_year = semester.year.data)
        session.add(form_submission)
        session.commit()
    semester_list = session.query(Semester).all()
    return render_template('semester.html', semester_list=semester_list, form=form, active_page='semester')

@app.route('/semester/<int:semester_id>', methods=['GET', 'POST'])
def show_semester(semester_id):
    semester = session.query(Semester).filter(Semester.semester_id == semester_id).first()
    course_list = session.query(Course).filter(Course.semester_id == semester_id)
    
    form = CourseForm()
    if semester:
        if request.method == 'POST' and form.validate_on_submit():
            form_submission = Course(course_name=form.name.data, semester=semester)
            # TODO: Insert for loop for the entered number of lessons to create lesson objects and add them to the session
            session.add(form_submission)
            session.commit()
        return render_template('show_semester.html', semester=semester, form=form, course_list=course_list)
    else:
        return "Semester not found", 404
    
@app.route('/course', methods=['GET', 'POST'])
def course():
    course_list = session.query(Course).all()
    return render_template('course.html', course_list=course_list, active_page='course')

@app.route('/semester/<int:semester_id>/course/<int:course_id>', methods=['GET', 'POST'])
def show_course(semester_id, course_id):
    course = session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_id == course_id)).first()
    lesson_list = session.query(Lesson).filter(Lesson.course_id == course_id)
    return render_template('show_course.html', course=course, lesson_list=lesson_list, active_page='course')

@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    return render_template('exercise.html', active_page='exercise')

if __name__ == '__main__':
   app.run(debug=True)