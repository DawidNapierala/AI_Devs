from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import requests
import ai_devs_template
import json
from datetime import datetime

from boilerplate import *
import os

TASK_NAME = 'tools'

OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

llm = ChatOpenAI(openai_api_key=OPEN_AI_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     'I Decide whether the task should be added to the ToDo list or to the calendar (if time is provided) '
     'and return the corresponding JSON. '
     'I always use YYYY-MM-DD format for dates \n'
     'If task has provided duration, and not date I classify as ToDo\n'
     'For example:\n'
     'Q: Jutro mam spotkanie z Marianem\n'
     'A: {{"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2024-04-10"}}\n'
     'Q: Przypomnij mi, że mam kupić mleko\n'
     'A: {{"tool":"ToDo","desc":"Kup mleko" }}\n'
     'Context:###:\n'
     'Today is: {date}\n'),
    ("user", "{question}")
])

chain = prompt | llm

task_token = ai_devs_template.get_auth_token(TASK_NAME)
task = ai_devs_template.download_task(task_token)
print(task)

question = task['question']
print(question)

llm_answer = chain.invoke({"question": question, "date": datetime.now().strftime("%Y-%m-%d")}).content
print(llm_answer)

answer = json.loads(llm_answer)
print(answer)

result = ai_devs_template.send_answer(task_token, {'answer': answer})
print(result)

questions = [
    "Potrzebuję kupić bułki",
    "Jutro mam spotkanie z Marianem",
    "We wtorek za tydzień, potrzebuję zrobić badania krwi",
    "Za rok o tej porze, wezmę udział w kursie języka angielskiego",
    "9 maja, koniec prawo jazdy",
    "1 września ślub",
    "30 września rozwód",
    "Opłacić rachunki",
    "Kupić wałek",
    "Sprzedać samochód",
    "Odeślij email z podziękowaniem za ostatnią rozmowę służbową.",
    "Umów się na wizytę u dentysty na przyszły tydzień.",
    "Posprzątaj kuchnię i zmyj naczynia.",
    "Skontaktuj się z przyjacielem, z którym dawno nie rozmawiałeś.",
    "Zapisz się na kurs jogi lub innej formy aktywności fizycznej.",
    "Przeczytaj co najmniej jeden rozdział książki przed snem.",
    "Zrób listę zakupów na najbliższy tydzień.",
    "Odpisz na wszystkie zaległe wiadomości tekstowe.",
    "Znajdź 15 minut na medytację lub relaksację."
]

for question in questions:
    print(question)
    llm_answer = chain.invoke({"question": question, "date": datetime.now().strftime("%Y-%m-%d")}).content
    print(llm_answer)