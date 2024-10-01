-- University-specific tables
DROP TABLE IF EXISTS semester;
CREATE TABLE semester (
    semester_id INTEGER PRIMARY KEY,
    semester_name TEXT NOT NULL
);

DROP TABLE IF EXISTS course;
CREATE TABLE course (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    semester_id INTEGER NOT NULL,
    FOREIGN KEY (semester_id) REFERENCES semester(semester_id)
);

DROP TABLE IF EXISTS lesson;
CREATE TABLE lesson (
    lesson_id INTEGER PRIMARY KEY,
    lesson_number INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

DROP TABLE IF EXISTS exercise;
CREATE TABLE exercise (
    exercise_id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    solution TEXT NOT NULL,
    lesson_id INTEGER NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id)
);

-- ChatGPT-specific tables
DROP TABLE IF EXISTS fine_tuning;
CREATE TABLE fine_tuning (
    fine_tuning_id INTEGER PRIMARY KEY,
    fine_tuning_name TEXT NOT NULL
);

DROP TABLE IF EXISTS prompt;
CREATE TABLE prompt (
    prompt_id INTEGER PRIMARY KEY,
    system_prompt TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    completion TEXT,
    fine_tuning_id INTEGER,
    FOREIGN KEY (fine_tuning_id) REFERENCES fine_tuning(fine_tuning_id)
);