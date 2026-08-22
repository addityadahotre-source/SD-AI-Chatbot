
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage

model = ChatMistralAI(model="mistral-small-latest", temperature=1)

messages = []

print("________Welcome to chatbot, type 0 to exit____________")
while True:
    prompt = input("You : ")
    if prompt == "0":
        break

    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot :", response.content)

print(messages)
