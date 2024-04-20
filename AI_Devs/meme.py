import ai_devs_template
import requests
import os
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", temperature=0)

auth_token = ai_devs_template.get_auth_token("meme")

task = ai_devs_template.download_task(auth_token)

print(task)
image_url = task['image']
text = task['text']

renderform_apikey = os.getenv("RENDERFORM_API_KEY")
url = "https://get.renderform.io/api/v2/render"


generated_image = requests.post(f"https://api.renderform.io/api/v2/render",
                                headers={
                                    'X-API-KEY': renderform_apikey,
                                },
                                json={
                                    "template": 'yellow-bears-bake-smoothly-1976',
                                    "data": {
                                        "image.src": image_url,
                                        "text.text": text
                                    }
                                })
print(generated_image.json())
href = generated_image.json()['href']

data={'answer':href}

ai_devs_template.send_answer(auth_token, data)