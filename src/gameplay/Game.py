from gameplay.Player import *
from queue import Queue
from gameplay.util import *
import copy

class Game():
    def __init__(self):
        self.WKing = Player("White")
        self.BKing = Player("Black")
        self.turn = 1
        self.phase = "PLAYER PLACE PHASE"

    def GameSummon(self,handposition,boardposition): 
        if self.phase == "PLAYER PLACE PHASE":
            self.WKing.Summon(handposition,boardposition)
        else: 
            print("NOT YOUR PLACEMENT PHASE")

    def BlackHeroPower(self):
        if self.WKing.board.summonedcards and self.turn >= 6 :
            self.BKing.mana -=2
            card = self.WKing.board.summonedcards.pop(0)
            print("CHEAT HERO POWER: DESTROYED",card.name)
    def WhiteHeroPower(self,idx):
        id = self.WKing.board.getboardPositions().index(idx)
        if id!=0 and self.WKing.mana >= 1:
            self.WKing.board.Castle(id)
            self.WKing.mana-=1
            print("CASTLE HERO POWER: SWAPPED ID",id,"TO THE LEFT")

    def NextPhase(self):
        if self.phase == "PLAYER PLACE PHASE":
            self.phase = "PLAYER BATTLE PHASE"
            print("WHITE ATTACKED")
            self.WKing.board.Battle(self.BKing)

        elif self.phase == "PLAYER BATTLE PHASE":
            self.phase = "CPU PLACE PHASE"
            print("BLACK'S TURN")
            self.BKing.draw()
            self.BKing.refreshMana()
            self.CPUMove()

        elif self.phase == "CPU PLACE PHASE":
            print("BLACK ATTACKED")
            self.BKing.board.Battle(self.WKing)
            self.phase = "CPU BATTLE PHASE"

        elif self.phase == "CPU BATTLE PHASE":
            print("WHITE'S TURN")
            self.turn+=1
            self.WKing.draw()
            self.WKing.refreshMana()
            self.phase = "PLAYER PLACE PHASE"

    def CPUMove(self):
        self.BlackHeroPower()
        if(len(self.BKing.board.summonedcards) >=7):
            return 
        cardpath,positionpath = self.solve()
        self.doSolution(cardpath,positionpath)

    def getBestPlacement(self,cardname):
        selfboard = self.BKing.board
        enemyplayer = self.WKing

        allpositions = selfboard.getAvailablePositions()
        maxweight = 0
        currentposition = 0

        for position in (allpositions):
            card = SummonedCard(cardname,"Black")
            selfboard.PlaceCard(card,position)
            weight = selfboard.BattlePrediction(enemyplayer)
            if(weight > maxweight):
                maxweight = weight
                currentposition = position 
            selfboard.RemoveCard(position)
        return currentposition,maxweight       

    def solve(self):
        # print("SOLVE TRY")
        q = Queue()
        root = SolutionNode([],[],self,self.BKing.board.BattlePrediction(self.WKing))

        maxweight = -999
        currentsolution = root
        q.put(root)
        while not q.empty():
            Node = q.get()
            # print("CURRWEIGHT:", maxweight)
            # print("NODEWEIGHT:", Node.weight)
            if Node.weight > maxweight:
                maxweight = Node.weight
                currentsolution = Node
            Node.AddBranch(q)

        # print("SOLVE DONE")
        return currentsolution.cardpath,currentsolution.positionpath
            

    def doSolution(self,cardpath,positionpath):
        for i in range (len(cardpath)):
            handposition = self.BKing.getHandIndex(cardpath[i])
            boardposition = positionpath[i]
            self.BKing.Summon(handposition,boardposition)


ALL = ["Pawn","Rook","Bishop","Queen"]
    
class SolutionNode:
    def __init__(self,cardpath,positionpath,game : Game,weight):
        self.cardpath = cardpath
        self.positionpath = positionpath
        self.game = game
        self.weight = weight

    def AddBranch(self,q):
        for cardname in ALL:
            # print("BRANCH ADDED",cardname)
            if self.cardpath:
                last_prio = getPrio(self.cardpath[-1])
            else: 
                last_prio = 0
            if(getPrio(cardname) >= last_prio and ManaCost(cardname) <= self.game.BKing.mana and self.game.BKing.inHand(cardname) and len(self.game.BKing.board.summonedcards) <7):
                gamecopy = copy.deepcopy(self.game)
   
                position,weight = self.game.getBestPlacement(cardname)
                handposition = self.game.BKing.getHandIndex(cardname)

                gamecopy.BKing.Summon(handposition,position)

                cardpath = self.cardpath + [cardname]
                positionpath = self.positionpath + [position]
                # print(cardpath  )
                # print("WEIGHT",weight)
                NewNode = SolutionNode(cardpath, positionpath, gamecopy,weight)
                q.put(NewNode)

        
