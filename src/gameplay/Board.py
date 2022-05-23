from gameplay.Deck import *
from gameplay.SummonedCard import *

class Board:
    def __init__(self):
        self.summonedcards = []

    #MAIN PROGRAMS
    def PlaceCard(self,card,cardposition):
        if(len(self.summonedcards) == 0):
            self.summonedcards.insert(0,card)
            return
        positions = self.getboardPositions()
        if(cardposition == positions[0] - 1):
            self.summonedcards.insert(0,card)
            return
        for idx,position in enumerate(positions):
            if(cardposition == position+1):
                self.summonedcards.insert(idx+1,card)
                return
    
    def RemoveCard(self,position):
        selfpositions = self.getboardPositions();
        idx = selfpositions.index(position)
        self.summonedcards.pop(idx)
        return

    def Battle(self,otherPlayer):
        selfpositions = self.getboardPositions();
        otherpositions = otherPlayer.board.getboardPositions();
        if self.isParityEqual(otherPlayer.board):
            for idx,position in enumerate(selfpositions):
                card = self.summonedcards[idx]
                if(card.name == "Bishop"):
                        if (position+2 in selfpositions):
                            self.summonedcards[selfpositions.index(position+2)].Heal()
                        if (position-2 in selfpositions):
                            self.summonedcards[selfpositions.index(position-2)].Heal()
                else:           
                    if(position in otherpositions):
                        otherPlayer.board.summonedcards[otherpositions.index(position)].TakeDamage(card.ATK)
                    else:
                        otherPlayer.HP -= card.ATK
                    
        else:
            for idx,position in enumerate(selfpositions):
                card = self.summonedcards[idx]

                if(card.name == "Bishop"):
                        if (position+2 in selfpositions):
                            self.summonedcards[selfpositions.index(position+2)].Heal()
                        if (position-2 in selfpositions):
                            self.summonedcards[selfpositions.index(position-2)].Heal()
                else:           
                    attacked = False
                    if(position+1 in otherpositions):
                        otherPlayer.board.summonedcards[otherpositions.index(position+1)].TakeDamage(card.ATK)
                        attacked = True
                        # print("Dealt damage ",card.ATK ," to",otherPlayer.board.summonedcards[otherpositions.index(position+1)].name)
                        # print("HP Remaining :",otherPlayer.board.summonedcards[otherpositions.index(position+1)].HP)
                    if(position-1 in otherpositions):
                        attacked = True
                        otherPlayer.board.summonedcards[otherpositions.index(position-1)].TakeDamage(card.ATK)
                        # print("Dealt damage ",card.ATK ," to",otherPlayer.board.summonedcards[otherpositions.index(position-1)].name)
                        # print("HP Remaining :",otherPlayer.board.summonedcards[otherpositions.index(position-1)].HP)
                    if(not attacked):
                        otherPlayer.HP -= card.ATK
        otherPlayer.board.RemoveAllDead()
        return 

    def BattlePrediction(self,otherPlayer):
        selfpositions = self.getboardPositions();
        self.RefreshAllVirtualHP();
        otherPlayer.board.RefreshAllVirtualHP();
        otherpositions = otherPlayer.board.getboardPositions();
        weight = 0
        
        if self.isParityEqual(otherPlayer.board):
            for idx,position in enumerate(selfpositions):
                card = self.summonedcards[idx]

                if(card.name == "Bishop"):
                        if (position+2 in selfpositions):
                            weight += self.summonedcards[selfpositions.index(position+2)].HealWeight()  #Heal Weight
                        if (position-2 in selfpositions):
                            weight += self.summonedcards[selfpositions.index(position-2)].HealWeight()  #Heal Weight
                else:           
                    if(position in otherpositions):
                        weight += otherPlayer.board.summonedcards[otherpositions.index(position)].ATKWeight(card.ATK)  #ATK Weight
                    else:
                        weight += card.ATK*PLAYER_DAMAGE_WEIGHT   #Face Weight
                    
        else:
            for idx,position in enumerate(selfpositions):
                card = self.summonedcards[idx]
                if(card.name == "Bishop"):
                    if (position+2 in selfpositions):
                        weight += self.summonedcards[selfpositions.index(position+2)].HealWeight() 
                    if (position-2 in selfpositions):
                        weight += self.summonedcards[selfpositions.index(position-2)].HealWeight() 
                else:           
                    attacked = False
                    if(position-1 in otherpositions):
                        attacked = True
                        weight += otherPlayer.board.summonedcards[otherpositions.index(position-1)].ATKWeight(card.ATK)
                        # print("Dealt damage ",card.ATK ," to",otherPlayer.board.summonedcards[otherpositions.index(position-1)].name,position-1)
                        # print("HP Remaining :",otherPlayer.board.summonedcards[otherpositions.index(position-1)].VirtualHP)

                    if(position+1 in otherpositions):
                        weight += otherPlayer.board.summonedcards[otherpositions.index(position+1)].ATKWeight(card.ATK)
                        attacked = True
                        # print("Dealt damage ",card.ATK ," to",otherPlayer.board.summonedcards[otherpositions.index(position+1)].name,position+1)
                        # print("HP Remaining :",otherPlayer.board.summonedcards[otherpositions.index(position+1)].VirtualHP)
                    
                    if(not attacked):
                        weight += card.ATK*PLAYER_DAMAGE_WEIGHT   #Face Weight
        weight += otherPlayer.board.TotalKillWeight()
        return weight

    def Castle(self,id):
        self.summonedcards[id],self.summonedcards[id-1]=self.summonedcards[id-1],self.summonedcards[id]
    #GETTERS
    def getAvailablePositions(self):
        positions = []
        if len(self.summonedcards) == 0:
            positions += [0] 
        else:
            if self.isEven():
                idx = 0
            else:
                idx = 1
            while idx <= len(self.summonedcards):
                if idx == 0:
                    positions += [0]                   
                else:
                    positions += [idx]
                    positions += [-idx]
                    
                idx+=2
        return positions

    def isEven(self):
        if len(self.summonedcards) % 2 == 1:
            return False
        return True
    
    def getboardPositions(self):
        positions = []
        if(len(self.summonedcards) == 0):
            return []
        if self.isEven():
            idx = 1
        else:
            idx = 0
        while idx <= len(self.summonedcards):
            if idx == 0:
                positions += [0]                   
            else:
                positions += [idx]
                positions += [-idx]
            idx+=2
        if(positions):
            positions.sort()
        return positions

    def isParityEqual(self,other): #Parity is Odd/Even
        return (len(self.summonedcards) % 2 ) == (len(other.summonedcards) % 2 )

    def getSize(self):
        return len(self.summonedcards)
    #HelperFunctions
    def RemoveAllDead(self):
        i = 0
        while(i < len(self.summonedcards)):
            if(self.summonedcards[i].HP <= 0 ):
                self.summonedcards.pop(i)
            else:
                i+=1

    def RefreshAllVirtualHP(self):
        for card in self.summonedcards:
            card.RefreshVirtualHP()

    def TotalKillWeight(self):
        weight = 0
        for card in self.summonedcards:
            weight += card.KillWeight()
        return weight

    #Utilities
    def PrintBoard(self):
        for card in self.summonedcards:
            print(card.name ,end=" ")
        print()