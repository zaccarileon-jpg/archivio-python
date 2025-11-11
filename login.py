# Programma di login con limite di tentativi

password_corretta = "segreto123"
tentativi = 0
limite_tentativi = 3

while tentativi < limite_tentativi:
    password_utente = input("Inserisci la password: ")

    if password_utente == password_corretta:
        print("Accesso consentito ✅")
        break
    else:
        tentativi += 1
        print("Accesso negato ❌")
        print("Tentativi rimasti:", limite_tentativi - tentativi)

if tentativi == limite_tentativi:
    print("Accesso bloccato. Troppi tentativi 🚫")

         
