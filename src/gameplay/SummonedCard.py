from gameplay.Gameconfig import *

class SummonedCard():
    def __init__(self, name,alignment):
        if(name == "Pawn"):
            self.name = "Pawn"
            self.ATK = 1
        elif(name == "Bishop"):
            self.name = "Bishop"
            self.ATK = 0
        elif(name == "Rook"):
            self.name = "Rook"
            self.ATK = 2
        elif(name == "Queen"):
            self.name = "Queen"
            self.ATK = 4
        self.HP = 6
        self.alignment = alignment
        self.path = self.getpath()

    def TakeDamage(self,amount):
        self.HP -= amount

    def isNotAlive(self):
        return self.HP <= 0
    def Heal(self):
        self.HP = min(6,self.HP+2)

    def HealWeight(self):
        HPHealed = min(6 - self.VirtualHP,2)
        if(self.name == "Pawn"):
            Weight = HPHealed*PAWN_HEAL_WEIGHT
        elif(self.name == "Bishop"):
            Weight = HPHealed*BISHOP_HEAL_WEIGHT
        elif(self.name == "Rook"):
            Weight = HPHealed*ROOK_HEAL_WEIGHT
        else:  #(self.name == "Queen"):
            Weight = HPHealed*QUEEN_HEAL_WEIGHT
        return Weight

    def ATKWeight(self,amount):
        ATKAmount = max(min(amount,self.VirtualHP),0)
        self.VirtualHP -= amount
        if(self.name == "Pawn"):
            Weight = ATKAmount*PAWN_DAMAGE_WEIGHT
        elif(self.name == "Bishop"):
            Weight = ATKAmount*BISHOP_DAMAGE_WEIGHT
        elif(self.name == "Rook"):
            Weight = ATKAmount*ROOK_DAMAGE_WEIGHT
        else:  #(self.name == "Queen"):
            Weight = ATKAmount*QUEEN_DAMAGE_WEIGHT
        return Weight
    
    def isNotAlive(self):
        return self.HP <= 0
    
    def RefreshVirtualHP(self):
        self.VirtualHP = self.HP

    def KillWeight(self):
        if self.VirtualHP <= 0 :
            if(self.name == "Pawn"):
                return PAWN_KILL_WEIGHT
            elif(self.name == "Bishop"):
                return BISHOP_KILL_WEIGHT
            elif(self.name == "Rook"):
                return ROOK_KILL_WEIGHT
            else:  #(self.name == "Queen"):
                return QUEEN_KILL_WEIGHT
        return 0

    def getpath(self):
        return "/static/img/card/"+(self.alignment).lower()+(self.name).lower()+".png"

    def gethppath(self):
        return "/static/img/hp/hp"+str(self.HP)+".png"
    