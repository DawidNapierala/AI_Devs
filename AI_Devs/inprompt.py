import ai_devs_template
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

auth_token = ai_devs_template.get_auth_token("inprompt")

task = ai_devs_template.download_task(auth_token)

print(task)

# Use regular expression to find capitalized words
capitalized_words = re.findall(r'\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]*\b', task['question'])

# Join the capitalized words to form the name
name = ' '.join(capitalized_words)

print("Name retrieved from the question variable:", name)
data = []
for sentence in task['input']:
    if name in sentence:
        data.append(sentence)
    else :
        pass
print(data)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are working as a detector system. 
Answer the question based on this data: {data}
            """,
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": task['question'], "data": data})
print(response.content)

ai_devs_template.send_answer(auth_token, {'answer': response.content})