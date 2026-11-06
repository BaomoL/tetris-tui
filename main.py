from menu import selection_menu, results_menu
from canvas import Canvas
from game import Game
from terminal import raw_mode
from keys import listener
from match import run_match, run_online_match
from net import Connection
import random

game_canvas = Canvas(100, 35)
net = None
try:
    listener.start()
    menu = True
    with raw_mode():

        # both menus don't return until a value has been selected
        while True:

            # game doesn't start until a mode has been selected
            games = []
            
            if menu:
                game_mode, multiplayer_options = selection_menu(game_canvas)
                if game_mode is None:
                    break
            
                menu = False

            # check if multiplayer
        
            if game_mode[0] == "Versus":
                if multiplayer_options == ():
                    game1, game2 = run_match(game_canvas, ("Versus", None, None, None))
                    games = [game1, game2]
                else:
                    net = Connection(*multiplayer_options)
                    seed = random.randint(1, 100000)
                    run_online_match(game_canvas, net, seed)
                    net.close()
            else:
                game = Game(game_canvas, game_mode)
                game.start() 
                games = [game]

            # display results until an option has been selected

            menu = results_menu(game_canvas, games)

finally:
    if net:
        net.close()
    game_canvas.close()
    listener.stop()