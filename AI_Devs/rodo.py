import requests
import os
from openai import OpenAI
import ai_devs_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
TASK_NAME = 'rodo'

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

message = """Weż głeboki oddech przed udzieleniem odpowiedzi. Nie podawaj informacji osobistych a jedynie placeholdery. Upewnij się, że odpowiedź zawiera wszystkie placeholdery:
    - '%imie%'
    - '%nazwisko%'
    - '%zawod%'
    - '%miasto%'
    """


ai_devs_template.send_answer(task_token, {'answer': message})