DROP TABLE IF EXISTS system_prompt;
DROP TABLE IF EXISTS prompt;
DROP TABLE IF EXISTS fine_tuning;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS lesson;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS semester;

-- University-specific tables
CREATE TABLE semester (
    semester_id INTEGER PRIMARY KEY,
    semester_year INTEGER NOT NULL,
    semester_name TEXT NOT NULL
);

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    semester_id INTEGER NOT NULL,
    FOREIGN KEY (semester_id) REFERENCES semester(semester_id)
);

CREATE TABLE lesson (
    lesson_id INTEGER PRIMARY KEY,
    lesson_name TEXT,
    lesson_number INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE exercise (
    exercise_id INTEGER PRIMARY KEY,
    exercise_number INTEGER NOT NULL,
    exercise_content TEXT,
    exercise_solution TEXT,
    lesson_id INTEGER NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id)
);

-- ChatGPT-specific tables

CREATE TABLE system_prompt (
    system_prompt_id INTEGER PRIMARY KEY,
    system_prompt TEXT NOT NULL,
    lesson_id INTEGER NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id)
);

CREATE TABLE prompt (
    prompt_id INTEGER PRIMARY KEY,
    user_prompt TEXT NOT NULL,
    completion TEXT,
    exercise_id INTEGER,
    fine_tuning_id INTEGER,
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id),
    FOREIGN KEY (fine_tuning_id) REFERENCES fine_tuning(fine_tuning_id)
);