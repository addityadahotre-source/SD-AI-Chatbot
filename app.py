from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__, static_folder=".", static_url_path="")

model = ChatMistralAI(model="mistral-small-latest", temperature=1)


conversation_history = [

]


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    conversation_history.append(HumanMessage(content=user_message))

    try:
        response = model.invoke(conversation_history)
    except Exception as exc: 
        conversation_history.pop()  
        return jsonify({"error": str(exc)}), 500

    conversation_history.append(AIMessage(content=response.content))

    return jsonify({"reply": response.content})


@app.route("/reset", methods=["POST"])
def reset():
    conversation_history.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
