from boilerplate import *
from pprint import pprint
import ai_devs_template
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# oszukane, do poprawy
TASK_NAME = 'knowledge'
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Folow the instructions from {input} and answer user question based on one of the api's: {database1}, {database2}. If the question is about statistics answer only with number
            """,
        ),
        ("user", "{question}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": task["msg"], "question": task["question"], "database1": task["database #1"], "database2": task["database #2"]})
print(response.content)



ai_devs_template.send_answer(task_token, {'answer': response.content})