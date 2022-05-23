# HearthstoneChessCPU

A program to recreate the Hearthstone Chess Mini Game

1. How to Run:
- Install python django module
- go to src/frontend/chessweb
- run python manage.py runserver
- open http://localhost:8000/game/ Note:location of localhost may differ.

2. How to play:
- Rules: https://hearthstone.fandom.com/wiki/Chess
- Summon Syntax: "S" or "SUMMON" [hand_id] [board_id] 
- Note: Not case sensitive, Board Id starts and centers at 0
- Example: S 0 0, summon S 1 -1
- Castle Syntax: "C" or "CASTLE" [board_id]
- Example: C 2
- (Util) Next Phase Syntax: "E" or "end"
- (Util) Reset Syntax: "Reset"

3. Things Missing:
- Knight Card (Important: it is almost impossible to win without this card if playing legit)
- Animations

4. Configs:
- Game settings and CPU can be edited in src/gameplay/gameconfig.py