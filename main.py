from menu import selection_menu, results_menu, waiting_screen
from canvas import Canvas
from game import Game
from terminal import raw_mode
from keys import listener
from match import run_match, run_online_match
from net import Connection, OpponentPOV
from renderer import display_waiting_join, display_waiting_to_start
import random, time

game_canvas = Canvas(100, 35)
net = None
games = []
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

            # multiplayer options
        
            if game_mode[0] == "Versus":
                if multiplayer_options == ():
                    game1, game2 = run_match(game_canvas, ("Versus", None, None, None))
                    games = [game1, game2]

                elif multiplayer_options[0] == 'host':
                    seed = random.randint(1, 100000)
                    display_waiting_join(game_canvas)
                    net = Connection(*multiplayer_options)
                    waiting_screen(game_canvas)
                    net.send({'start': True, 'seed': seed})
                    # save game results
                    games.append(run_online_match(game_canvas, net, seed))
                    if net.latest:
                        games.append(OpponentPOV(net.latest))        

                    net.close()

                else:
                    net = Connection(*multiplayer_options)
                    while not net.start:
                        display_waiting_join(game_canvas)
                        time.sleep(0.01)
                    seed = net.seed
                    # save game results
                    games.append(run_online_match(game_canvas, net, seed))
                    if net.latest:
                        games.append(OpponentPOV(net.latest))

                    net.close()
                        
            else:
                game = Game(game_canvas, game_mode)
                game.start() 
                games.append(game)

            # display results until an option has been selected

            menu = results_menu(game_canvas, games)

finally:
    if net:
        net.close()
    game_canvas.close()
    listener.stop()