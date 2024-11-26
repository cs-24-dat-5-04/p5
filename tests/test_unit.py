import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from database.db_init import setup_database
from app.models import *

class Test_base():
    @pytest.fixture(scope = "function")
    def object(self):
        setup_database("test")
        object = create_app("test")
        yield object
        session = object[1]
        session.close()
        
    @pytest.fixture(scope = "function")
    def client(self, object):
        return object[0].test_client()
    
    @pytest.fixture(scope="function")
    def session(self, object):
        return object[1]
    
    def find_in_db(session, type, filter):
        return session.query(type).filter(filter).first()
    
    
class Test_semesters(Test_base):
    def test_create_semester(self, client, session):
        response = client.post("/create_semester", data = {
            "semester_name": "abc11"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(session, Semester, Semester.semester_name == "abc11")
        assert semester.semester_name == "abc11" and semester.semester_id == 2
        
        response = client.post("/create_semester", data = {
        })
        assert response.status_code == 500   
        
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
        
    def test_change_semester(self, client, session):
        response = client.post("/save_semester", data = {
            "semester_id": "1",
            "new_name": "abc12"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(session, Semester, Semester.semester_name == "abc12")
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
        
    def test_delete_semester(self, client, session):
        response = client.post("/delete_semester", data = {
            "semester_id": "1"
        })
        assert response.status_code == 302
        semester = Test_base.find_in_db(session, Semester, Semester.semester_id == 1)
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
    def test_create_course(self, client, session):
        response = client.post("/create_course", data = {
            "course_year": "2020",
            "semester_id": "1",
            "course_name": "TEST"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(session, Course, Course.course_name == "TEST")
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
        assert "<li>MI (2024-DAT5)</li>" in response.get_data(as_text = True)
        
    def test_get_specific_course(self, client):
        response = client.get("/semester/1/course/1")
        assert response.status_code == 200
        assert "href=\"/semester/1\" class=\"card-title\">DAT5 2024" in response.get_data(as_text = True)
        
        response = client.get("/semester/1/course/500")

        assert response.status_code == 500

        response = client.get("/semester/5000/course/1")
        assert response.status_code == 500

        response = client.get("/semester/1/course/-1")
        assert response.status_code == 404

        response = client.get("/semester/1/course/0")
        assert response.status_code == 500
        
    def test_change_course(self, client, session):
        response = client.post("/save_course", data = {
            "course_id": "1",
            "new_name": "testa"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(session, Course, Course.course_name == "testa")
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
        
    def test_delete_course(self, client, session):
        response = client.post("/delete_course", data = {
            "course_id": "1"
        })
        assert response.status_code == 302
        course = Test_base.find_in_db(session, Course, Course.course_id == 1)
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
        
        
class Test_lessons(Test_base):
    def test_create_lesson(self, client, session):
        response = client.post("/create_lesson", data = {
            "course_id": "1"
        })
        assert response.status_code == 302
        lesson = Test_base.find_in_db(session, Lesson, Lesson.lesson_id == 4)
        assert lesson.lesson_id == 4 and lesson.lesson_number == 2 and lesson.course_id == 1
        
        response = client.post("/create_lesson", data = {
            "course_id": "9999"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lesson", data = {
            "course_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lesson", data = {
            "course_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lesson", data = {
            "course_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/create_lesson", data = {
            "course_id": ""
        })
        assert response.status_code == 404
        
    def test_get_lessonlist(self, client):
        # Virker ikke atm?
        response = client.get("/lesson")
        assert response.status_code == 200
        
    def test_get_specific_lesson(self, client):
        response = client.get("/semester/1/course/1/lesson/1")
        assert response.status_code == 200
        assert "<h1>Lesson #1" in response.get_data(as_text = True)
        
        response = client.get("/semester/1/course/1/lesson/1000")
        assert response.status_code == 500
        
        response = client.get("/semester/1/course/1/lesson/0")
        assert response.status_code == 500
        
        response = client.get("/semester/1/course/1/lesson/-1")
        assert response.status_code == 404
        
    def test_change_lesson(self, client, session):
        response = client.post("/save_lesson", data = {
            "lesson_id": "1",
            "new_name": "test"
        })
        assert response.status_code == 302
        lesson = Test_base.find_in_db(session, Lesson, Lesson.lesson_id == 1)
        assert lesson.lesson_id == 1 and lesson.lesson_number == 1 and lesson.course_id == 1 and lesson.lesson_name == "test"
        
        response = client.post("/save_lesson", data = {
            "lesson_id": "9999",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lesson", data = {
            "lesson_id": "-1",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lesson", data = {
            "lesson_id": "0",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lesson", data = {
            "lesson_id": "a",
            "new_name": "test"
        })
        assert response.status_code == 404
        
        response = client.post("/save_lesson", data = {
            "lesson_id": "",
            "new_name": "test"
        })
        assert response.status_code == 404
        
    def test_delete_lesson(self, client, session):
        response = client.post("/delete_lesson", data = {
            "lesson_id": "1",
        })
        assert response.status_code == 302
        lesson = Test_base.find_in_db(session, Lesson, Lesson.lesson_id == 1)
        assert not lesson
        
        response = client.post("/delete_lesson", data = {
            "lesson_id": "10000",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lesson", data = {
            "lesson_id": "-1",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lesson", data = {
            "lesson_id": "a",
        })
        assert response.status_code == 404
        
        response = client.post("/delete_lesson", data = {
            "lesson_id": "",
        })
        assert response.status_code == 404
        
        
class Test_exercises(Test_base):
    def test_create_exercise(self, client, session):
        response = client.post("/create_exercise", data = {
            "lesson_id": "1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 4)
        assert exercise.exercise_id == 4 and exercise.exercise_number == 2 and exercise.lesson_id == 1
        
        response = client.post("/create_exercise", data = {
            "lesson_id": "9999"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lesson_id": "-1"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lesson_id": "0"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lesson_id": "a"
        })
        assert response.status_code == 404
        
        response = client.post("/create_exercise", data = {
            "lesson_id": ""
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
        
    def test_change_exercise(self, client, session):
        response = client.post("/save_exercise", data = {
            "exercise_id": "1",
            "new_name": "test"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_name == "test"
        
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
        
    def test_delete_exercise(self, client, session):
        response = client.post("/delete_exercise", data = {
            "exercise_id": "1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
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
        
    def test_change_exercise_question(self, client, session):
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test",
            "exercise_solution": "testx"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_content == "test" and exercise.exercise_solution == "testx"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test",
            "exercise_solution": ""
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_content == "test" and exercise.exercise_solution == ""
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "",
            "exercise_solution": "test"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_content == "" and exercise.exercise_solution == "test"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_content": "test1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_content == "test1"
        
        response = client.post("/update_exercise/1", data = {
            "exercise_solution": "test1"
        })
        assert response.status_code == 302
        exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        assert exercise.exercise_id == 1 and exercise.exercise_number == 1 and exercise.lesson_id == 1 and exercise.exercise_solution == "test1"
        
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
        
    #def test_update_system_prompt(self, client, session):
        # Ser ike ud til at være færdigt?
        #response = client.post("/update_system_prompt/1", data = {
            #"system_prompt": "test"
        #})
        #assert response.status_code == 302
        #exercise = Test_base.find_in_db(session, Exercise, Exercise.exercise_id == 1)
        
        
        
#class Test_prompts(Test_base):
    #def test_create_prompt(self, client):
        #response = client.post("/create_prompt", data = {
        #})
        #assert response.status_code == 200