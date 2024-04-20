import requests
import json
import os
from openai import OpenAI


OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPEN_AI_API_KEY)
# Set your OpenAI API key
# Step 1: Obtain authentication token
def get_auth_token():
    api_key = "df3b3faa-82dc-4111-92d4-66a7c6f6b026"
    response = requests.post("https://tasks.aidevs.pl/token/blogger", json={"apikey": api_key})
    data = response.json()
    if "token" in data:
        return data["token"]
    else:
        print("Failed to obtain authentication token:", data)
        return None

# Step 2: Download the task
def download_task(auth_token):
    response = requests.get(f"https://tasks.aidevs.pl/task/{auth_token}")
    data = response.json()
    
    return data
    
# Step 4: Prepare the answer array
def prepare_answer(data):
    answer = []
    for chapter in data["blog"]:
        m = [
            {
                "role": "system",
                "content": "Jesteś blogerem kuchennym. Twoim zadaniem jest opisać poszczególne etapy wykonywania pizzy hawajskiej",
            },
        ]
        for a in answer:
            m.append({"role": "user", "content": a[0]})
            m.append({"role": "assistant", "content": a[1]})
        m.append(
            {"role": "user", "content": chapter},
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=m,
        )
        print("# " + chapter)
        print(response.choices[0].message.content)
        answer.append(response.choices[0].message.content)

    return {'answer': answer}


# Step 5: Send the answer back
def send_answer(auth_token, answer):
    response = requests.post(f"https://tasks.aidevs.pl/answer/{auth_token}", json=answer)
    data = response.json()
    if "code" in data and data["code"] == 0:
        print("Answer submitted successfully!")
    else:
        print("Failed to submit answer:", data)

# Main function to orchestrate the process
def main():
    # Step 1: Obtain authentication token
    auth_token = get_auth_token()
    if auth_token is None:
        return
    
    # Step 2: Download the task
    task = download_task(auth_token)
    
    # Step 4: Prepare the answer array
    answer = prepare_answer(task)
    
    # Step 5: Send the answer back
    send_answer(auth_token, answer)

if __name__ == "__main__":
    main()