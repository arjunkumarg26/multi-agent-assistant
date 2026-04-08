from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)")
conn.commit()

# Task agent
def task_agent(query):
    if "add task" in query:
        task = query.replace("add task", "")
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        return f"Task added: {task}"
    elif "show tasks" in query:
        cursor.execute("SELECT * FROM tasks")
        return str(cursor.fetchall())

# Notes agent
def notes_agent(query):
    if "add note" in query:
        note = query.replace("add note", "")
        cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
        conn.commit()
        return f"Note added: {note}"
    elif "show notes" in query:
        cursor.execute("SELECT * FROM notes")
        return str(cursor.fetchall())

# Main agent
def main_agent(query):
    if "task" in query:
        return task_agent(query)
    elif "note" in query:
        return notes_agent(query)
    else:
        return "Not understood"

# API route
@app.route("/", methods=["POST"])
def home():
    data = request.json
    query = data.get("query")
    result = main_agent(query)
    return jsonify({"response": result})

# Run app
app.run(host="0.0.0.0", port=8080)
