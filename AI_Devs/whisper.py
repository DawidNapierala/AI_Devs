from boilerplate import *
from pprint import pprint
import ai_devs_template
import os
from openai import OpenAI
import requests


TASK_NAME = 'whisper'

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

url = 'https://tasks.aidevs.pl/data/mateusz.mp3'
response = requests.get(url)

if response.status_code == 200:
    with open('mateusz.mp3', 'wb') as audio_file:
        audio_file.write(response.content)

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open('mateusz.mp3', 'rb')
    )
    
    print(transcription.text)
else:
    print("Failed to download the file")

response = ai_devs_template.send_answer(task_token, {'answer': transcription.text})
print(response)