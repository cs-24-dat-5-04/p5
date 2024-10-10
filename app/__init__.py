
from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from openai import OpenAI
import sys
import markdown
import json
from .forms.semester_form import SemesterForm

with open('secrets.json', 'r') as file:
    secrets = json.load(file)
    
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets["csrf_token"]
engine = create_engine('sqlite:///./database.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from .models import Semester, Course, Exercise, FineTuning, Lesson, Prompt
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
    semester = SemesterForm()
    if request.method == 'POST' and semester.validate_on_submit():
        form_submission = Semester(semester_name = semester.name.data, semester_year = semester.year.data)
        session.add(form_submission)
        session.commit()
    semester_list = session.query(Semester).all()
    return render_template('semester.html', semester_list=semester_list, form=semester, active_page='semester')

@app.route('/semester/<int:semester_id>')
def show_semester(semester_id):
    semester = session.query(Semester).filter(Semester.semester_id == semester_id).first()
    course_list = session.query(Course).filter(Course.semester_id == semester_id)
    if semester:
        return render_template('show_semester.html', semester=semester, course_list=course_list)
    else:
        return "Semester not found", 404
@app.route('/course', methods=['GET', 'POST'])
def course():
    course_list = session.query(Course).all()
    return render_template('course.html', course_list=course_list, active_page='course')

@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    return render_template('exercise.html', active_page='exercise')

if __name__ == '__main__':
   app.run(debug=True)
