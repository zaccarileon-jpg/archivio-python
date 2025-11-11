import json
import os
from datetime import datetime

FILE_DATI = "archivio_dati.json"


# ---------- UTILITÀ FILE ----------

def carica_dati():
    """Carica i dati dal file JSON, se esiste."""
    if not os.path.exists(FILE_DATI):
        return []
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salva_dati(dati):
    """Salva la lista di note nel file JSON."""
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)


# ---------- FUNZIONI DELL'APP ----------

def crea_nota(dati):
    print("\n=== CREA NUOVA NOTA ===")
    titolo = input("Titolo: ").strip()
    testo = input("Testo / appunto: ").strip()
    fonte = input("Fonte (link, libro, ecc.) [facoltativo]: ").strip()
    tags_raw = input("Tag separati da virgola (es. italia, strategia, usa): ").strip()

    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

    nota = {
        "id": genera_id(dati),
        "titolo": titolo,
        "testo": testo,
        "fonte": fonte,
        "tags": tags,
        "creata_il": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    dati.append(nota)
    salva_dati(dati)
    print("✅ Nota creata e salvata.\n")


def genera_id(dati):
    """Genera un ID incrementale semplice."""
    if not dati:
        return 1
    ids = [n["id"] for n in dati]
    return max(ids) + 1


def lista_note(dati):
    print("\n=== TUTTE LE NOTE ===")
    if not dati:
        print("Nessuna nota salvata.")
        return
    for nota in dati:
        print(f"[{nota['id']}] {nota['titolo']}  ({nota['creata_il']})  tags: {', '.join(nota['tags'])}")
    print()


def mostra_nota(dati):
    lista_note(dati)
    try:
        nota_id = int(input("ID della nota da visualizzare: "))
    except ValueError:
        print("ID non valido.\n")
        return

    nota = next((n for n in dati if n["id"] == nota_id), None)
    if not nota:
        print("Nota non trovata.\n")
        return

    print("\n=== DETTAGLI NOTA ===")
    print("Titolo:", nota["titolo"])
    print("Creata il:", nota["creata_il"])
    print("Fonte:", nota["fonte"] if nota["fonte"] else "—")
    print("Tag:", ", ".join(nota["tags"]) if nota["tags"] else "—")
    print("\nTesto:")
    print(nota["testo"])
    print()


def cerca_per_tag(dati):
    tag = input("Inserisci il tag da cercare: ").strip().lower()
    risultati = [n for n in dati if tag in [t.lower() for t in n["tags"]]]
    print(f"\n=== RISULTATI PER TAG '{tag}' ===")
    if not risultati:
        print("Nessuna nota trovata.")
        return
    for nota in risultati:
        print(f"[{nota['id']}] {nota['titolo']}  ({nota['creata_il']})")
    print()


def cerca_testo(dati):
    parola = input("Parola o frase da cercare nel testo/titolo: ").strip().lower()
    risultati = []
    for n in dati:
        if parola in n["titolo"].lower() or parola in n["testo"].lower():
            risultati.append(n)

    print(f"\n=== RISULTATI PER '{parola}' ===")
    if not risultati:
        print("Nessuna nota trovata.")
        return

    for nota in risultati:
        print(f"[{nota['id']}] {nota['titolo']}  ({nota['creata_il']})")
    print()


def elimina_nota(dati):
    lista_note(dati)
    try:
        nota_id = int(input("ID della nota da eliminare: "))
    except ValueError:
        print("ID non valido.\n")
        return

    nuova_lista = [n for n in dati if n["id"] != nota_id]

    if len(nuova_lista) == len(dati):
        print("Nota non trovata.\n")
        return

    salva_dati(nuova_lista)
    print("🗑️ Nota eliminata.\n")


def mostra_menu():
    print("\n=== ARCHIVIO APPUNTI ===")
    print("1) Crea nuova nota")
    print("2) Elenca tutte le note")
    print("3) Mostra dettagli nota")
    print("4) Cerca per tag")
    print("5) Cerca per testo")
    print("6) Elimina nota")
    print("0) Esci")


def main():
    dati = carica_dati()

    while True:
        mostra_menu()
        scelta = input("Scegli un'opzione: ").strip()

        if scelta == "1":
            crea_nota(dati)
        elif scelta == "2":
            lista_note(dati)
        elif scelta == "3":
            mostra_nota(dati)
        elif scelta == "4":
            cerca_per_tag(dati)
        elif scelta == "5":
            cerca_testo(dati)
        elif scelta == "6":
            # ricarichiamo i dati dopo l'eliminazione
            elimina_nota(dati)
            dati = carica_dati()
        elif scelta == "0":
            print("Ciao 👋")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()


