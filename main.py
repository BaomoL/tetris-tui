from menu import selection_menu, results_menu, waiting_screen, connection_lost_screen, play_again_screen, countdown
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

                # host

                elif multiplayer_options[0] == 'host':
                    display_waiting_join(game_canvas, 'host')
                    net = Connection(*multiplayer_options)
                    play_again = True

                    while play_again:

                        if waiting_screen(game_canvas, net):

                            seed = random.randint(1, 100000)

                            games = []
                            net.latest = None
                            net.attacks = []

                            # send signal to start

                            net.send({'start': True, 'seed': seed})

                            countdown(game_canvas)

                            # save game results with append

                            games.append(run_online_match(game_canvas, net, seed))

                            # only wait up to 1 second for official final results
                            now = time.perf_counter()

                            while net.connected and net.latest and not net.latest.get('final', False) and time.perf_counter()-now <= 1:
                                time.sleep(0.01)
                            if net.latest:    
                                games.append(OpponentPOV(net.latest))

                            play_again = play_again_screen(game_canvas, games, net)
                        else:
                            # show lost connection screen; wait to return to menu

                            connection_lost_screen(game_canvas)
                            play_again = False

                        time.sleep(0.01)

                    menu = True
                    net.close()
                    continue

                # joiner

                else:
                    display_waiting_join(game_canvas, 'joiner', multiplayer_options[1])
                    net = Connection(*multiplayer_options)

                    play_again = True

                    while play_again:

                        # wait for game to start

                        while not net.start:
                            # cancel the loop if other player disconnects
                            if not net.connected:
                                break
                            display_waiting_to_start(game_canvas, 'joiner')
                            time.sleep(0.01)

                        if net.start:

                            # reset game states

                            games = []
                            seed = net.seed
                            net.latest = None
                            net.attacks = []

                            countdown(game_canvas)

                            # save game results with append

                            games.append(run_online_match(game_canvas, net, seed))

                            # only wait up to 1 second for official final results
                            now = time.perf_counter()

                            while net.connected and net.latest and not net.latest.get('final', False) and time.perf_counter()-now <= 1:
                                time.sleep(0.01)
                            if net.latest:    
                                games.append(OpponentPOV(net.latest))
                            net.start = False

                            play_again = play_again_screen(game_canvas, games, net)
                        else:

                            connection_lost_screen(game_canvas)
                            play_again = False


                        time.sleep(0.01)

                    net.close()
                    menu = True
                    continue
                        
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