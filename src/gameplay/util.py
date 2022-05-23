def ManaCost(name):
    if(name == "Pawn"):
        return 1
    elif(name == "Bishop"):
        return 3
    elif(name == "Rook"):
        return 3
    elif(name == "Queen"):
        return 7
    else:
        print("THIS SHOULDNT REACH HERE ERROR")
        return -99 

def getPrio(name):
    if(name == "Pawn"):
        return 1
    elif(name == "Bishop"):
        return 2
    elif(name == "Rook"):
        return 3
    elif(name == "Queen"):
        return 4
    else: #(name == "Nothing"):
        return 5
        