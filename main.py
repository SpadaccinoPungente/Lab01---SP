import random


# 1. Definiamo la classe base per contenere i dati della singola domanda
class Domanda:
    def __init__(self, testo, livello, corretta, errata1, errata2, errata3):
        self.testo = testo
        self.livello = int(livello)
        self.corretta = corretta
        # Salviamo tutte le risposte in una lista per comodità
        self.risposte = [corretta, errata1, errata2, errata3]


# 2. Funzione per leggere il file txt e creare le domande
def carica_domande(nome_file):
    domande_per_livello = {}

    with open(nome_file, 'r', encoding='utf-8') as f:
        # Leggiamo tutte le righe, ma teniamo SOLO quelle che non sono vuote
        # Questo ci salva dal problema della riga vuota tra una domanda e l'altra
        righe = [riga.strip() for riga in f if riga.strip()]

    # Analizziamo la lista a blocchi di 6 (proprio come dicevamo prima!)
    for i in range(0, len(righe), 6):
        if i + 5 < len(righe):  # Controllo di sicurezza
            d = Domanda(righe[i], righe[i + 1], righe[i + 2], righe[i + 3], righe[i + 4], righe[i + 5])

            # Se il livello non esiste ancora nel dizionario, creiamo una lista vuota
            if d.livello not in domande_per_livello:
                domande_per_livello[d.livello] = []

            # Aggiungiamo la domanda al suo livello corrispondente
            domande_per_livello[d.livello].append(d)

    return domande_per_livello


# 3. Funzione per aggiornare la classifica
def salva_punteggio(nickname, punti, nome_file="punti.txt"):
    classifica = []

    # Proviamo a leggere i vecchi punteggi (se il file esiste)
    try:
        with open(nome_file, 'r', encoding='utf-8') as f:
            for riga in f:
                parti = riga.strip().split()
                if len(parti) >= 2:
                    classifica.append((parti[0], int(parti[1])))
    except FileNotFoundError:
        pass  # Se è la prima partita e il file non esiste, andiamo avanti

    # Aggiungiamo il giocatore attuale
    classifica.append((nickname, punti))

    # Ordiniamo la classifica in base ai punti (il secondo elemento della tupla, indice 1)
    # reverse=True fa in modo che sia decrescente (dal più alto al più basso)
    classifica.sort(key=lambda x: x[1], reverse=True)

    # Salviamo tutto nel file sovrascrivendolo
    with open(nome_file, 'w', encoding='utf-8') as f:
        for nick, score in classifica:
            f.write(f"{nick} {score}\n")


# 4. Il cuore del gioco
def gioca():
    domande = carica_domande("domande.txt")
    livello_corrente = 0
    punti = 0

    # Il gioco continua finché ci sono domande per il livello corrente
    while livello_corrente in domande:
        # Peschiamo una domanda a caso per questo livello
        domanda_scelta = random.choice(domande[livello_corrente])

        print(f"\nLivello {livello_corrente}) {domanda_scelta.testo}")

        # Copiamo la lista delle risposte per non modificare l'originale e le mescoliamo
        risposte_mescolate = list(domanda_scelta.risposte)
        random.shuffle(risposte_mescolate)

        # Troviamo quale numero (da 1 a 4) corrisponde alla risposta corretta
        indice_corretto = risposte_mescolate.index(domanda_scelta.corretta) + 1

        # Stampiamo le opzioni
        for i, risposta in enumerate(risposte_mescolate, start=1):
            print(f"\t{i}. {risposta}")

        scelta_utente = input("Inserisci la risposta: ")

        # Controlliamo se ha inserito un numero e se è quello giusto
        if scelta_utente.isdigit() and int(scelta_utente) == indice_corretto:
            print("Risposta corretta!")
            punti += 1
            livello_corrente += 1
        else:
            print(f"Risposta sbagliata! La risposta corretta era: {indice_corretto}")
            break  # Esce dal ciclo while e finisce la partita

    print(f"\nHai totalizzato {punti} punti!")
    nickname = input("Inserisci il tuo nickname: ")
    salva_punteggio(nickname, punti)


# Questo fa partire il gioco solo se eseguiamo direttamente questo file
if __name__ == "__main__":
    gioca()