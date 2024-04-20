import sys
sys.path.append(r'..')
from ai_devs_template import get_auth_token, download_task, send_answer
import json

auth_token = get_auth_token('ownapipro')
task_data = download_task(auth_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))

data = {"answer": "https://bf4b-89-77-116-90.ngrok-free.app"}


send_answer(auth_token, data)