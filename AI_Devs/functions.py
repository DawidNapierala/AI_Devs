from boilerplate import *
from pprint import pprint
import ai_devs_template
import os


TASK_NAME = 'functions'

API_KEY = os.getenv('API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

addUser = {
    "name": "addUser",
    "description": "Add a user to the database",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the user"
            },
            "surname": {
                "type": "string",
                "description": "The surname of the user"
            },
            "year": {
                "type": "integer",
                "description": "The year of birth of the user"
            }
        }
    },
}

response = ai_devs_template.send_answer(task_token, {'answer': addUser})
print(response)