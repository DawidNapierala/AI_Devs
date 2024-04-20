import requests
import os
from openai import OpenAI
import ai_devs_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
TASK_NAME = 'scraper'

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Scrape all data from this webpage {input} and answer user question
            """,
        ),
        ("user", "{question}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": task["input"], "question": task["question"]})
print(response.content)



ai_devs_template.send_answer(task_token, {'answer': response.content})