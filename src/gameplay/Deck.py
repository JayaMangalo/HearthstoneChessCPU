import random

from gameplay.SummonedCard import SummonedCard

class Deck:
    def __init__(self,alignment):
        self.arr_cards = []
        arr_cards = ["Pawn"] * 16 + ["Bishop"] * 4 + ["Rook"] * 4 + ["Queen"] * 2
        for card in arr_cards:
            cardx = SummonedCard(card,alignment)
            self.arr_cards += [cardx]
        random.shuffle(self.arr_cards)

    def drawfromdeck(self):
        if(self.arr_cards):
            return self.arr_cards.pop()

