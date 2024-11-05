from openai import OpenAI
import json

with open('secrets.json', 'r') as file:
    secrets = json.load(file)

client = OpenAI(
    organization = secrets["organization"],
    project = secrets["project"],
    api_key = secrets["api_key"],
)

job_id = "ftjob-106Ngs4SjW39rKCaoqLNEWwF"
model_id = "ft:gpt-4o-mini-2024-07-18:cs24dat504::AFOXcSn9"

# Retrieve the state of a fine-tune
def receive(id):
    return client.fine_tuning.jobs.retrieve(id)

# List models
def model_list():
    return client.models.list()

# Cancel a fine-tune job
def cancel(id):
    return client.fine_tuning.jobs.cancel(id)

# Delete a fine-tuned model (ft:gpt-4o-x models won’t accept a delete for some reason)
def delete(id):
    return client.models.delete(id) 

#print(receive(job_id))
#print(model_list())
#print(cancel(job_id))
#print(delete(model_id))
