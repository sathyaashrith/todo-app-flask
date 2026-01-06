from flask import Blueprint, jsonify, request
from models import get_db

api = Blueprint("api", __name__)

@api.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@api.route("/api/tasks/<int:id>", methods=["GET"])
def get_task(id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()
    conn.close()
    if task:
        return jsonify(dict(task))
    return jsonify({"error": "Task not found"}), 404

@api.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, priority) VALUES (?, ?)",
        (data["title"], data.get("priority", "Medium"))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task created"}), 201

@api.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (data.get("status", "Completed"), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated"})

@api.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})

@api.route("/api/health")
def health():
    return jsonify({"status": "API is running"})
