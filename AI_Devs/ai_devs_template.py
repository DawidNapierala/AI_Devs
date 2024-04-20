import requests

def get_auth_token(task):
    api_key = "df3b3faa-82dc-4111-92d4-66a7c6f6b026"
    response = requests.post(f"https://tasks.aidevs.pl/token/{task}", json={"apikey": api_key})
    data = response.json()
    if "token" in data:
        return data["token"]
    else:
        print("Failed to obtain authentication token:", data)
        return None

def download_task(auth_token):
    response = requests.get(f"https://tasks.aidevs.pl/task/{auth_token}")
    data = response.json()
    
    return data


def send_answer(auth_token, answer):
    response = requests.post(f"https://tasks.aidevs.pl/answer/{auth_token}", json=answer)
    data = response.json()
    if "code" in data and data["code"] == 0:
        print("Answer submitted successfully!")
    else:
        print("Failed to submit answer:", data)