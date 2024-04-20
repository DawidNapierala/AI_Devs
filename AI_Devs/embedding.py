import ai_devs_template
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
import openai

# Ustawienie klucza API
OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)

auth_token = ai_devs_template.get_auth_token("embedding")
# Generowanie embeddingu dla tekstu
response = client.embeddings.create(
    input="Hawaiian pizza",
    model="text-embedding-ada-002"
)

# Extracting the embedding from the response
embedding = response.data[0].embedding
print(len(embedding))

# Pobranie wygenerowanego embeddingu
embedding_vector = embedding

# Sprawdzenie długości embeddingu
print(len(embedding_vector))
# Powinno wydrukować: 1536

# Wydrukowanie embeddingu w odpowiednim formacie
print({"answer": embedding_vector})

ai_devs_template.send_answer(auth_token, {'answer': embedding_vector})