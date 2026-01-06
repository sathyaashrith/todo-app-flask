from flask import Flask, render_template, request, redirect, url_for
from models import init_db, get_db
import logging

app = Flask(__name__)
init_db()

logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.form
    conn = get_db()
    conn.execute("""
        INSERT INTO tasks (title, description, due_date, priority)
        VALUES (?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["due_date"],
        data["priority"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/update/<int:id>")
def complete_task(id):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# 🔹 REGISTER API
from api import api
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
