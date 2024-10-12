from flask import Flask, redirect, render_template, request
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
        form_submission = Semester(semester_name = form.name.data)
        session.add(form_submission)
        session.commit()
    semester_list = session.query(Semester).all()
    return render_template('semester.html', semester_list=semester_list, form=form, active_page='semester')

@app.route('/semester/<int:semester_id>', methods=['GET', 'POST'])
def show_semester(semester_id):
    semester = session.query(Semester).filter(Semester.semester_id == semester_id).first()
    course_year = request.args.get('year', default=2024, type=int)
    course_list = session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_year == course_year))
    
    form = CourseForm()
    if semester:
        if request.method == 'POST' and form.validate_on_submit():
            form_submission = Course(course_name=form.name.data, course_year=form.year.data, semester=semester)
            # TODO: Insert for loop for the entered number of lessons to create lesson objects and add them to the session
            session.add(form_submission)
            session.commit()
        return render_template('show_semester.html', semester=semester, form=form, course_list=course_list, course_year = course_year)
    else:
        return "Semester not found", 404
    
@app.route('/course', methods=['GET', 'POST'])
def course():
    course_list = session.query(Course, Semester).join(Semester, Course.semester_id == Semester.semester_id).all()
    return render_template('course.html', course_list=course_list, active_page='course')

@app.route('/semester/<int:semester_id>/course/<int:course_id>', methods=['GET', 'POST'])
def show_course(semester_id, course_id):
    course = session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_id == course_id)).first()
    lesson_list = session.query(Lesson).filter(Lesson.course_id == course_id)
    return render_template('show_course.html', course=course, lesson_list=lesson_list, active_page='course')

@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    return render_template('exercise.html', active_page='exercise')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/delete_course', methods=['POST'])
def delete_course():
    course_id = request.form.get('course_id')
    course = session.query(Course).get(course_id)
    
    if course:
        session.delete(course)
        session.commit()

    return redirect(request.referrer)

@app.route('/save_course', methods=['POST'])
def save_course():
    course_id = request.form.get('course_id')
    new_name = request.form.get('new_name')
    course = session.query(Course).get(course_id)
    if course:
        course.course_name = new_name
        session.commit()

    return redirect(request.referrer)

@app.route('/create_course', methods=['POST'])
def create_course():
    course_name = request.form.get('course_name')
    course_year = request.form.get('course_year')
    semester_id = request.form.get('semester_id')
    semester = session.query(Semester).filter_by(semester_id=semester_id).first()
    course = Course(course_name=course_name, course_year=course_year, semester=semester)
    if semester:
        session.add(course)
        session.commit()
    return redirect(request.referrer)

@app.route('/delete_semester', methods=['POST'])
def delete_semester():
    semester_id = request.form.get('semester_id')
    semester = session.query(Semester).get(semester_id)
    
    if semester:
        session.delete(semester)
        session.commit()

    return redirect(request.referrer)

@app.route('/save_semester', methods=['POST'])
def save_semester():
    semester_id = request.form.get('semester_id')
    new_name = request.form.get('new_name')
    semester = session.query(Semester).get(semester_id)
    if semester:
        semester.semester_name = new_name
        session.commit()
    return redirect(request.referrer)

@app.route('/create_semester', methods=['POST'])
def create_semester():
    semester_name = request.form.get('semester_name')
    semester = Semester(semester_name = semester_name)
    session.add(semester)
    session.commit()
    return redirect(request.referrer)


if __name__ == '__main__':
   app.run(debug=True)