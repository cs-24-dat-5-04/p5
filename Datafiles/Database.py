import sqlite3


#Creates the database, then clears any previous tables and creates a new set.
Db = sqlite3.connect("Database.db")
cur = Db.cursor()

cur.execute("DROP TABLE IF EXISTS semester")
cur.execute("DROP TABLE IF EXISTS course")
cur.execute("DROP TABLE IF EXISTS lesson")
cur.execute("DROP TABLE IF EXISTS exercise")

cur.execute("CREATE TABLE IF NOT EXISTS semester(semester_id PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS course(course_id PRIMARY KEY, lessons, semester_id NOT NULL, FOREIGN KEY (semester_id) REFERENCES semester(semester_id))")
cur.execute("CREATE TABLE IF NOT EXISTS lesson(lesson_id NOT NULL, exercise_num, course_id NOT NULL, FOREIGN KEY (course_id) REFERENCES course(course_id))")
cur.execute("CREATE TABLE IF NOT EXISTS exercise(exercise_id NOT NULL, text NOT NULL, answer NOT NULL, lesson_id NOT NULL, course_id NOT NULL, FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id), FOREIGN KEY (course_id) REFERENCES course(course_id))")


#Populates database ##Currently just preliminary data for testing purposes
cur.execute("INSERT INTO semester VALUES (5)")
cur.execute("INSERT INTO course VALUES ('MI', 10, 5),('ASE', 12, 5),('DBS', 11, 5)")
cur.execute("INSERT INTO lesson VALUES (1, 4, 'MI'),(1, 4, 'ASE'),(1, 4, 'DBS')")
cur.execute("INSERT INTO exercise VALUES (1, 'text', 'answer', 1, 'MI'),(1, 'text', 'answer_wrong', 2, 'DBS'),(1, 'text_mistake', 'answer', 1, 'DBS')")
