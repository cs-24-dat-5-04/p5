
from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, Time, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from openai import OpenAI
from models import Course, Exercise, FineTuning, Lesson, Prompt, Semester
import sys
import markdown
import json

app = Flask(__name__)
engine = create_engine('sqlite:///./database.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['GET', 'POST'])

def hello():
    output = "Hello! How can I assist you today?"
    if request.method == 'POST':
        prompt = request.form['prompt']
        model = request.form['model']
        with open('secrets.json', 'r') as file:
            secrets = json.load(file)

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
        #markdown.markdown(completion.choices[0].message.content)

        user_prompt = Prompt(user_prompt = prompt, completion = output)
        session.add(user_prompt)
        session.commit()


    return render_template("index.html", output=output)
#create a system prompt, update it with user prompt and both return ID. 

#def create_prompt(prompt, output):
    
 #   return new_prompt.prompt_id

#def save_system_prompt(prompt_id):
#    new_system_prompt = Prompt.system_prompt()
#    session.add(new_system_prompt)
#    session.commit
#    return new_system_prompt.system_prompt

def save_user_prompt(prompt_id):
    new_user_prompt = Prompt.user_prompt()
    session.add(new_user_prompt)
    session.commit
    return new_user_prompt.user_prompt

if __name__ == '__main__':
   app.run(debug=True)
