# definisco classe base per contenere i dati della singola domanda
class Domanda:
    def __init__(self, testo, livello, corretta, errata1, errata2, errata3):
        self.testo = testo
        self.livello = int(livello)
        self.corretta = corretta
        self.risposte = [corretta, errata1, errata2, errata3] # salvo tutte le risposte anche in una lista per comodità