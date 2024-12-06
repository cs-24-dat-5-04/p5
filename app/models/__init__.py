from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .semester import Semester
from .course import Course
from .lesson import Lesson
from .exercise import Exercise
from .fine_tuning import FineTuning
from .prompt import Prompt
from .system_prompt import SystemPrompt
