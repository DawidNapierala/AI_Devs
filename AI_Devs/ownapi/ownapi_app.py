from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def get_response_to_user_request(question):
    chat = ChatOpenAI(model="gpt-4")
    response = chat.invoke(input=[
        SystemMessage(content="Answer the user question."),
        HumanMessage(content=question)
        ])
    return(response.content)

# --------------------------------------------------------------
# Create flask app
# --------------------------------------------------------------
from flask import Flask, request
app = Flask(__name__)

# --------------------------------------------------------------
# Define available methods and route
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Start app
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(port=5000)