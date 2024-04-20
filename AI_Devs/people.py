import json
from langchain_core.prompts import ChatPromptTemplate
import ai_devs_template
import requests
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def prepare_db():
    URL = "https://tasks.aidevs.pl/data/people.json"
    response = requests.get(URL)
    data = response.json()

    db = {}
    for d in data:
        name = d["imie"] + " " + d["nazwisko"]
        description = f"{d['o_mnie']}, ulubiony kolor: {d['ulubiony_kolor']}"
        db[name] = description
    with open("13-db.json", "w") as f:
        json.dump(db, f)


token = ai_devs_template.get_auth_token("people")
task = ai_devs_template.download_task(token)
prepare_db()


prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
    "Przykłady:###\nQ: Jaki jest ulubiony kolor Krysi Ludek?\nA: Krystyna Ludek\nQ: Gdzie mieszka Szymon Rumcajs?\nA: Szymon Rumcajs\nQ: Jakie jest ulubione jedzenie Magdaleny Kot?\nA: Magdalena Kot###".
                """,
            ),
            ("user", 'Podaj imię i nazwisko osoby. Imię w mianowniku. Jeśli imię jest zdrobnione, podaj niezdrobnioną wersję: {input}", model="gpt-4")'),
        ]
    )
chain = prompt | model
response = chain.invoke({"input": task["question"]})
print(response.content)
name = response.content


with open("13-db.json", encoding="utf-8") as f:
    db = json.load(f)
    prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
        "Answer briefly in POLISH. Context: ```{name}: {database}```".
                    """,
                ),
                ("user", 'Answer: {input}", model="gpt-4")'),
            ]
        )
    chain = prompt | model
    response = chain.invoke({"input": task["question"], "name": name, "database": db[name]})
    print(response.content)

ai_devs_template.send_answer(token, {'answer': response.content})
