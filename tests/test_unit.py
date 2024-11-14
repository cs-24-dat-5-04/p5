import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from database.db_init import setup_database

class Test_class():
    @pytest.fixture
    def client(self):
        app = create_app("test")
        return app.test_client()
    

class Test_setup(Test_class):
    def test_setup(self):
        setup_database("test")
    
    
class Test_semesters(Test_class):    
    def test_create_semester(self, client):
        response = client.post("/create_semester", data = {
            "semester_name": "abc11"
        })
        assert response.status_code == 302
        response = client.get("/semester")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View abc11\" href=\"/semester/2\"" in response.get_data(as_text = True)
        
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
        
    def test_change_semester(self, client):
        response = client.post("/save_semester", data = {
            "semester_id": "2",
            "new_name": "abc12"
        })
        assert response.status_code == 302
        response = client.get("/semester")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View abc12\" href=\"/semester/2\"" in response.get_data(as_text = True)
        
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
            "semester_id": "2",
            "new_name": "abc123"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "2",
            "new_name": "123"
        })
        assert response.status_code == 404
        
        response = client.post("/save_semester", data = {
            "semester_id": "2",
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
        
    def test_delete_semester(self, client):
        response = client.post("/delete_semester", data = {
            "semester_id": "2"
        })
        assert response.status_code == 302
        assert not "href=\"/semester/2\"" in response.get_data(as_text = True)
        
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
        
        
class Test_courses(Test_class):
    def test_create_course(self, client):
        response = client.post("/create_course", data = {
            "course_year": "2024",
            "semester_id": "1",
            "course_name": "TEST"
        })
        assert response.status_code == 302
        
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
        
    def test_change_course(self, client):
        response = client.post("/save_course", data = {
            "course_id": "4",
            "new_name": "testa"
        })
        assert response.status_code == 302
        response = client.get("/semester/1")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View testa\" href=\"/semester/1/course/4\"" in response.get_data(as_text = True)
        
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
        
    def test_delete_course(self, client):
        response = client.post("/delete_course", data = {
            "course_id": "4"
        })
        assert response.status_code == 302
        response = client.get("/course")
        assert response.status_code == 200
        assert not "href=\"/semester/1/course/4\"" in response.get_data(as_text = True)
        
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
        
        
class Test_lessons(Test_class):
    def test_create_lesson(self, client):
        response = client.post("/create_lesson", data = {
            "course_id": "1"
        })
        assert response.status_code == 302
        response = client.get("/lesson")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View Lesson #2\" href=\"/semester/1/course/1/lesson/2\"" in response.get_data(as_text = True)
        
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
        response = client.get("/lesson")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View Exercise \#1\" href=\"/exercise/1\"" in response.get_data(as_text = True)
        
        response = client.get("/semester/1/course/1/lesson/1000")
        assert response.status_code == 404
        
        response = client.get("/semester/1/course/1/lesson/0")
        assert response.status_code == 404
        
        response = client.get("/semester/1/course/1/lesson/-1")
        assert response.status_code == 404
        
    def test_change_lesson(self, client):
        response = client.post("/save_lesson", data = {
            "lesson_id": "4",
            "new_name": "test"
        })
        assert response.status_code == 302
        response = client.get("/lesson")
        assert response.status_code == 200
        assert "class=\"name\" title=\"View test\" href=\"/semester/1/course/1/lesson/2\"" in response.get_data(as_text = True)
        
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
        
    def test_delete_lesson(self, client):
        response = client.post("/delete_lesson", data = {
            "lesson_id": "4",
        })
        assert response.status_code == 302
        response = client.get("/lesson")
        assert response.status_code == 200
        assert not "href=\"/semester/1/course/1/lesson/2\"" in response.get_data(as_text = True)
        
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
        
        
class Test_exercises(Test_class):
    def test_create_exercise(self, client):
        response = client.post("/create_exercise", data = {
            "lesson_id": "1"
        })
        assert response.status_code == 302
        
    def test_get_exerciselist(self, client):
        response = client.get("/exercise")
        assert response.status_code == 200
        
    def test_get_specific_exercise(self, client):
        response = client.get("/exercise/1")
        assert response.status_code == 200
        
        response = client.get("/exercise/90000")
        assert response.status_code == 500
        
        response = client.get("/exercise/0")
        assert response.status_code == 500
        
        response = client.get("/exercise/-1")
        assert response.status_code == 404
        
    def test_change_exercise(self, client):
        response = client.post("/save_exercise", data = {
            "exercise_id": "1",
            "new_name": "test"
        })
        assert response.status_code == 302
        
        
class Test_prompts(Test_class):
    def test_create_prompt(self, client):
        response = client.post("/create_prompt", data = {
        })
        assert response.status_code == 200