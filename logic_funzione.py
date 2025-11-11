

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


esito = login()

if esito:
    print("Benvenuto nel sistema 👋")
else:
    print("Chiusura programma 🔒")

