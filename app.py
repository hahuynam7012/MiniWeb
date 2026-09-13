from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import quote
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
DB_PATH = r"D:\Project\MiniWeb\static\database.db"
UPLOAD_FOLDER = os.path.join(app.static_folder, "StockImage")


def save_uploaded_image(file):
    if file is None or file.filename == "":
        return "default.png"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filename


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0,
            image TEXT NOT NULL DEFAULT 'default.png'
        )
        """
    )

    columns = [row[1] for row in conn.execute("PRAGMA table_info(products)").fetchall()]
    if "image" not in columns:
        conn.execute("ALTER TABLE products ADD COLUMN image TEXT NOT NULL DEFAULT 'default.png'")

    legacy_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='username'"
    ).fetchone()

    if legacy_exists:
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            legacy_rows = conn.execute("SELECT name, email FROM username").fetchall()
            for row in legacy_rows:
                conn.execute(
                    "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
                    (row["name"], 0.0, "default.png"),
                )

    conn.commit()
    conn.close()


init_db()


@app.route("/")
@app.route("/mua")
def buy():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("buy.html", products=products)


@app.route("/ban")
def sell():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("sell.html", products=products)


@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    price = request.form["price"].strip()
    image_file = request.files.get("image")
    image = save_uploaded_image(image_file)

    if not name or not price:
        return redirect(url_for("sell"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        (name, float(price), image),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("sell"))


@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("sell"))


@app.route("/edit/<int:id>", methods=["POST"])
def edit_product(id):
    name = request.form["name"].strip()
    price = request.form["price"].strip()
    image_file = request.files.get("image")
    image = save_uploaded_image(image_file)

    if not name or not price:
        return redirect(url_for("sell"))

    conn = get_db_connection()
    current = conn.execute("SELECT image FROM products WHERE id = ?", (id,)).fetchone()
    if current and not image_file:
        image = current["image"]

    conn.execute(
        "UPDATE products SET name = ?, price = ?, image = ? WHERE id = ?",
        (name, float(price), image, id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("sell"))


@app.route("/checkout/<int:id>")
def checkout(id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()
    conn.close()

    if product is None:
        return redirect(url_for("buy"))

    product_name = product["name"]
    payment_text = f"ProductID:{product['id']}|Name:{product_name}|Price:{product['price']}"
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=" + quote(payment_text)

    return render_template(
        "checkout.html",
        product=product,
        qr_url=qr_url,
        payment_text=payment_text,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
