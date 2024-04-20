import ai_devs_template
import requests, os
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

auth_token = ai_devs_template.get_auth_token("liar")

task = ai_devs_template.download_task(auth_token)


def get_answer(token, debug=False):
    url = "https://tasks.aidevs.pl/task/" + token
    response = requests.post(url, data={"question": "What year was the Polish baptism?"})
    response.raise_for_status()
    if debug:
        print(response.json())
    return response.json()


answer = get_answer(auth_token, True)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are working as a detector system. 
Please check if this sentence is answer to question about what year was the Polish baptism.
Answer only YES or NO.
            """,
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": answer["answer"]})
print(response.content)

ai_devs_template.send_answer(auth_token, {'answer': response.content})
