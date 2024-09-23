from flask import Flask, render_template, request
from openai import OpenAI
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def hello():
    output = ""  # Initialize output variable
    if request.method == 'POST':
        prompt = request.form['Prompt']  # Get the prompt from the form
        # Generate a response based on the prompt (this is just an example)
        with open('secrets.json', 'r') as file:
            secrets = json.load(file)

        client = OpenAI(
        organization = secrets["organization"],
        project = secrets["project"],
        api_key = secrets["api_key"],
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens = 50
        )
        output = completion.choices[0].message.content
    
    return render_template("index.html", output=output)  # Pass output to template

if __name__ == '__main__':
   app.run(debug=True)
