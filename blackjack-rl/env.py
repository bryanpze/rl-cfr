class Deck():
    def __init__(self, num):
        self.cards = [i if i<10 else 10 for i in range (1,14)] * 4*num