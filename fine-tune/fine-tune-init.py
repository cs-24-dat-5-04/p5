from openai import OpenAI
import time
import json
import sqlite3

with open('secrets.json', 'r') as file:
    secrets = json.load(file)

client = OpenAI(
    organization = secrets["organization"],
    project = secrets["project"],
    api_key = secrets["api_key"]
)

# Name of the training file
training_file_name = "finetune_dataset_demo"

# Convert db to jsonl
try:
    db = sqlite3.connect("fine-tune/database_name.db")
    cur = db.cursor()

    cur.execute("SELECT * from table_name")
    rows = cur.fetchall()

    data = []
    for row in rows:
        data.append({"messages":[{"role": "system", "content": row[0]},       # 
                                 {"role": "user", "content": row[1]},         # This is hard coded and need to be changed when integrated with the real database
                                 {"role": "assistant", "content": row[2]}]})  #

    with open("fine-tune/"+training_file_name+".jsonl", "w") as file:
        for data_line in data:
            json.dump(data_line, file)
            file.write("\n")
    
    db.close()
except Exception as e:
    print("An error has occured: ", e)

# Uploading training file
training_data = client.files.create(
    file=open("fine-tune/"+training_file_name+".jsonl", "rb"),
    purpose="fine-tune"
)
print(f"Training ID: {training_data.id}")

# Create a fine-tuned model
response = client.fine_tuning.jobs.create(
  training_file=training_data.id, 
  model="gpt-4o-mini-2024-07-18"#,
  #hyperparameters={
  #  "n_epochs":10,
  #  "batch_size":1,
  #  "learning_rate_multiplier":1.8
  #}
)
print(f"Fine-tunning model ID: {response.id} \nFine-tunning model Status: {response.status} \n")

# Check status
status = client.fine_tuning.jobs.retrieve(response.id).status
while not status == "succeeded" or status == "failed" or status == "cancelled":
    time.sleep(5)
    status = client.fine_tuning.jobs.retrieve(response.id).status
    print(f"Status: {status}")
