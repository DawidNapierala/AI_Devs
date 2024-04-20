import requests
import os
from openai import OpenAI

# Set your OpenAI API key
OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)

# Step 1: Obtain authentication token
def get_auth_token():
    api_key = "df3b3faa-82dc-4111-92d4-66a7c6f6b026"
    response = requests.post("https://tasks.aidevs.pl/token/moderation", json={"apikey": api_key})
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
    
    return data['input']
    
# Step 4: Prepare the answer array
def prepare_answer(sentences):
    answer = []
    for sentence in sentences:
        response = client.moderations.create(input=sentence, model='text-moderation-latest')
        flagged = any(result.flagged for result in response.results)
        answer.append(1 if flagged else 0)
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