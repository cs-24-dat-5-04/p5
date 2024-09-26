from flask import Flask, render_template, request
from openai import OpenAI
import markdown
import json

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
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
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens = 50
        )
        output = markdown.markdown(completion.choices[0].message.content)
    return render_template("index.html", output=output)

if __name__ == '__main__':
   app.run(debug=True)