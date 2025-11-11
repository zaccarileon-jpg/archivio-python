# ----- FUNZIONI DI UTILITÀ ----- #

def login():
    password_corretta = "segreto123"
    tentativi = 0
    limite_tentativi = 3

    while tentativi < limite_tentativi:
        password_utente = input("Inserisci la password: ")

        if password_utente == password_corretta:
            print("Accesso consentito ✅")
            return True
        else:
            tentativi += 1
            print("Accesso negato ❌")
            print("Tentativi rimasti:", limite_tentativi - tentativi)

    print("Accesso bloccato. Troppi tentativi 🚫")
    return False


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


def saluta():
    nome = input("Come ti chiami? ")
    print("Ciao", nome, "👋")


# ----- PROGRAMMA PRINCIPALE ----- #

def mostra_menu():
    print("\n=== MENU PRINCIPALE ===")
    print("1) Login")
    print("2) Calcolatrice")
    print("3) Controllo età")
    print("4) Saluto")
    print("0) Esci")

def main():
    while True:
        mostra_menu()
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            esito = login()
            if not esito:
                # se il login fallisce non blocchiamo il programma, torniamo al menu
                pass
        elif scelta == "2":
            calcolatrice()
        elif scelta == "3":
            controllo_eta()
        elif scelta == "4":
            saluta()
        elif scelta == "0":
            print("Uscita dal programma. Ciao 👋")
            break
        else:
            print("Scelta non valida, riprova.")


# Avvia il programma
main()

