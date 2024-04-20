from boilerplate import *
import ai_devs_template
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# oszukane, do poprawy
TASK_NAME = 'gnome'
model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


task_token = ai_devs_template.get_auth_token(TASK_NAME)

task = ai_devs_template.download_task(task_token)
print(task)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
# Analize this drawing {question} of a gnome with a hat on his head. Tell me in one word what is the color of the hat in POLISH. If you can't specify the color or if the drawing does not contain gnome, return "ERROR" as answer.
# Remember {hint}'
#             """,
#         ),
#     ]
# )
# chain = prompt | model
# response = chain.invoke({"input": task["msg"], "question": task["url"], "hint": task["hint"]})
# print(response.content)
from openai import OpenAI

client = OpenAI(api_key=OPEN_AI_API_KEY)

response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": task["msg"]},
        {
          "type": "image_url",
          "image_url": {
            "url": task["url"],
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])

ai_devs_template.send_answer(task_token, {'answer': response.content})