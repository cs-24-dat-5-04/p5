from openai import OpenAI
import time
import json

with open('secrets.json', 'r') as file:
    secrets = json.load(file)

client = OpenAI(
    api_key = secrets["api_key"]
)

training_file_name = "fine-tune/finetune_dataset_demo.jsonl"

#Uploading training file
training_data = client.files.create(
    file=open(training_file_name, "rb"),
    purpose="fine-tune"
)
print(f"Training ID: {training_data.id} \n")

#Create a fine-tuned model
response = client.fine_tuning.jobs.create(
  training_file=training_data.id, 
  model="gpt-4o-mini-2024-07-18"
)
print(f"Fine-tunning model ID: {response.id} \nFine-tunning model Status: {response.status}")

while response.status != "succeeded" or response.status != "failed":
    time.sleep(2)
    print(f"Status: {response.status}")


#res = client.fine_tuning.jobs.retrieve("ftjob-ytw7Mrzf5MNUvRPbqVmcnq1o")
#print(res)