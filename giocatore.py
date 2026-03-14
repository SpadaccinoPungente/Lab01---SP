class Giocatore:
    def __init__(self, nickname = "Guest", punti = None):
        self.nickname = nickname
        self.punti = punti

    def __lt__(self, other):
        if self.punti < other.punti:
            return True
        return False