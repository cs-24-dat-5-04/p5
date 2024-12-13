import random
import string
import time
from flask import Flask, Response, flash, jsonify, redirect, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from app.forms.semester_form import SemesterForm
from app.forms.course_form import CourseForm
from werkzeug.utils import secure_filename
from openai import OpenAI

from app.models import db, Course, Exercise, FineTuning, Lesson, Prompt, Semester, SystemPrompt
import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
def create_app():
    app = Flask(__name__)
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    app.config['SECRET_KEY'] = secrets["csrf_token"]
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, 'database.db')}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Max file size = 16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Specify upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    
    # Initialize database and update tables as needed
    db.init_app(app)
    with app.app_context():
        db.create_all()
        client = OpenAI(
        organization = secrets["organization"],
        project = secrets["project"],
        api_key = secrets["api_key"],
        )
        # Populate Semester
        existing_semester = Semester.query.filter_by(semester_name='DAT5').first()
        if not existing_semester: 
            semester = Semester(semester_name='DAT5')
            db.session.add(semester)
            db.session.commit()  # Commit to get the generated primary key (semester_id)

            # Populate Courses
            courses = [
                Course(course_name='MI', course_year=2024, semester_id=semester.semester_id),
                Course(course_name='ASE', course_year=2024, semester_id=semester.semester_id),
                Course(course_name='DBS', course_year=2024, semester_id=semester.semester_id),
            ]
            db.session.add_all(courses)
            db.session.commit()  # Commit to get the generated primary keys for courses

            # Populate Lessons
            for course in courses:
                lesson = Lesson(lesson_number=1, course_id=course.course_id)
                db.session.add(lesson)
            db.session.commit()  # Commit to get the generated primary keys for lessons

            # Populate Exercises
            lessons = Lesson.query.join(Course).join(Semester).filter(
                Course.course_name.in_(['MI', 'ASE', 'DBS']),
                Semester.semester_name == 'DAT5'
            ).all()

            for lesson in lessons:
                exercise = Exercise(exercise_number=1, lesson_id=lesson.lesson_id)
                db.session.add(exercise)
            db.session.commit()

    def complete(system_prompt, user_prompt):
        model = 'gpt-4o-mini'

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
        prompt = db.session.query(Prompt).get(prompt_id)
        return prompt.user_prompt

    @app.template_filter('get_prompt_completion')
    def get_prompt_completion(prompt_id):
        prompt = db.session.query(Prompt).get(prompt_id)
        if prompt != None:
            return prompt.completion
        else:
            return ''

    @app.template_filter('get_system_prompt_from_lesson')
    def get_system_prompt_from_lesson(lesson_id):
        system_prompt = db.session.query(SystemPrompt).filter_by(lesson_id = lesson_id).first()
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
            db.session.add(form_submission)
            db.session.commit()

        return render_template("prompt.html", output=output, active_page='prompt')

    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        return render_template('dashboard.html', active_page='dashboard')

    @app.route('/semester', methods=['GET', 'POST'])
    def semester():
        form = SemesterForm()
        if request.method == 'POST' and form.validate_on_submit():
            form_submission = Semester(semester_name = form.name.data)
            db.session.add(form_submission)
            db.session.commit()
        semester_list = db.session.query(Semester).all()
        return render_template('semester.html', semester_list=semester_list, form=form, active_page='semester')

    @app.route('/semester/<int:semester_id>', methods=['GET', 'POST'])
    def show_semester(semester_id):
        semester = db.session.query(Semester).filter(Semester.semester_id == semester_id).first()
        course_year = request.args.get('year', default=2024, type=int)
        course_list = db.session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_year == course_year))
        
        form = CourseForm()
        if semester:
            if request.method == 'POST' and form.validate_on_submit():
                form_submission = Course(course_name=form.name.data, course_year=form.year.data, semester=semester)
                # TODO: Insert for loop for the entered number of lessons to create lesson objects and add them to the db.session
                db.session.add(form_submission)
                db.session.commit()
            return render_template('show_semester.html', semester=semester, form=form, course_list=course_list, course_year = course_year, active_page='semester')
        else:
            return "Semester not found", 404
        
    @app.route('/course', methods=['GET', 'POST'])
    def course():
        course_list = db.session.query(Course, Semester).join(Semester, Course.semester_id == Semester.semester_id).all()
        return render_template('course.html', course_list=course_list, active_page='course')

    @app.route('/semester/<int:semester_id>/course/<int:course_id>', methods=['GET', 'POST'])
    def show_course(semester_id, course_id):
        course = db.session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_id == course_id)).first()
        lesson_list = db.session.query(Lesson).filter(Lesson.course_id == course_id)
        course_list = db.session.query(Course).filter(and_(Course.semester_id == semester_id, Course.course_year == course.course_year))
        semester = db.session.query(Semester).filter(Semester.semester_id == semester_id).first()
        return render_template('show_course.html', course=course, semester=semester, lesson_list=lesson_list, course_list=course_list, active_course_id=course_id)

    @app.route('/exercise', methods=['GET', 'POST'])
    def exercise():
        return render_template('exercise.html', active_page='exercise')

    @app.route('/lesson', methods=['GET', 'POST'])
    def lesson():
        return render_template('lesson.html', active_page='lesson')

    @app.route('/semester/<int:semester_id>/course/<int:course_id>/lesson/<int:lesson_number>', methods=['GET', 'POST'])
    def show_lesson(semester_id, course_id, lesson_number):
        course = db.session.query(Course).filter(Course.course_id == course_id).first()
        lesson = db.session.query(Lesson).filter(and_(Lesson.course_id == course_id, Lesson.lesson_number == lesson_number)).first()
        exercise_list = db.session.query(Exercise).filter(Exercise.lesson_id == lesson.lesson_id)
        system_prompt = db.session.query(SystemPrompt).filter_by(lesson_id = lesson.lesson_id).first()
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
        semester = db.session.query(Semester).get(semester_id)
        print(semester_id)
        print(semester)
        
        if semester:
            db.session.delete(semester)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/save_semester', methods=['POST'])
    def save_semester():
        semester_id = request.form.get('semester_id')
        new_name = request.form.get('new_name')
        semester = db.session.query(Semester).get(semester_id)
        match = re.search(r"[A-Za-z][A-Za-z]?[A-Za-z]?\d\d?", new_name)
        if semester and match and match.group() == new_name and len(new_name) <= 5:
            semester.semester_name = new_name
            db.session.commit()
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
            db.session.add(semester)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/delete_course', methods=['POST'])
    def delete_course():
        course_id = request.form.get('course_id')
        course = db.session.query(Course).get(course_id)
        
        if course:
            db.session.delete(course)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer, 404)

    @app.route('/save_course', methods=['POST'])
    def save_course():
        course_id = request.form.get('course_id')
        new_name = request.form.get('new_name')
        course = db.session.query(Course).get(course_id)
        if course:
            course.course_name = new_name
            db.session.commit()
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
        semester = db.session.query(Semester).filter_by(semester_id=semester_id).first()
        course = Course(course_name=course_name, course_year=course_year, semester=semester)
        if semester and match and match.group() == course_name and len(course_name) <= 5 and course_year_int >= 1890 and course_year_int <= 2100:
            db.session.add(course)
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/delete_lesson', methods=['POST'])
    def delete_lesson():
        lesson_id = request.form.get('lesson_id')
        lesson = db.session.query(Lesson).get(lesson_id)
        
        if lesson:
            db.session.delete(lesson)
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/save_lesson', methods=['POST'])
    def save_lesson():
        lesson_id = request.form.get('lesson_id')
        new_name = request.form.get('new_name')
        lesson = db.session.query(Lesson).get(lesson_id)
        if lesson:
            lesson.lesson_name = new_name
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/create_lesson', methods=['POST'])
    def create_lesson():
        course_id = request.form.get('course_id')
        last_lesson = db.session.query(Lesson).filter_by(course_id = course_id).order_by(Lesson.lesson_number.desc()).first()
        if last_lesson:
            lesson_number = last_lesson.lesson_number + 1
        else:
            lesson_number = 1
        course = db.session.query(Course).filter_by(course_id = course_id).first()
        if not course:
            return redirect(request.referrer, 404)
        lesson = Lesson(course_id = course_id, lesson_number = lesson_number)
        db.session.add(lesson)
        db.session.commit()
        return redirect(request.referrer)

    @app.route('/delete_exercise', methods=['POST'])
    def delete_exercise():
        exercise_id = request.form.get('exercise_id')
        exercise = db.session.query(Exercise).get(exercise_id)
        
        if exercise:
            db.session.delete(exercise)
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/save_exercise', methods=['POST'])
    def save_exercise():
        exercise_id = request.form.get('exercise_id')
        new_name = request.form.get('new_name')
        exercise = db.session.query(Exercise).get(exercise_id)
        if exercise:
            exercise.exercise_name = new_name
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/create_exercise', methods=['POST'])
    def create_exercise():
        lesson_id = request.form.get('lesson_id')
        last_exercise = db.session.query(Exercise).filter_by(lesson_id = lesson_id).order_by(Exercise.exercise_number.desc()).first()
        if last_exercise:
            exercise_number = last_exercise.exercise_number + 1
        else:
            exercise_number = 1
        lesson = db.session.query(Lesson).filter_by(lesson_id = lesson_id).first()
        if not lesson:
            return redirect(request.referrer, 404)
        exercise = Exercise(lesson_id = lesson_id, exercise_number = exercise_number)
        db.session.add(exercise)
        db.session.commit()
        return redirect(request.referrer)

    @app.route('/exercise/<int:exercise_id>', methods=['GET', 'POST'])
    def show_exercise(exercise_id):
        exercise = db.session.query(Exercise).filter_by(exercise_id = exercise_id).first()
        prompts = None
        fine_tuning = None
        if exercise.exercise_type == 'advanced':
            fine_tuning = db.session.query(FineTuning).filter_by(exercise_id = exercise.exercise_id).first()
            if fine_tuning:
                    prompts = [
                    {'prompt_id': p.prompt_id, 'system_prompt': p.system_prompt, 'user_prompt': p.user_prompt, 'assistant_prompt': p.assistant_prompt}
                    for p in db.session.query(Prompt).filter(Prompt.fine_tuning.has(fine_tuning_id=fine_tuning.fine_tuning_id)).all()
                    ]
        return render_template('show_exercise.html', exercise=exercise, prompts=prompts, active_page='exercise', fine_tuning=fine_tuning)

    @app.route('/update_exercise/<int:exercise_id>', methods=['POST'])
    def update_exercise(exercise_id):
        exercise_content = request.form.get('exercise_content')
        exercise_solution = request.form.get('exercise_solution')
        exercise = db.session.query(Exercise).get(exercise_id)
        if exercise:
            exercise.exercise_content = exercise_content
            exercise.exercise_solution = exercise_solution
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)

    @app.route('/update_exercise_type/<int:exercise_id>', methods=['POST'])
    def update_exercise_type(exercise_id):
        exercise_type = request.form.get('exercise_type')
        exercise = db.session.query(Exercise).get(exercise_id)
        if exercise:
            exercise.exercise_type = exercise_type
            fine_tuning_exists = db.session.query(FineTuning).filter_by(exercise_id = exercise_id).first()
            if not fine_tuning_exists:
                db.session.add(FineTuning(exercise_id = exercise_id))
            db.session.commit()
            return redirect(request.referrer)
        else: 
            return redirect(request.referrer, 404)
        
    @app.route('/update_system_prompt/<int:lesson_id>', methods=['POST'])
    def update_system_prompt(lesson_id):
        content = request.form.get('system_prompt')
        system_prompt = db.session.query(SystemPrompt).filter_by(lesson_id = lesson_id).first()
        lesson = db.session.query(Lesson).get(lesson_id)
        if lesson:
            if system_prompt:
                system_prompt.system_prompt = content
            else:
                system_prompt = SystemPrompt(system_prompt = content, lesson_id = lesson_id)
                db.session.add(system_prompt)
                db.session.flush()
            lesson.system_prompt_id = system_prompt.system_prompt_id
            db.session.commit()
            
        return redirect(request.referrer)

    @app.route('/finetune', methods=['POST'])
    def finetune():
        fine_tuning_id = request.form.get('fine_tuning_id')
        fine_tuning = db.session.query(FineTuning).filter_by(fine_tuning_id = fine_tuning_id).first()
        prompts = db.session.query(Prompt).filter(Prompt.fine_tuning_id == fine_tuning_id).all()
        filename = f'{fine_tuning.exercise.lesson.course.semester.semester_name}-{fine_tuning.exercise.lesson.course.course_year}-{fine_tuning.exercise.lesson.course.course_name}-L{fine_tuning.exercise.lesson.lesson_number}-E{fine_tuning.exercise.exercise_number}.jsonl'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(file_path, "w") as file:
            for line in prompts_to_jsonl(prompts):
                file.write(line)
                
        
        training_data = client.files.create(
            file=open(file_path, "rb"),
            purpose="fine-tune"
        )
        response = client.fine_tuning.jobs.create(
        training_file=training_data.id, 
        model="gpt-4o-mini-2024-07-18"
        )
        
        status = client.fine_tuning.jobs.retrieve(response.id).status
        while status != "succeeded" and status != "failed" and status != "cancelled":
            time.sleep(5)
            status = client.fine_tuning.jobs.retrieve(response.id).status
            print(f"Status: {status}")

        return redirect(request.referrer)

    def complete_prompt(user_prompt, system_prompt, prompt_id=None):
        if prompt_id:
            print(f'Prompt ID: {prompt_id}')
            prompt = db.session.query(Prompt).get(prompt_id)
        else:
            print("Prompt ID is None")
            prompt = Prompt(user_prompt = user_prompt)
            db.session.add(prompt)
            db.session.flush()
        completion = complete(system_prompt, user_prompt)
        print(f'Prompt: {prompt}')
        prompt.completion = completion
        db.session.commit()
        return completion, prompt.prompt_id

    def validate_proposed_solution(question, solution, proposed_solution):
        system_prompt = 'Only reply with "True" or "False". Nothing else.'
        user_prompt = f'{solution} is the solution to the question: {question}. Is {proposed_solution} also a valid solution to the question?'
        completion = complete(system_prompt, user_prompt)
        print(user_prompt)
        answer = re.search(r'True', completion, re.IGNORECASE) is not None
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
        exercise = db.session.query(Exercise).get(exercise_id)
        exercise.proposed_solution_id = prompt_id
        if validate_proposed_solution(user_prompt, exercise_solution, proposed_solution):
            exercise.proposed_solution_validation = True
        else:
            exercise.proposed_solution_validation = False
        db.session.commit()
        return redirect(request.referrer)

    @app.route('/upload_fine_tuning_file/<int:exercise_id>', methods=['POST'])
    def upload_fine_tuning_file(exercise_id):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.referrer)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.referrer)

        if file and file.filename.rsplit('.', 1)[1].lower() == 'jsonl':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file
            file.save(file_path)

            result = jsonl_to_prompts(file_path, exercise_id)

            if result['status'] == 'success':
                print(f"{result['prompts_added']} prompts successfully added.")
                return redirect(request.referrer)
            else:
                print(f"Error processing file: {result['message']}")
                return redirect(request.referrer)

        flash('File type not allowed')
        return redirect(request.referrer)
    
    @app.route('/update_prompt', methods=['POST'])
    def update_prompt():
        prompt_id = request.form.get('prompt_id')
        user_prompt = request.form.get('user_prompt')
        prompt = db.session.query(Prompt).filter_by(prompt_id = prompt_id).first()
        prompt.user_prompt = user_prompt
        db.session.commit()
        return redirect(request.referrer)
        
    def jsonl_to_prompts(file_path, exercise_id):
        prompts = []
        fine_tuning_id = db.session.query(FineTuning).filter_by(exercise_id = exercise_id).first().fine_tuning_id
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        message = json.loads(line)
                        system_prompt = message['messages'][0]['content']
                        user_prompt = message['messages'][1]['content']
                        assistant_prompt = message['messages'][2]['content']

                        prompt = Prompt(
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            assistant_prompt=assistant_prompt,
                            fine_tuning_id=fine_tuning_id
                        )
                        prompts.append(prompt)
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Skipping invalid line: {e}")

            if prompts:
                db.session.add_all(prompts)
                db.session.commit()

            return {'status': 'success', 'prompts_added': len(prompts)}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @app.route('/export-prompts/<int:exercise_id>', methods=['GET'])
    def export_prompts(exercise_id):
        # Example data to write as JSONL
        fine_tuning_id = db.session.query(FineTuning).filter_by(exercise_id = exercise_id).first().fine_tuning_id
        prompts = db.session.query(Prompt).filter(Prompt.fine_tuning_id == fine_tuning_id).all()
        
        return Response(
            prompts_to_jsonl(prompts),
            mimetype='application/jsonl',
            headers={
                "Content-Disposition": "attachment;filename=data.jsonl"
            }
        )
        
    def prompts_to_jsonl(prompts):
        for prompt in prompts:
            prompt_data = { 
                "messages": [        
                    {"role": "system", "content": prompt.system_prompt}, 
                    {"role": "user", "content": prompt.user_prompt},
                    {"role": "assistant", "content": prompt.assistant_prompt}
                ]
            }
            yield json.dumps(prompt_data) + "\n"
      
    return app

def create_flask_app():
    return create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)