import sys
import ai_devs_template
import json

auth_token = ai_devs_template.get_auth_token('ownapi')
task_data = ai_devs_template.download_task(auth_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))

data = {"answer": "https://04ab-89-77-116-90.ngrok-free.app/"}


ai_devs_template.send_answer(auth_token, data)