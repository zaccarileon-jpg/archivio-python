import json
import os
from datetime import datetime

FILE_UTENTI = "utenti.json"


# ---------- GESTIONE UTENTI ----------

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


def registra_utente():
    print("\n=== REGISTRAZIONE ===")
    utenti = carica_utenti()
    username = input("Scegli un username: ").strip()

    if username in utenti:
        print("⚠️ Username già esistente.")
        return None

    password = input("Scegli una password: ").strip()
    utenti[username] = {
        "password": password
    }
    salva_utenti(utenti)
    print("✅ Utente registrato.")
    return username


def login_utente():
    print("\n=== LOGIN ===")
    utenti = carica_utenti()
    if not utenti:
        print("Nessun utente registrato. Registrati prima.")
        return None

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in utenti and utenti[username]["password"] == password:
        print("✅ Login effettuato.")
        return username
    else:
        print("❌ Credenziali errate.")
        return None


# ---------- GESTIONE NOTE (PER UTENTE) ----------

def get_file_note(username):
    # ogni utente ha il suo file
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


# ---------- FUNZIONI DELL'APP DI NOTE ----------

def genera_id(note):
    if not note:
        return 1
    return max(n["id"] for n in note) + 1


def crea_nota(username, note):
    print("\n=== CREA NUOVA NOTA ===")
    titolo = input("Titolo: ").strip()
    testo = input("Testo / appunto: ").strip()
    fonte = input("Fonte (link/libro) [facoltativo]: ").strip()
    tags_raw = input("Tag separati da virgola: ").strip()
    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

    nuova = {
        "id": genera_id(note),
        "titolo": titolo,
        "testo": testo,
        "fonte": fonte,
        "tags": tags,
        "creata_il": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    note.append(nuova)
    salva_note(username, note)
    print("✅ Nota salvata.\n")


def lista_note(note):
    print("\n=== LE TUE NOTE ===")
    if not note:
        print("Nessuna nota.")
        return
    for n in note:
        print(f"[{n['id']}] {n['titolo']} ({n['creata_il']})  tags: {', '.join(n['tags'])}")
    print()


def mostra_nota(note):
    lista_note(note)
    if not note:
        return
    try:
        nota_id = int(input("ID nota da visualizzare: "))
    except ValueError:
        print("ID non valido.")
        return

    nota = next((n for n in note if n["id"] == nota_id), None)
    if not nota:
        print("Nota non trovata.")
        return

    print("\n=== DETTAGLI NOTA ===")
    print("Titolo:", nota["titolo"])
    print("Data:", nota["creata_il"])
    print("Fonte:", nota["fonte"] or "—")
    print("Tag:", ", ".join(nota["tags"]) or "—")
    print("\nTesto:")
    print(nota["testo"])
    print()


def cerca_per_tag(note):
    tag = input("Tag da cercare: ").strip().lower()
    risultati = [
        n for n in note
        if any(tag == t.lower() for t in n["tags"])
    ]
    print(f"\n=== RISULTATI PER TAG '{tag}' ===")
    if not risultati:
        print("Nessuna nota trovata.")
        return
    for n in risultati:
        print(f"[{n['id']}] {n['titolo']} ({n['creata_il']})")
    print()


def cerca_testo(note):
    parola = input("Testo da cercare: ").strip().lower()
    risultati = [
        n for n in note
        if parola in n["titolo"].lower() or parola in n["testo"].lower()
    ]
    print(f"\n=== RISULTATI PER '{parola}' ===")
    if not risultati:
        print("Nessuna nota trovata.")
        return
    for n in risultati:
        print(f"[{n['id']}] {n['titolo']} ({n['creata_il']})")
    print()


def elimina_nota(username, note):
    lista_note(note)
    if not note:
        return
    try:
        nota_id = int(input("ID nota da eliminare: "))
    except ValueError:
        print("ID non valido.")
        return

    nuova_lista = [n for n in note if n["id"] != nota_id]
    if len(nuova_lista) == len(note):
        print("Nota non trovata.")
        return

    salva_note(username, nuova_lista)
    print("🗑️ Nota eliminata.")
    # restituiamo la lista aggiornata al chiamante
    return nuova_lista


# ---------- MENU ----------

def mostra_menu_note(username):
    print(f"\n=== ARCHIVIO DI {username} ===")
    print("1) Crea nota")
    print("2) Elenca note")
    print("3) Mostra nota")
    print("4) Cerca per tag")
    print("5) Cerca per testo")
    print("6) Elimina nota")
    print("0) Esci")


def main():
    # fase login/registrazione
    while True:
        print("\n=== ACCESSO ===")
        print("1) Login")
        print("2) Registrati")
        print("0) Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            username = login_utente()
            if username:
                break
        elif scelta == "2":
            username = registra_utente()
            if username:
                break
        elif scelta == "0":
            print("Ciao 👋")
            return
        else:
            print("Scelta non valida.")

    # qui l'utente è autenticato
    note = carica_note(username)

    while True:
        mostra_menu_note(username)
        scelta = input("Scegli un'opzione: ").strip()

        if scelta == "1":
            crea_nota(username, note)
            note = carica_note(username)
        elif scelta == "2":
            lista_note(note)
        elif scelta == "3":
            mostra_nota(note)
        elif scelta == "4":
            cerca_per_tag(note)
        elif scelta == "5":
            cerca_testo(note)
        elif scelta == "6":
            nuova = elimina_nota(username, note)
            if nuova is not None:
                note = nuova
        elif scelta == "0":
            print("Ciao 👋")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()

