import random


# definisco classe base per contenere i dati della singola domanda
class Domanda:
    def __init__(self, testo, livello, corretta, errata1, errata2, errata3):
        self.testo = testo
        self.livello = int(livello)
        self.corretta = corretta
        self.risposte = [corretta, errata1, errata2, errata3] # salvo tutte le risposte anche in una lista per comodità


# funzione per leggere il file txt e creare le domande
def carica_domande(nome_file):
    domande_per_livello = {}

    with open(nome_file, 'r', encoding='utf-8') as f:
        righe = [riga.strip() for riga in f if riga.strip()]
        # riga.strip() dà false se vuota --> risolve prob riga vuota

    # analizzo la lista a blocchi di 6 (dal momento che non ho più righe vuote)
    for i in range(0, len(righe), 6): # indice: start 0 incluso, step 6 non incluso --> 0, 1, 2, 3, 4, 5, STOP!
        if i + 5 < len(righe): # controllo di sicurezza
            d = Domanda(righe[i], righe[i + 1], righe[i + 2], righe[i + 3], righe[i + 4], righe[i + 5])

            if d.livello not in domande_per_livello: domande_per_livello[d.livello] = []
            # se il livello non esiste ancora nel dizionario, creo una lista vuota

            domande_per_livello[d.livello].append(d)
            # aggiungo la domanda al suo livello corrispondente

    return domande_per_livello


# funzione per aggiornare la classifica
def salva_punteggio(nickname, punti, nome_file="punti.txt"):
    classifica = []

    # proviamo a leggere i vecchi punteggi (se il file esiste)
    try:
        with open(nome_file, 'r', encoding='utf-8') as f:
            for riga in f:
                parti = riga.strip().split()
                if len(parti) >= 2:
                    classifica.append((parti[0], int(parti[1])))
    except FileNotFoundError:
        pass  # se è la prima partita e il file non esiste, andiamo avanti

    # aggiungo il giocatore attuale
    classifica.append((nickname, punti))

    # ordino la classifica in base ai punti (il secondo elemento della tupla, indice 1)
    classifica.sort(key=lambda x: x[1], reverse=True) # reverse=True fa in modo che sia decrescente (dal più alto al più basso)

    # Salviamo tutto nel file sovrascrivendolo
    with open(nome_file, 'w', encoding='utf-8') as f:
        for nick, score in classifica:
            f.write(f"{nick} {score}\n")


# il gioco vero e proprio
def gioca():
    domande = carica_domande("domande.txt")
    livello_corrente = 0
    punti = 0

    while livello_corrente in domande: # controlla che il livello sia presente come chiave del dizionario
        domanda_scelta = random.choice(domande[livello_corrente]) # peschiamo una domanda a caso per questo livello

        print(f"\nLivello {livello_corrente}) {domanda_scelta.testo}")

        # shallow copy (nuova lista, stessi oggetti) della lista delle risposte per mescolare
        risposte_mescolate = list(domanda_scelta.risposte)
        random.shuffle(risposte_mescolate)

        # troviamo quale numero (da 1 a 4) corrisponde alla risposta corretta
        indice_corretto = risposte_mescolate.index(domanda_scelta.corretta) + 1

        # Stampa delle opzioni
        for i, risposta in enumerate(risposte_mescolate, start=1): # di default start=0
            print(f"\t{i}. {risposta}")

        scelta_utente = input("Inserisci la risposta: ")

        # Controlliamo se ha inserito un numero e se è quello giusto
        if scelta_utente.isdigit() and int(scelta_utente) == indice_corretto:
            print("Risposta corretta!")
            punti += 1
            livello_corrente += 1
        else:
            print(f"Risposta sbagliata! La risposta corretta era: {indice_corretto}")
            break  # esce dal ciclo while e finisce la partita

    print(f"\nHai totalizzato {punti} punti!")
    nickname = input("Inserisci il tuo nickname: ")
    salva_punteggio(nickname, punti)


# per far partire il gioco solo se eseguiamo direttamente questo file
if __name__ == "__main__": gioca()