import requests
import os
from openai import OpenAI
import ai_devs_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
TASK_NAME = 'whoami'

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

task_token = ai_devs_template.get_auth_token(TASK_NAME)

for i in range(100):
    task = ai_devs_template.download_task(task_token)
    print(task)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
    We will play 'who am i?' game, i will give you hints one by one and you will have to answer If you can't guess who am i talking about and you are not 100% sure answer NO.
                """,
            ),
            ("user", "{input}"),
        ]
    )
    chain = prompt | model
    response = chain.invoke({"input": task["hint"]})
    print(response.content)
    guess = response.content

    if 'NO' in guess:
        continue
    else:
        ai_devs_template.send_answer(task_token, {'answer': guess})