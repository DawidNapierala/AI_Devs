import ai_devs_template, os
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from openai import OpenAI

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPEN_AI_API_KEY)

def get_embedding(text: str, model="text-embedding-ada-002", **kwargs) -> list[float]:
    text = text.replace("\n", " ")
    return client.embeddings.create(input=text, model=model).data[0].embedding

COLLECTION = 'AI_DEVS'
def populate_qdrant(client: QdrantClient):
    qdrant_client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

    URL = "https://unknow.news/archiwum_aidevs.json"

    response = requests.get(URL)
    data = response.json()

    points = []
    for idx, d in enumerate(data):
        description = d["title"] + " " + d["info"]
        embedding = get_embedding(description)
        points.append(PointStruct(id=idx, vector=embedding, payload={"url": d["url"]}))

    qdrant_client.upsert(collection_name=COLLECTION, points=points)


qdrant_client = QdrantClient(url="localhost:54356")
populate_qdrant(qdrant_client)

token = ai_devs_template.get_auth_token("search")
task = ai_devs_template.download_task(token)

query_embedding = get_embedding(task["question"])
answer = qdrant_client.search(collection_name=COLLECTION, query_vector=query_embedding, limit=1)[0]

ai_devs_template.send_answer(token, {'answer': answer.payload["url"]})