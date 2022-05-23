from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import ActionForm
import sys
import os
# insert at 1, 0 is the script path (or '' in REPL)
x = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
sys.path.append(x)

from gameplay import Game

GAME = Game.Game()

def ENDTURN(request):
     GAME.NextPhase()
     
     return index(request)

def index(request):
     if request.method == 'POST':
          # create a form instance and populate it with data from the request:
          form = ActionForm(request.POST)
          # check whether it's valid:
          if form.is_valid():
               action = form.cleaned_data['ACTION']
               first_word = action.split()[0]
               try:
                    global GAME
                    if(first_word.upper() == "SUMMON" or first_word.upper() == "S"):
                         hand_id = int(action.split()[1])
                         board_position = int(action.split()[2])
                         GAME.GameSummon(hand_id,board_position)
                    elif(first_word.upper() == "CASTLE" or first_word.upper() == "C"):
                         board_position = int(action.split()[1])
                         GAME.WhiteHeroPower(board_position)
                    elif(first_word.upper() == "END" or first_word.upper() == "E"):
                         GAME.PlayerENDTURN()
                    elif(first_word.upper() == "RESET"):
                         GAME = Game.Game()
                    else:
                         raise Exception()
               except:
                    print("\nINVALID INPUT\n")

               # process the data in form.cleaned_data as required
               # ...
               # redirect to a new URL:
               
     # if a GET (or any other method) we'll create a blank form
     else:
          form = ActionForm()

     blackkinghand = (GAME.BKing.hand)
     blackkingboard = (GAME.BKing.board.summonedcards)

     whitekinghand = (GAME.WKing.hand)
     whitekingboard = (GAME.WKing.board.summonedcards)
     positions = GAME.WKing.board.getboardPositions()

     new = []
     for i in range(len(whitekingboard)):
          new += [[whitekingboard[i],positions[i]]]

     BKHP = GAME.BKing.HP
     BKMANA = GAME.BKing.mana
     BKMAXMANA = GAME.BKing.maxmana

     TURN = GAME.turn

     WKHP = GAME.WKing.HP
     WKMANA = GAME.WKing.mana
     WKMAXMANA = GAME.WKing.maxmana
     


     template = loader.get_template('game/index.html')
     context = {
          'blackkinghand': blackkinghand,
          'blackkingboard': blackkingboard,
          'whitekinghand': whitekinghand,
          'whitekingboard': new,

          'BKHP': BKHP,
          'BKMANA':BKMANA,
          'BKMAXMANA':BKMAXMANA,
          
          'TURN':TURN,

          'WKHP':WKHP,
          'WKMANA':WKMANA,
          'WKMAXMANA':WKMAXMANA,

          'form': form
     }
     return HttpResponse(template.render(context, request))