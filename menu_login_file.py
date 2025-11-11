# --- FUNZIONI BASE --- #

def carica_utenti():
    utenti = {}
    try:
        with open("utenti.txt", "r") as file:
            for riga in file:
                if ":" in riga:
                    nome, password = riga.strip().split(":")
                    utenti[nome] = password
    except FileNotFoundError:
        print("File utenti non trovato! ⚠️")
    return utenti


def login(utenti):
    print("=== LOGIN ===")
    tentativi = 0
    limite = 3

    while tentativi < limite:
        nome = input("Nome utente: ")
        password = input("Password: ")

        if nome in utenti and utenti[nome] == password:
            print("Accesso consentito ✅")
            return True, nome
        else:
            tentativi += 1
            print("Credenziali errate ❌")
            print("Tentativi rimasti:", limite - tentativi)

    print("Accesso bloccato 🚫")
    return False, None


def calcolatrice():
    print("=== CALCOLATRICE ===")
    n1 = float(input("Primo numero: "))
    n2 = float(input("Secondo numero: "))
    operazione = input("Operazione (+, -, *, /): ")

    if operazione == "+":
        risultato = n1 + n2
    elif operazione == "-":
        risultato = n1 - n2
    elif operazione == "*":
        risultato = n1 * n2
    elif operazione == "/":
        if n2 == 0:
            print("Errore: divisione per zero ❌")
            return
        risultato = n1 / n2
    else:
        print("Operazione non valida")
        return

    print("Risultato:", risultato)


def controllo_eta():
    print("=== CONTROLLO ETÀ ===")
    eta = int(input("Quanti anni hai? "))
    if eta >= 18:
        print("Sei maggiorenne ✅")
    else:
        print("Sei minorenne ❌")


# --- PROGRAMMA PRINCIPALE --- #

def mostra_menu():
    print("\n=== MENU PRINCIPALE ===")
    print("1) Calcolatrice")
    print("2) Controllo età")
    print("0) Esci")


def main():
    utenti = carica_utenti()
    autenticato, nome = login(utenti)

    if not autenticato:
        print("Chiusura programma 🔒")
        return

    print(f"\nBenvenuto, {nome}! 👋")

    while True:
        mostra_menu()
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            calcolatrice()
        elif scelta == "2":
            controllo_eta()
        elif scelta == "0":
            print("Uscita dal programma. Ciao 👋")
            break
        else:
            print("Scelta non valida.")


main()

