
from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from openai import OpenAI
from .models import Course, Exercise, FineTuning, Lesson, Prompt, Semester
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

@app.route('/', methods=['GET', 'POST'])
def index():
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

    return render_template("index.html", output=output)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/semester', methods=['GET', 'POST'])
def semester_create():
    semester = SemesterForm()
    if request.method == 'POST' and semester.validate_on_submit():
        form_submission = Semester(semester_name = semester.name.data, semester_year = semester.year.data)
        session.add(form_submission)
        session.commit()
        return f'Form submitted!\nName: {semester.name.data}\nYear:{semester.year.data}'
    return render_template('semester.html', form=semester)

@app.route('/course', methods=['GET', 'POST'])
def course():
    return render_template('course.html')

if __name__ == '__main__':
   app.run(debug=True)
