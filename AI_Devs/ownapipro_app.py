from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = ChatOpenAI()
# ConversationChain automaticaly appends every message to Memory
# In other words every time user is sending requests model sees all previous messages
conversation = ConversationChain(
    llm=chat, verbose=True, memory=ConversationBufferMemory()
)

def get_response_to_user_request(question):
    response = conversation.predict(input=question)
    return(response)

from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_response_to_user_question():

    if request.method == 'POST':
        # Get user question
        print("Request JSON data:", request.json)
        print("User question is: ", request.json['question'])


        # Generate answer
        answer = get_response_to_user_request(question=request.json['question'])
        
        print("Answer to user question is", answer)
        formatted_answer = {"reply":answer}

    return formatted_answer

if __name__ == '__main__':
    app.run(port=5000)