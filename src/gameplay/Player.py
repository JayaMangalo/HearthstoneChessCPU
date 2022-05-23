from gameplay.Deck import *
from gameplay.Board import *
from gameplay.util import *

class Player:
    def __init__(self,alignment):
        self.deck = Deck(alignment)
        self.board = Board()
        self.hand = []
        
        if(alignment == "White"):
            self.HP = PLAYER_HEALTH
            self.mana = PLAYER_STARTING_MANA
            self.maxmana = PLAYER_STARTING_MANA
            for i in range(PLAYER_STARTING_HAND):
                self.draw()
        else:
            self.HP = CPU_HEALTH
            self.mana = CPU_STARTING_MANA-1 
            self.maxmana = CPU_STARTING_MANA-1
            for i in range(CPU_STARTING_HAND):
                self.draw()
        

    def draw(self):
        if(len(self.deck.arr_cards) == 0):
            return False
        self.hand += [self.deck.drawfromdeck()]
        if(len(self.hand) > 10):
            self.hand.pop(10)
        return True

    def refreshMana(self):
        if self.maxmana < 10:
            self.maxmana+=1
            self.mana = self.maxmana
        else:
            self.mana = self.maxmana

    def canSummon(self,handposition):
        return ManaCost(self.hand[handposition].name) <= self.mana and len(self.board.summonedcards) < 7
    def canCastle(self):
        return self.mana>=1 and self.board.getSize() >=2
   
    def Summon(self,handposition,boardposition): 
        if(not boardposition in self.board.getAvailablePositions()):   
            print("Invalid Position")   
            return           
        if(not self.canSummon(handposition)):
            print("MANA NOT ENOUGH")
            return 
        card = self.hand.pop(handposition)
        self.mana -= ManaCost(card.name)
        self.board.PlaceCard(card,boardposition)
        print("SUMMONED",card.name,"AT POSITION",boardposition)

    def getCheatWeight(self):
        if(self.maxmana >= 2):
            if self.board.getboardPositions():
                return self.board.summonedcards[0].CheatWeight()
        return 0
            
    def inHand(self,cardname):
        for summonedcard in self.hand:
            if(summonedcard.name == cardname):
                return True
        return False
    def removeCard(self,cardname):
        self.hand.pop(self.getHandIndex(cardname))
    def getHandIndex(self,cardname):
        for idx,summonedcard in enumerate(self.hand):
            if(summonedcard.name == cardname):
                return idx
        return -999