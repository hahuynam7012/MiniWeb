from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = r"D:\Project\MiniWeb\static\database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM username").fetchall()
    conn.close()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    conn = get_db_connection()
    conn.execute("INSERT INTO username (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_user(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM username WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit_user(id):
    name = request.form["name"]
    email = request.form["email"]
    conn = get_db_connection()
    conn.execute("UPDATE username SET name = ?, email = ? WHERE id = ?", (name, email, id))
    conn.commit()
    conn.close()  
    return redirect(url_for("index"))

if __name__ == "__main__":
    # chạy trên tất cả host, port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
