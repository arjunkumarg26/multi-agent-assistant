from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET"])
def home():
    return """
    <h1>🚀 Multi-Agent Assistant</h1>
    <p>System is running successfully on Cloud Run.</p>
    <p><b>Available API:</b></p>
    <ul>
        <li>POST / → add/show tasks</li>
    </ul>
    <p>Use curl or Postman to interact.</p>
    """

@app.route("/", methods=["POST"])
def handle_request():
    data = request.get_json()
    query = data.get("query", "").lower()

    if "add task" in query:
        task = query.replace("add task", "").strip()
        tasks.append(task)
        return jsonify({"response": f"Task added: {task}"})

    elif "show tasks" in query:
        return jsonify({"response": tasks})

    else:
        return jsonify({"response": "Unknown command"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)