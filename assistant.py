import os
from openai import OpenAI
import openai
# client = OpenAI()
API_TOKEN = os.getenv('OPENAI_API_KEY')
# OpenAI.api_key = API_TOKEN
import json
import requests
import httpx
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
def file_download(api_token, file_id):
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": "Bearer " + api_token
    }
    response = httpx.get(url + '/' + file_id, headers=headers)
    print(response.json())
    filename = path_leaf(response.json()['filename'])
    file_content = httpx.get(url + '/' + file_id + '/content', headers=headers)
    with open(filename, mode='wb') as f:
        f.write(file_content.content)
def file_upload(api_token, filename):
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": "Bearer " + api_token
    }
    # Make a POST request to OpenAI API
    data = {
        "purpose": "assistants",
    }
    files = {
        "file": open(filename, "rb")
    }
    with httpx.Client() as client:
        response = client.post(url, headers=headers, data=data, files=files)

    # Process the response
    if response.status_code == 200:
        file_id = response.json()['id']
        print(f"File uploaded successfully. File ID: {file_id}")
        return file_id
    else:
        print(f"Failed to upload file. Status code: {response.status_code}, Error: {response.text}")

def getOpenaiClient():
    return OpenAI( api_key=os.getenv('OPENAI_API_KEY'))

def getAssistant(Name, Instructions, client, tools=None):
    # retrieve an OpenAI assistant by Name or create one if not found.
    # in that case you should add your getTools() call so that the assistant
    # is created with the right tools attached to it.
    aa = client.beta.assistants.list()
    assistant = None
    for a in aa.data:
        if a.name == Name:
            assistant = a
            break
    if assistant is None: # create a new Agent
        assistant = client.beta.assistants.create(name=Name,
        instructions=Instructions,
        tools=tools,
        model="gpt-3.5-turbo-16k")
    return assistant

#Step 1: Retrieve an Assistant
client = getOpenaiClient()
my_assistant = getAssistant('Terraform AI',
                            '''You are an assistant to help me write Terraform code. 
                                        I will upload a file containing terraform code and you will process my request to modify it.
                                        Use the code interpreter to create and output file. The output should always be a tfvars file or multiple files that I can download''',
                            client, tools=None, )
print(f"This is the assistant object: {my_assistant} \n")

# Step 2: Create a Thread
my_thread = client.beta.threads.create()
print(f"This is the thread object: {my_thread} \n")

file_id = file_upload(API_TOKEN, 'roles.tfvars')

# Step 3: Add a Message to a Thread. The content is the request we want the AI to perform
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role='user',
  content='''I want to create a new custom role for cosmosdb reader. 
  Use a similar role name than the one existing in the file. 
  Use the same subscription.Append a unique suffix to the filename. Add it in the custom_roles array. The tfvars files are not json files''',
  file_ids=[file_id]
)
print(f"This is the message object: {my_thread_message} \n")

# Step 4: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id,
)
print(f"This is the run object: {my_run} \n")

# Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
while my_run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")
        break

# Step 6: Retrieve the Messages added by the Assistant to the Thread
all_messages = client.beta.threads.messages.list(
  thread_id=my_thread.id
)

print("------------------------------------------------------------ \n")

print(f"User: {my_thread_message.content[0].text.value}")
print(f"Assistant: {all_messages.data[0].content[0].text.value}")
print(all_messages)
outputFiles = all_messages.data[0].file_ids
print(all_messages.data[0].file_ids)
for file_id in outputFiles:
    file_download(API_TOKEN, file_id)
