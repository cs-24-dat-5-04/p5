import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from app.models import *

class Test_base():
    @pytest.fixture(scope = "function")
    def client(self, app):
        yield app.test_client()
        
    @pytest.fixture(scope = "function")
    def app(self):
        return create_app(True)
    
    @pytest.fixture(scope = "function")
    def session(self):
        return db.session
    
    def find_in_db(app, session, type, filter):
        with app.app_context():
            return session.query(type).filter(filter).first()
    
class Test_semesters(Test_base):
    def test_create_semester(self, client, session, app):
        response = client.post("/create_semester", data = {
            "semester_name": "abc11"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(app, session, Semester, Semester.semester_name == "abc11")
        print(f'SEMESTER NAME: {str(semester.semester_name)}')
        print(f'SEMESTER ID: {int(semester.semester_id)}')
        assert str(semester.semester_name) == "abc11" and int(semester.semester_id) == 2
        response = client.post("/create_semester", data = {
        })
        assert response.status_code == 404
        
        response = client.post("/create_semester", data = {
            "semester_name": "test321"
        })
        assert response.status_code == 404
        
        response = client.post("/create_semester", data = {
            "semester_name": ""
        })
        assert response.status_code == 404
        
        response = client.post("/create_semester", data = {
            "semester_name": "321"
        })
        assert response.status_code == 404
        
        response = client.post("/create_semester", data = {
            "semester_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/create_semester", data = {
            "semester_name": "a3a"
        })
        assert response.status_code == 404
        
    def test_change_semester(self, client, session, app):
        response = client.post("/save_semester", data = {
            "semester_id": "1",
            "new_name": "abc12"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(app, session, Semester, Semester.semester_name == "abc12")
        assert semester.semester_name == "abc12" and semester.semester_id == 1
        
        response = client.post("/save_semester", data = {
            "semester_id": "1000",
            "new_name": "abc12"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "0",
            "new_name": "abc12"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "-1",
            "new_name": "abc12"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "a",
            "new_name": "abc12"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "",
            "new_name": "abc12"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "1",
            "new_name": "abc123"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "1",
            "new_name": "123"
        })
        assert response.status_code == 404
    
        response = client.post("/save_semester", data = {
            "semester_id": "1",
            "new_name": "a3a"
        })
        assert response.status_code == 404
    
    def test_get_semesterlist(self, client):
        response = client.get("/semester")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View DAT5\" href=\"/semester/1\">" in response.get_data(as_text = True)
        
    def test_get_specific_semester(self, client):
        response = client.get("/semester/1")
        assert response.status_code == 200
        assert "<h1>Courses in DAT5</h1>" in response.get_data(as_text = True)
        
        response = client.get("/semester/100")
        assert response.status_code == 404
        
        response = client.get("/semester/0")
        assert response.status_code == 404
        
        response = client.get("/semester/-1")
        assert response.status_code == 404
        
    def test_delete_semester(self, client, session, app):
        response = client.post("/delete_semester", data = {
            "semester_id": "1"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(app, session, Semester, Semester.semester_id == 1)
        assert not semester
        
        response = client.post("/delete_semester", data = {
            "semester_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_semester", data = {
            "semester_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_semester", data = {
            "semester_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_semester", data = {
            "semester_id": ""
        })
        assert response.status_code == 404
        
        
class Test_courses(Test_base):
    def test_create_course(self, client, session, app):
        response = client.post("/create_course", data = {
            "course_year": "2020",
            "semester_id": "1",
            "course_name": "TEST"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(app, session, Course, Course.course_name == "TEST")
        assert course.course_name == "TEST" and course.course_id == 4 and course.course_year == 2020 and course.semester_id == 1
        
        response = client.post("/create_course", data = {
            "course_year": "1889",
            "semester_id": "1",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2101",
            "semester_id": "1",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "1",
            "course_name": "TEST1"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "1",
            "course_name": "TESTTEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "4",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "0",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "-1",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "a",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "",
            "course_name": "TEST"
        })
        assert response.status_code == 404
        
    def test_get_courselist(self, client):
        response = client.get("/course")
        assert response.status_code == 200
        assert "<h1>Courses</h1>" in response.get_data(as_text = True)
        
    def test_get_specific_course(self, client):
        response = client.get("/semester/1/course/1")
        assert response.status_code == 200
        assert "href=\"/semester/1/course/1\"" in response.get_data(as_text = True)
        
        response = client.get("/semester/1/course/500")

        assert response.status_code == 500

        response = client.get("/semester/5000/course/1")
        assert response.status_code == 500

        response = client.get("/semester/1/course/-1")
        assert response.status_code == 404

        response = client.get("/semester/1/course/0")
        assert response.status_code == 500
        
    def test_change_course(self, client, session, app):
        response = client.post("/save_course", data = {
            "course_id": "1",
            "new_name": "testa"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(app, session, Course, Course.course_name == "testa")
        assert course.course_name == "testa" and course.course_id == 1 and course.course_year == 2024 and course.semester_id == 1
        
        response = client.post("/save_course", data = {
            "course_id": "10000",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "0",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "-1",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "a",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "4",
            "new_name": "test1"
        })
        assert response.status_code == 404
        
        response = client.post("/save_course", data = {
            "course_id": "4",
            "new_name": "testtest"
        })
        assert response.status_code == 404
        
    def test_delete_course(self, client, session, app):
        response = client.post("/delete_course", data = {
            "course_id": "1"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(app, session, Course, Course.course_id == 1)
        assert not course
        
        response = client.post("/delete_course", data = {
            "course_id": "20000"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_course", data = {
            "course_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_course", data = {
            "course_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_course", data = {
            "course_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/delete_course", data = {
            "course_id": ""
        })
        assert response.status_code == 404
        
        
class Test_lectures(Test_base):
    def test_create_lecture(self, client, session, app):
        response = client.post("/create_lecture", data = {
            "course_id": "1"
        })
        assert response.status_code == 302
        lecture = Test_base.find_in_db(app, session, Lecture, Lecture.lecture_id == 4)
        assert lecture.lecture_id == 4 and lecture.lecture_number == 2 and lecture.course_id == 1
        
        response = client.post("/create_lecture", data = {
            "course_id": "9999"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lecture", data = {
            "course_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lecture", data = {
            "course_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lecture", data = {
            "course_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lecture", data = {
            "course_id": ""
        })
        assert response.status_code == 404
        
    def test_get_lecturelist(self, client):
        # Virker ikke atm?
        response = client.get("/lecture")
        assert response.status_code == 200
        
    def test_get_specific_lecture(self, client):
        response = client.get("/semester/1/course/1/lecture/1")
        assert response.status_code == 200
        assert "<h1>Lecture #1" in response.get_data(as_text = True)
        
        response = client.get("/semester/1/course/1/lecture/1000")
        assert response.status_code == 500
        
        response = client.get("/semester/1/course/1/lecture/0")
        assert response.status_code == 500
        
        response = client.get("/semester/1/course/1/lecture/-1")
        assert response.status_code == 404
        
    def test_change_lecture(self, client, session, app):
        response = client.post("/save_lecture", data = {
            "lecture_id": "1",
            "new_name": "test"
        })
        assert response.status_code == 302
        lecture = Test_base.find_in_db(app, session, Lecture, Lecture.lecture_id == 1)
        assert lecture.lecture_id == 1 and lecture.lecture_number == 1 and lecture.course_id == 1 and lecture.lecture_name == "test"
        
        response = client.post("/save_lecture", data = {
            "lecture_id": "9999",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lecture", data = {
            "lecture_id": "-1",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lecture", data = {
            "lecture_id": "0",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lecture", data = {
            "lecture_id": "a",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lecture", data = {
            "lecture_id": "",
            "new_name": "test"
        })
        assert response.status_code == 404
        
    def test_delete_lecture(self, client, session, app):
        response = client.post("/delete_lecture", data = {
            "lecture_id": "1",
        })
        assert response.status_code == 302
        lecture = Test_base.find_in_db(app, session, Lecture, Lecture.lecture_id == 1)
        assert not lecture
        
        response = client.post("/delete_lecture", data = {
            "lecture_id": "10000",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lecture", data = {
            "lecture_id": "-1",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lecture", data = {
            "lecture_id": "a",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lecture", data = {
            "lecture_id": "",
        })
        assert response.status_code == 404
        
        
class Test_exercises(Test_base):
    def test_create_exercise(self, client, session, app):
        response = client.post("/create_exercise", data = {
            "lecture_id": "1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 4)
        assert exercise.exercise_id == 4 and exercise.exercise_number == 2 and exercise.lecture_id == 1
        
        response = client.post("/create_exercise", data = {
            "lecture_id": "9999"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lecture_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lecture_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lecture_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lecture_id": ""
        })
        assert response.status_code == 404
        
    def test_get_exerciselist(self, client):
        response = client.get("/exercise")
        assert response.status_code == 200
        
    def test_get_specific_exercise(self, client):
        response = client.get("/exercise/1")
        assert response.status_code == 200
        assert "<h1>Exercise #1</h1>" in response.get_data(as_text = True)
        
        response = client.get("/exercise/90000")
        assert response.status_code == 500
        
        response = client.get("/exercise/0")
        assert response.status_code == 500
        
        response = client.get("/exercise/-1")
        assert response.status_code == 404
        
    def test_change_exercise(self, client, session, app):
        response = client.post("/save_exercise", data = {
            "exercise_id": "1",
            "new_name": "test"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_name == "test"
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "99999",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "0",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "-1",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "a",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_exercise", data = {
            "exercise_id": "0"
        })
        assert response.status_code == 404
        
    def test_delete_exercise(self, client, session, app):
        response = client.post("/delete_exercise", data = {
            "exercise_id": "1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert not exercise
        
        response = client.post("/delete_exercise", data = {
            "exercise_id": "10000",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_exercise", data = {
            "exercise_id": "0",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_exercise", data = {
            "exercise_id": "-1",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_exercise", data = {
            "exercise_id": "a",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_exercise", data = {
            "exercise_id": "",
        })
        assert response.status_code == 404
        
    def test_change_exercise_question(self, client, session, app):
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test",
            "exercise_solution": "testx"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_content == "test" and exercise.exercise_solution == "testx"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test",
            "exercise_solution": ""
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_content == "test" and exercise.exercise_solution == ""
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "",
            "exercise_solution": "test"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_content == "" and exercise.exercise_solution == "test"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_content == "test1"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(app, session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lecture_id == 1 and exercise.exercise_solution == "test1"
        
        response = client.post("/update_exercise/100", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 404
        
        response = client.post("/update_exercise/0", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 404
        
        response = client.post("/update_exercise/-1", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 404
        
        response = client.post("/update_exercise/a", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 404