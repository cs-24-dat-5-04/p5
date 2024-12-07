import re
from flask import Flask, redirect, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from openai import OpenAI
import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from forms.semester_form import SemesterForm
from forms.course_form import CourseForm

def create_app(setup="none"):
    app = Flask(__name__)
    if setup == "none":
        engine = create_engine('sqlite:///./database.db', echo=True)
    elif setup == "test":
        engine = create_engine('sqlite:///./testdatabase.db', echo=True)
    else:
        raise Exception("wrong setup argument")
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
        app.config['SECRET_KEY'] = secrets["csrf_token"]
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    test = [app, session]
    

    from models import Semester, Course, Lesson, Exercise, FineTuning, Prompt, SystemPrompt

    def complete(system_prompt, user_prompt):
        model = 'gpt-4o-mini'
        client = OpenAI(
        organization = secrets["organization"],
        project = secrets["project"],
        api_key = secrets["api_key"],
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user","content": user_prompt},
            ],
            max_tokens = 200
        )
        return completion.choices[0].message.content

    @app.template_filter('get_user_prompt')
    def get_user_prompt(prompt_id):
        prompt = session.query(Prompt).get(prompt_id)
        return prompt.user_prompt

    @app.template_filter('get_prompt_completion')
    def get_prompt_completion(prompt_id):
        prompt = session.query(Prompt).get(prompt_id)
        if prompt != None:
            return prompt.completion
        else:
            return ''

    @app.template_filter('get_system_prompt_from_lesson')
    def get_system_prompt_from_lesson(lesson_id):
        system_prompt = session.query(SystemPrompt).filter_by(lesson_id = lesson_id).first()
        if system_prompt:
            return system_prompt.system_prompt
        return None

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
            return render_template('show_semester.html', semester=semester, form=form, course_list=course_list, course_year = course_year, active_page='semester')
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
        course_list = session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_year == course.course_year))
        semester = session.query(Semester).filter(Semester.semester_id == semester_id).first()
        return render_template('show_course.html', course=course, semester=semester, lesson_list=lesson_list, course_list=course_list, active_course_id=course_id)

    @app.route('/exercise', methods=['GET', 'POST'])
    def exercise():
        return render_template('exercise.html', active_page='exercise')

    @app.route('/lesson', methods=['GET', 'POST'])
    def lesson():
        return render_template('lesson.html', active_page='lesson')

    @app.route('/semester/<int:semester_id>/course/<int:course_id>/lesson/<int:lesson_number>', methods=['GET', 'POST'])
    def show_lesson(semester_id, course_id, lesson_number):
        course = session.query(Course).filter(Course.course_id == course_id).first()
        lesson = session.query(Lesson).filter(and_(Lesson.course_id == course_id, Lesson.lesson_number == lesson_number)).first()
        exercise_list = session.query(Exercise).filter(Exercise.lesson_id == lesson.lesson_id)
        system_prompt = session.query(SystemPrompt).filter_by(lesson_id = lesson.lesson_id).first()
        return render_template('show_lesson.html', course=course, lesson=lesson, lesson_id=lesson.lesson_id, exercise_list=exercise_list, system_prompt=system_prompt, active_page='lesson')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.route('/delete_semester', methods=['POST'])
    def delete_semester():
        semester_id = request.form.get('semester_id')
        semester = session.query(Semester).get(semester_id)
        print(semester_id)
        print(semester)
        
        if semester:
            session.delete(semester)
            session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/save_semester', methods=['POST'])
    def save_semester():
        semester_id = request.form.get('semester_id')
        new_name = request.form.get('new_name')
        semester = session.query(Semester).get(semester_id)
        match = re.search(r"[A-Za-z][A-Za-z]?[A-Za-z]?\d\d?", new_name)
        if semester and match and match.group() == new_name and len(new_name) <= 5:
            semester.semester_name = new_name
            session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/create_semester', methods=['POST'])
    def create_semester():
        semester_name = request.form.get('semester_name')
        match = re.search(r"[A-Za-z][A-Za-z]?[A-Za-z]?\d\d?", semester_name)
        if match and match.group() == semester_name and len(semester_name) <= 5:
            print(321321)
            semester = Semester(semester_name = semester_name)
            session.add(semester)
            session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/delete_course', methods=['POST'])
    def delete_course():
        course_id = request.form.get('course_id')
        course = session.query(Course).get(course_id)
        
        if course:
            session.delete(course)
            session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/save_course', methods=['POST'])
    def save_course():
        course_id = request.form.get('course_id')
        new_name = request.form.get('new_name')
        course = session.query(Course).get(course_id)
        if course:
            course.course_name = new_name
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/create_course', methods=['POST'])
    def create_course():
        course_name = request.form.get('course_name')
        match = re.search(r"[A-Za-z][A-Za-z]?[A-Za-z]?[A-Za-z]?[A-Za-z]?", course_name)
        course_year = request.form.get('course_year')
        course_year_int = int(course_year)
        semester_id = request.form.get('semester_id')
        semester = session.query(Semester).filter_by(semester_id=semester_id).first()
        course = Course(course_name=course_name, course_year=course_year, semester=semester)
        if semester and match and match.group() == course_name and len(course_name) <= 5 and course_year_int >= 1890 and course_year_int <= 2100:
            session.add(course)
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/delete_lesson', methods=['POST'])
    def delete_lesson():
        lesson_id = request.form.get('lesson_id')
        lesson = session.query(Lesson).get(lesson_id)
        
        if lesson:
            session.delete(lesson)
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/save_lesson', methods=['POST'])
    def save_lesson():
        lesson_id = request.form.get('lesson_id')
        new_name = request.form.get('new_name')
        lesson = session.query(Lesson).get(lesson_id)
        if lesson:
            lesson.lesson_name = new_name
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/create_lesson', methods=['POST'])
    def create_lesson():
        course_id = request.form.get('course_id')
        last_lesson = session.query(Lesson).filter_by(course_id = course_id).order_by(Lesson.lesson_number.desc()).first()
        if last_lesson:
            lesson_number = last_lesson.lesson_number + 1
        else:
            lesson_number = 1
        course = session.query(Course).filter_by(course_id = course_id).first()
        if not course:
            return redirect(request.referrer, 404)
        lesson = Lesson(course_id = course_id, lesson_number = lesson_number)
        session.add(lesson)
        session.commit()
        return redirect(request.referrer)

    @app.route('/delete_exercise', methods=['POST'])
    def delete_exercise():
        exercise_id = request.form.get('exercise_id')
        exercise = session.query(Exercise).get(exercise_id)
        
        if exercise:
            session.delete(exercise)
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/save_exercise', methods=['POST'])
    def save_exercise():
        exercise_id = request.form.get('exercise_id')
        new_name = request.form.get('new_name')
        exercise = session.query(Exercise).get(exercise_id)
        if exercise:
            exercise.exercise_name = new_name
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/create_exercise', methods=['POST'])
    def create_exercise():
        lesson_id = request.form.get('lesson_id')
        last_exercise = session.query(Exercise).filter_by(lesson_id = lesson_id).order_by(Exercise.exercise_number.desc()).first()
        if last_exercise:
            exercise_number = last_exercise.exercise_number + 1
        else:
            exercise_number = 1
        lesson = session.query(Lesson).filter_by(lesson_id = lesson_id).first()
        if not lesson:
            return redirect(request.referrer, 404)
        exercise = Exercise(lesson_id = lesson_id, exercise_number = exercise_number)
        session.add(exercise)
        session.commit()
        return redirect(request.referrer)

    @app.route('/exercise/<int:exercise_id>', methods=['GET', 'POST'])
    def show_exercise(exercise_id):
        exercise = session.query(Exercise).filter_by(exercise_id = exercise_id).first()
        return render_template('show_exercise.html', exercise=exercise, active_page='exercise')

    @app.route('/update_exercise/<int:exercise_id>', methods=['POST'])
    def update_exercise(exercise_id):
        exercise_content = request.form.get('exercise_content')
        exercise_solution = request.form.get('exercise_solution')
        exercise = session.query(Exercise).get(exercise_id)
        if exercise:
            exercise.exercise_content = exercise_content
            exercise.exercise_solution = exercise_solution
            session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/update_system_prompt/<int:lesson_id>', methods=['POST'])
    def update_system_prompt(lesson_id):
        content = request.form.get('system_prompt')
        system_prompt = session.query(SystemPrompt).filter_by(lesson_id = lesson_id).first()
        lesson = session.query(Lesson).get(lesson_id)
        if lesson:
            if system_prompt:
                system_prompt.system_prompt = content
            else:
                system_prompt = SystemPrompt(system_prompt = content, lesson_id = lesson_id)
                session.add(system_prompt)
                session.flush()
            lesson.system_prompt_id = system_prompt.system_prompt_id
            session.commit()
        return redirect(request.referrer)

    def complete_prompt(user_prompt, system_prompt, prompt_id=None):
        if prompt_id:
            print(f'Prompt ID: {prompt_id}')
            prompt = session.query(Prompt).get(prompt_id)
        else:
            print("Prompt ID is None")
            prompt = Prompt(user_prompt = user_prompt)
            session.add(prompt)
            session.flush()
        completion = complete(system_prompt, user_prompt)
        print(f'Prompt: {prompt}')
        prompt.completion = completion
        session.commit()
        return completion, prompt.prompt_id

    def validate_proposed_solution(question, solution, proposed_solution):
        system_prompt = 'Only reply with "yes" or "no". Nothing else.'
        user_prompt = f'{solution} is the solution to the question: {question}. Is {proposed_solution} also a valid solution to the question?'
        completion = complete(system_prompt, user_prompt)
        print(user_prompt)
        answer = re.search(r'yes', completion, re.IGNORECASE) is not None
        print(f'Answer: {answer}')
        return answer
        
        
    @app.route('/generate_proposed_solution', methods=['POST'])
    def generate_proposed_solution():
        user_prompt = request.form.get('user_prompt')
        system_prompt = request.form.get('system_prompt')
        exercise_id = request.form.get('exercise_id')
        exercise_solution = request.form.get('exercise_solution')
        prompt_id = request.form.get('prompt_id')
        proposed_solution, prompt_id = complete_prompt(user_prompt, system_prompt, prompt_id)
        exercise = session.query(Exercise).get(exercise_id)
        exercise.proposed_solution_id = prompt_id
        if validate_proposed_solution(user_prompt, exercise_solution, proposed_solution):
            exercise.proposed_solution_validation = True
        else:
            exercise.proposed_solution_validation = False
        session.commit()
        return redirect(request.referrer)
    return test

if __name__ == '__main__':
    app = create_app()[0]
    app.run(debug=True)