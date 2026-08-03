"""
メモ・ToDoアプリ（入力・処理・出力を持つシンプルなWebアプリ）
- 入力: タスクの追加フォーム（タイトル・メモ内容）
- 処理: Flaskがリクエストを受け取り、SQLiteデータベースを操作
- 出力: タスク一覧をHTMLとして描画、完了状態や削除もリアルタイム反映
"""

import os
import sqlite3
from datetime import datetime

from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "memo_todo.db")


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


# ---- 入力: タスク一覧取得（出力） ----
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    db = get_db()
    rows = db.execute(
        "SELECT id, title, content, done, created_at FROM tasks ORDER BY id DESC"
    ).fetchall()
    tasks = [dict(row) for row in rows]
    return jsonify(tasks)


# ---- 入力: 新規タスク追加（処理） ----
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title:
        return jsonify({"error": "タイトルは必須です"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO tasks (title, content, done, created_at) VALUES (?, ?, 0, ?)",
        (title, content, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    db.commit()
    return jsonify({"message": "追加しました"}), 201


# ---- 処理: 完了状態の切り替え ----
@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    db = get_db()
    row = db.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify({"error": "タスクが見つかりません"}), 404

    new_done = 0 if row["done"] else 1
    db.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_done, task_id))
    db.commit()
    return jsonify({"done": new_done})


# ---- 処理: タスク削除 ----
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return jsonify({"message": "削除しました"})


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
