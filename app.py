from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("guestbook.db")


# Skapa tabellen första gången
con = db()
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    message TEXT
)
""")
con.commit()
con.close()


@app.route("/")
def index():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT title, message FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    con.close()

    return render_template("index.html", posts=posts)


@app.route("/save", methods=["POST"])
def save():
    title = request.form["title"]
    message = request.form["message"]

    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO posts(title, message) VALUES(?, ?)",
        (title, message)
    )
    con.commit()
    con.close()

    return redirect("/")


app.run(debug=True)
