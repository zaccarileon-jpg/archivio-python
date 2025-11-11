from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersegreto"  # per le sessioni, puoi cambiarlo

FILE_UTENTI = "utenti.json"


# ----- FUNZIONI DI SUPPORTO ----- #

def carica_utenti():
    if not os.path.exists(FILE_UTENTI):
        return {}
    with open(FILE_UTENTI, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def salva_utenti(utenti):
    with open(FILE_UTENTI, "w", encoding="utf-8") as f:
        json.dump(utenti, f, ensure_ascii=False, indent=2)


def get_file_note(username):
    return f"note_{username}.json"


def carica_note(username):
    file_note = get_file_note(username)
    if not os.path.exists(file_note):
        return []
    with open(file_note, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salva_note(username, note):
    file_note = get_file_note(username)
    with open(file_note, "w", encoding="utf-8") as f:
        json.dump(note, f, ensure_ascii=False, indent=2)


# ----- ROTTE ----- #

@app.route("/")
def index():
    # se loggato → vai a home
    if "username" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        utenti = carica_utenti()
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if username in utenti and utenti[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", errore="Credenziali errate")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        utenti = carica_utenti()
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if username in utenti:
            return render_template("register.html", errore="Username già esistente")

        utenti[username] = {"password": password}
        salva_utenti(utenti)
        session["username"] = username
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    note = carica_note(username)
    return render_template("home.html", username=username, note=note)


@app.route("/note/<int:nota_id>")
def nota_dettaglio(nota_id):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    note = carica_note(username)
    nota = next((n for n in note if n["id"] == nota_id), None)
    if not nota:
        return "Nota non trovata", 404
    return render_template("note.html", nota=nota, username=username)


@app.route("/new", methods=["GET", "POST"])
def nuova_nota():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]

    if request.method == "POST":
        titolo = request.form.get("titolo").strip()
        testo = request.form.get("testo").strip()
        fonte = request.form.get("fonte").strip()
        tags_raw = request.form.get("tags").strip()
        tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

        note = carica_note(username)
        new_id = max([n["id"] for n in note], default=0) + 1

        nuova = {
            "id": new_id,
            "titolo": titolo,
            "testo": testo,
            "fonte": fonte,
            "tags": tags,
            "creata_il": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        note.append(nuova)
        salva_note(username, note)
        return redirect(url_for("home"))

    return render_template("new_note.html", username=username)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
@app.route("/search")
def search():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    q = request.args.get("q", "").strip().lower()
    note = carica_note(username)

    if not q:
        risultati = []
    else:
        risultati = [
            n for n in note
            if q in n["titolo"].lower() or q in n["testo"].lower() or q in " ".join(n["tags"]).lower()
        ]

    return render_template("search.html", username=username, query=q, risultati=risultati)
@app.route("/delete/<int:nota_id>", methods=["POST"])
def delete_nota(nota_id):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    note = carica_note(username)
    nuove = [n for n in note if n["id"] != nota_id]
    salva_note(username, nuove)
    return redirect(url_for("home"))

@app.route("/edit/<int:nota_id>", methods=["GET", "POST"])
def edit_nota(nota_id):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    note = carica_note(username)
    nota = next((n for n in note if n["id"] == nota_id), None)
    if not nota:
        return "Nota non trovata", 404

    if request.method == "POST":
        nota["titolo"] = request.form.get("titolo").strip()
        nota["testo"] = request.form.get("testo").strip()
        nota["fonte"] = request.form.get("fonte").strip()
        tags_raw = request.form.get("tags").strip()
        nota["tags"] = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
        salva_note(username, note)
        return redirect(url_for("nota_dettaglio", nota_id=nota_id))

    # GET → mostra il form precompilato
    return render_template("edit_note.html", nota=nota, username=username)


if __name__ == "__main__":
    # avvia il server in locale
    app.run(debug=True)


