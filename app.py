from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET"])
def home():
    return """
    <html>
    <head>
        <title>Multi-Agent Assistant</title>
    </head>
    <body>
        <h1>🚀 Multi-Agent Assistant</h1>
        
        <input type="text" id="query" placeholder="Enter command (e.g., add task study)" size="40">
        <button onclick="sendRequest()">Submit</button>
        
        <h3>Response:</h3>
        <pre id="output"></pre>

        <script>
        function sendRequest() {
            let query = document.getElementById("query").value;

            fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({query: query})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText = JSON.stringify(data, null, 2);
            });
        }
        </script>
    </body>
    </html>
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