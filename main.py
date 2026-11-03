from menu import selection_menu, results_menu
from canvas import Canvas
from game import Game
from terminal import raw_mode
from keys import listener

game_canvas = Canvas(50, 35)
try:
    listener.start()
    menu = True
    with raw_mode():

        # both menus don't return until a value has been selected
        while True:
            # game doesn't start until a mode has been selected
            
            if menu:
                game_mode = selection_menu(game_canvas)
                if game_mode is None:
                    break
            
                menu = False

            game = Game(game_canvas, game_mode)
            game.start()

            # display results until an option has been selected

            menu = results_menu(game_canvas, game)
finally:
    game_canvas.close()
    listener.stop()