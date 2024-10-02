-- Currently just preliminary data for testing purposes
INSERT INTO semester (semester_year, semester_name)
VALUES (2023, 'DAT5'), (2024, 'DAT5'), (2025, 'DAT5');

INSERT INTO course (course_name, semester_id) VALUES
('MI', (SELECT semester.semester_id FROM semester WHERE semester_year = 2024 AND semester_name = 'DAT5')),
('ASE', (SELECT semester.semester_id FROM semester WHERE semester_year = 2024 AND semester_name = 'DAT5')),
('DBS', (SELECT semester.semester_id FROM semester WHERE semester_year = 2024 AND semester_name = 'DAT5'));

INSERT INTO lesson (lesson_number, course_id)
SELECT 1, course.course_id 
FROM course 
JOIN semester ON course.semester_id = semester.semester_id 
WHERE course.course_name IN ('MI', 'ASE', 'DBS')
  AND semester.semester_year = 2024 
  AND semester.semester_name = 'DAT5';

INSERT INTO exercise (exercise_number, lesson_id)
SELECT 1, lesson.lesson_id
FROM lesson
JOIN course ON lesson.course_id = course.course_id
JOIN semester ON course.semester_id = semester.semester_id
WHERE course.course_name IN ('MI', 'ASE', 'DBS')
  AND semester.semester_year = 2024
  AND semester.semester_name = 'DAT5';
